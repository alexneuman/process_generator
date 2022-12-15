
# from abc import ABC, abstractmethod
from json_template import base_template
from pprint import pprint
import json

class NewPage:
    pass

class Action:
    def __init__(self):
        self.parent = None
        BASE_TEMPLATE = base_template()

    def set_field_name(self, field_name):
        self.obj['field'] = field_name
        return self

    def create(self):
        return self.obj

    def add_child_act(self, action):
        action.parent = self
        self.obj['childActs'].append(action.create())
        return self

    def has_parent(self):
        return self.parent is not None

    def get_closest_parent(self):
        if self.has_parent():
            self = self.parent
        else:
            return self

    def __repr__(self):
        return f'{self.obj}'

class Custom(Action):

    def __init__(self, field_name, value='', ignore_no_capture=True):
        super().__init__()
        self.obj = {
            'actionType': 'custom',
            'field': field_name,
            'value': value,
            'ignoreNoCapture': ignore_no_capture
        }

class Capture(Action):

    def __init__(self, field_name, xpath=[], capturedef=None, optional=False, ignore_no_capture:bool|None=None, value=None, parseType=None):
        super().__init__()
        self.obj = {
            'actionType': 'capture',
            'field': field_name,
            'xPath': xpath,
            'type': 'text',
            'waitfor': 0,
            'optional': optional
        }
        if 'URL' in field_name or 'url' in field_name:
            self.obj['parseType'] = {field_name: 'url'}
            self.obj['type'] = 'attribute',
            self.obj['type'] = self.obj['type'][0]
            self.obj['att'] = 'href'
        
        if capturedef is not None:
            self.obj['captureDef'] = capturedef

        if ignore_no_capture is not None:
            self.obj['ignoreNoCapture'] = ignore_no_capture

        if value is not None:
            self.obj['value'] = value

        if parseType is not None:
            self.obj['parseType'] = parseType
class Input(Action):

    def __init__(self, field_name, xpath=[]):
        super().__init__()
        self.obj = {
            'actionType': 'input',
            'field': field_name,
            'xPath': xpath,
            'waitfor': 0,
            'optional': False,
            'keys': ''
        }

class Click(Action):

    def __init__(self, field_name, xpath=[]):
        super().__init__()
        self.obj = {
            'actionType': 'click',
            'field': field_name,
            'xPath': xpath,
            'waitfor': 0,
            'optional': False,
        }


class IterableAction(Action):

    def __init__(self):
        super().__init__()
        self.obj = {
            'actionType': 'items',
            'field': 'items',
            'xPath': [],
            'waitfor': 0,
            'optional': False,
            'childActs': [
                
            ]
        }

class Items(IterableAction):

    def __init__(self, field_name='results'):
        super().__init__()
        self.obj = {
            'actionType': 'items',
            'field': field_name,
            'xPath': [],
            'waitfor': 0,
            'optional': False,
            'childActs': [
                
            ]
        }

class InputList(IterableAction):

    def __init__(self, field_name='input list', process_name = 'default'):
        super().__init__()
        self.obj = {
            'actionType': 'inputlist',
            'field': field_name,
            'processName': process_name,
            'collectionName': '_data',
            'queryName': 'default',
            'index': '%%index%%',
            'passAlongFields': [
                '__ALL__'
            ],
            'excludeFields': [],
            'childActs': [
                
            ]
        }

class Load(Action, NewPage):
    
    def __init__(self, url_or_input, new_page: int, field_name='load to'):
        super().__init__()
        self.obj = {
            'actionType': 'load',
            'field': field_name,
            'url': url_or_input,
            'newPage': new_page
        }

class CreatePagination(Action, NewPage):

    def __init__(self, field_name='create pagination', code='', block=True):
        super().__init__()
        self.obj = {
            'actionType': 'javascript',
            'field': field_name,
            'code': code,
            'block': block
        }

class Template:

    def __init__(self):
        self.BASE_TEMPLATE = base_template()

    def add_actions_item(self, action_num: int):
        self.BASE_TEMPLATE[f'actions{action_num}'] = []
        return self

    def add_action_to_actions_item(self, action_num, action: Action):
        if not self.BASE_TEMPLATE.get(f'actions{action_num}'):
            self.add_actions_item(action_num)
        self.BASE_TEMPLATE[f'actions{action_num}'].append(action.create())

    def __repr__(self) -> str:
        return f'{self.BASE_TEMPLATE}'

    def to_json(self):
        with open('output.json', 'w') as f:
            json.dump(self.BASE_TEMPLATE, f, indent=4)


template = Template()
items = Items()
subcategories = Items()
subcategories.set_field_name('subcategories')
items.set_field_name('categories')
subcategories.set_field_name('subcategories')
items.add_child_act(subcategories)


# template.to_json()