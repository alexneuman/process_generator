

from actions_normalizer import actions_normalizer
from actions import InputList, Load, CreatePagination, Capture, Input, Click, Template

from pytest import fixture

@fixture
def template():
    template = Template()
    return template

@fixture
def actions1():
    actions = [
        InputList('testing input list', 'testing process name'),
        Load('https://www.google.com', new_page=2, field_name='load to url'),
    ]
    return actions

def test_add_actions(actions1, template):
    template.add_actions_item(actions1[0])

def test_actions_in_template(actions1, template):
    template.add_actions_item(actions1[0])
    assert template.BASE_TEMPLATE.get['actions1']
