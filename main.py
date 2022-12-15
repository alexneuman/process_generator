
from actions import Template, Items, InputList, Load, IterableAction, CreatePagination, Capture, NewPage, Input, Click
from actions_normalizer import actions_normalizer
from actions_director import get_actions, template
from inputs import input_columns, captures


actions = get_actions()
normalizer = actions_normalizer(actions)
# print('\n')
current_page_num = 1
for i, action in enumerate(actions):
    prev_action = None
    next_action = None
    
    if i > 0:
        prev_action = actions[i-1]
    if i < len(actions)-1:
        next_action = actions[i+1]

    
    if not prev_action:
        template.add_action_to_actions_item(current_page_num, action)
    
    elif isinstance(action, NewPage) and isinstance(prev_action, IterableAction):
        parent = action.parent or prev_action
        parent.add_child_act(action)
        current_page_num += 1
    
    elif isinstance(prev_action, NewPage) and isinstance(action, IterableAction):
        template.add_action_to_actions_item(current_page_num, action)
    

    elif isinstance(prev_action, Items) and not isinstance(action, NewPage):
        parent = action.parent or prev_action
        parent.add_child_act(action)

    elif isinstance(action, NewPage) and not isinstance(prev_action, NewPage):
        try:
            parent = prev_action.parent or prev_action
            parent.add_child_act(action) 
        except KeyError:
            template.add_action_to_actions_item(current_page_num, action)
        current_page_num += 1
        # print(action, current_page_num)


    elif isinstance(action, NewPage):
        template.add_action_to_actions_item(current_page_num, action)
        current_page_num += 1

    elif isinstance(action, Items):
        parent = action.parent or prev_action
        if not isinstance(parent, Items):
            parent = parent.parent
        try:
            parent.add_child_act(action)
        except AttributeError:
            template.add_action_to_actions_item(current_page_num, action)

    elif not isinstance(action, NewPage) and not isinstance(prev_action, NewPage) and not isinstance(prev_action, Items) and not isinstance(next_action, Items):
        try:
            # print(action)
            parent = action.parent or prev_action.parent
            # print(action, '\n', parent)
            parent.add_child_act(action)
        except AttributeError:
            template.add_action_to_actions_item(current_page_num, action)

    elif not isinstance(action, NewPage) and not isinstance(prev_action, NewPage) and not isinstance(prev_action, Items) and isinstance(next_action, Items):
        parent = action.parent or prev_action.parent
        if not parent:
            template.add_action_to_actions_item(current_page_num, action)
        else:
            parent.add_child_act(action)

    else:
        # print(action)
        template.add_action_to_actions_item(current_page_num, action)

template.to_json()