
from match import input_matcher

def instructions_normalizer():
    instructions = []
    with open('instructions.txt') as f:
        lines = list(f)
        for line in lines:
            pass