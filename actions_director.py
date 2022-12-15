
import csv
import re
from difflib import get_close_matches

from actions import Template, Items, InputList, Load, IterableAction, CreatePagination, Capture, NewPage, Input, Click, Custom
from actions_normalizer import actions_normalizer
from pagination import get_pagination_actions
from match import input_matcher, capture_matcher
from inputs import input_columns, captures


template = Template()


def capture_action(line, current_page_num, field_name=None):
    # note this is not a pure function as it mutates the captures list
    if not field_name:
        field_name = re.search(r'CAPTURE (.*)', line).group(1)
    match = capture_matcher(field_name)
    if match:
        field_name = match
    
    action = Capture(field_name)
    return action

def inputlist_action(line):
    field_name = (re.search(r'INPUT LIST (.*)', line) or re.search(r'.*THROUGH (.*)', line)).group(1)

    action = InputList(field_name=field_name)
    return action

def input_action(line):
    field_name = (re.search(r'SEARCH (.*)', line) or re.search('INPUT (.*)', line)).group(1)
    field_name.replace(' FOR ', '')
    action = Input(field_name=f'input {field_name}')
    return action

def items_action(line):
    field_name = re.search(r'ITERATE THROUGH (.*)', line).group(1)
    action = Items(field_name=field_name)
    return action

def load_action(line, current_page_num):
    field_name = re.search(r'LOAD TO (.*)', line).group(1)
    url_or_input = field_name
    if 'http' in field_name:
        field_name = 'url' # this needs to be changed to dynmaically get the field name
    else:
        url_or_input = f'%%{field_name}%%'
    action = Load(url_or_input, new_page=current_page_num+1, field_name=f'load to {field_name}')
    return action

def pagination_action(line, current_page_num):
    action = CreatePagination()
    return action

def click_action(line, current_page_num):
    field_name = re.search(r'CLICK (.*)', line).group(1)
    field_name = field_name.replace('CLICK', '').replace('click', '').strip()
    action = Click(field_name='click '+field_name)
    return action

def custom_action(line, current_page_num):
    ignore_no_capture = True
    field_name = re.sub(r'\s+=\s+?', '=', line).replace('= ', '=')
    if  '=' in line:
        field_name, value = re.search(r'CUSTOM (.*)', field_name).group(1).split('=')
        ignore_no_capture = False
    else:
        value = ''
    action = Custom(field_name=field_name, value=value, ignore_no_capture=ignore_no_capture)
    return action


def get_actions():
    actions = []
    with open('instructions.txt') as f:
        current_page_num = 1
        lines = list(f)
        for i, line in enumerate(lines):
            current_actions = []
            # print(line)
            if 'STARTING' in line and 'ITERATE' in line or ' INPUTS' in line:
                field_name = (re.search(r'INPUT LIST (.*)', line) or re.search(r'.*THROUGH (.*)', line)).group(1)
                match = input_matcher(field_name)
                current_actions.append(inputlist_action(line))
                if match:
                    field_name = match
                    if 'url' in field_name.lower():
                        pass
                        # current_page_num += 1
                        # current_actions.append(Load(field_name, new_page=current_page_num, field_name=f'load to {field_name}'))
                        # current_page_num += 1
                        print(match)
                        # input_columns.remove(field_name)


            elif 'ITERATE' in line and 'PAGINAT' not in line:
                print('ITERATE ACTION')
                # actions.append((capture_action(line, current_page_num, 'TEST'), line))
                current_actions.append(items_action(line))

            elif 'LOAD TO ' in line:
                # print('LOAD ACTION')
                current_actions.append(load_action(line, current_page_num))
                current_page_num += 1

            elif 'PAGINAT' in line:
                # pagination is a special case, the pagination action is a list of actions
                for action in get_pagination_actions(line):
                    actions.append(action)
                current_page_num += 1
                continue

            elif 'CAPTURE' in line:
                print('CAPTURE ACTION')
                current_actions.append(capture_action(line, current_page_num))

            elif 'INPUT' in line or 'SEARCH' in line or 'ENTER' in line:
                current_actions.append(input_action(line))

            elif 'SCROLL THROUGH' in line:
                current_actions.append(pagination_action(line, current_page_num))

            elif line.startswith('CUSTOM'):
                current_actions.append(custom_action(line, current_page_num))

            elif 'CLICK' in line:
                current_actions.append(click_action(line, current_page_num))

            if not current_actions:
                raise Exception(f'Invalid line {line}')

            
            for action in current_actions:
                actions.append(action)

    return actions



