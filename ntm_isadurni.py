#!/usr/bin/env python3

import csv
import sys
from collections import deque

def read_ntm(file_stream):
    """Reads and parses an NTM automata file from a csv file."""
    reader = csv.reader(file_stream, delimiter=',')
    # Read the header lines
    machine_name = next(reader)[0]
    state_names = next(reader)
    sigma = next(reader)
    gamma = next(reader)
    start_state = next(reader)[0]
    accept_state = next(reader)[0]
    reject_state = next(reader)[0]

    # Read the transitions
    transitions = []
    for row in reader:
        # Format of transitions:
        current_state, input_char, next_state, tape_write, head_move = row
        transitions.append({
            'current_state': current_state,
            'input_char': input_char,
            'next_state': next_state,
            'tape_write': tape_write,
            'head_move': head_move
        })

    # Return header and transitions in dictionary
    return {
        'machine_name': machine_name,
        'state_names': state_names,
        'sigma': sigma,
        'gamma': gamma,
        'start_state': start_state,
        'accept_state': accept_state,
        'reject_state': reject_state,
        'transitions': transitions
    }

def simulate_ntm(automata, input_string, max_steps=100): # set number of maximum steps to halt machine if exceeded
    """Simulate TM given input string using breadth first search"""
    tape = list(input_string)
    # Read in information
    initial_state = automata['start_state']
    accept_state = automata['accept_state']
    reject_state = automata['reject_state']
    transitions = automata['transitions']

    # Initialize tree of transition configurations
    tree = []

    # Add initial configuration
    initial_config = [["", initial_state, "".join(tape)]]
    tree.append(initial_config)

    total_transitions = 0
    accept_count = 0
    reject_count = 0
    depth = 0

    # Output name and string information
    print(f"Name of Machine: {automata['machine_name']}")
    print(f"Initial String: {input_string}")

    # Compute BFS of transition configurations for as long as you dont exceed limit
    while depth < max_steps:
        current_level = tree[-1]  # Get the current level of the tree
        next_level = []

        for left_of_head, state, right_of_head in current_level:
            tape = list(left_of_head + right_of_head)
            head = len(left_of_head)

            # If we reach an accept state
            if state == accept_state:
                accept_count += 1
                continue

            # If in a reject state, do not explore further
            if state == reject_state:
                reject_count += 1
                next_level.append([left_of_head, state, right_of_head])
                continue

            # Explore all possible transitions
            for transition in transitions:
                if (transition['current_state'] == state and (transition['input_char'] == tape[head] if head < len(tape) else "_")):

                    total_transitions += 1  # Increment the transition count

                    # Create a new tape
                    new_tape = tape[:]
                    if head < len(tape):
                        new_tape[head] = transition['tape_write']
                    else:
                        new_tape.append(transition['tape_write'])

                    # Calculate new position of head
                    if transition['head_move'] == "R":
                        new_head = head + 1
                    elif transition['head_move'] == "L":
                        new_head = head - 1
                    elif transition['head_move'] == "S":
                        new_head = head

                    # Check if we move past the bounds of the tape
                    if new_head < 0:
                        new_tape.insert(0, "_")
                        new_head = 0
                    if new_head >= len(new_tape):
                        new_tape.append("_")

                    # Split the tape from the head
                    new_left_of_head = "".join(new_tape[:new_head])
                    new_right_of_head = "".join(new_tape[new_head:])

                    # Add the new configuration to the next level [left_of_head, state, right_of_head]
                    next_level.append([new_left_of_head, transition['next_state'], new_right_of_head])

        if not next_level: # If there are no more configurations to explore we have reached an accept or reject state
            print(f"Total transitions simulated: {total_transitions}")
            if accept_count:
                print(f"String accepted in {depth} transitions.") # number of transitions = depth
            else:
                print(f"String rejected at depth {depth}.")
            print_tree(tree)
            return

        # Add the next level to the tree
        tree.append(next_level)
        depth += 1

    # If max steps are reached -> reject
    print_tree(tree)
    print(f"Execution stopped after reaching the maximum depth of {max_steps}.")
    print(f"Total transitions simulated: {total_transitions}")

def print_tree(tree): # Print configurations of tape by level/depth
    """Prints the tree of configurations"""
    print("Tree of Configurations:")
    for depth, level in enumerate(tree):
        print(f"Depth {depth}: {level}")

def main():
    # Read the NTM and input string from files ./ntm.py automata.csv string.txt
    with open(sys.argv[1], 'r') as file:
        automata = read_ntm(file)
    with open(sys.argv[2], 'r') as file:
        string = file.read().strip()
    # Simulate the NTM
    simulate_ntm(automata, string)

if __name__ == '__main__':
    main()
