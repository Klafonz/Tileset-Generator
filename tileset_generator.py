from ast import arg, operator
import argparse
from collections import defaultdict
import itertools
import operator
import time
import sys
import os
from xmlrpc.client import MININT

def clear_console():
    os.system('clear') if os.name == 'posix' else os.system('CLS')
    
def get_input():
    while True:
        try:
            sys.stdout.flush()
            clear_console()
            repeater_chain_length = int(input("Enter the length of your repeater chain...\n"))
            break
        except ValueError:
            sys.stdout.flush()
            clear_console()
            print("\033[31mThe length must be a valid integer.\033[0m")
            time.sleep(1)
    while True:
        try:
            sys.stdout.flush()
            clear_console()
            outfile = str(input("Enter an output file path (Optional)...\n"))
            if not outfile:
                break
            with open(outfile, 'w') as fstream:
                fstream.write("")
            os.remove(outfile)
            break
        except OSError:
            sys.stdout.flush()
            clear_console()
            print("\033[31mThe string must be a valid file name.\033[0m")
            time.sleep(1)

    return (repeater_chain_length, outfile)

def generate_repeater_list(repeater_chain_length):
    repeater_list = []
    i = 0
    while len(repeater_list) < repeater_chain_length or i % 4 != 0:
        repeater_list.append(((i % 4) + 1) * 2)
        i += 1
    return repeater_list

def calculate_order(permutations, repeater_chain_length):
    ordered_permutations = {}
    prelim_ordered_permutations = {}
    final_gt_count = defaultdict(lambda: 0)
    for permutation in permutations:
        gt = 0
        gt_list = []
        for val in permutation:
            gt += val
            gt_list.append(gt)
        final_gt_count[gt] += 1
        prelim_ordered_permutations[tuple(gt_list)] = permutation
    max_val = MININT
    for k, v in final_gt_count.items():
        if max(v, max_val) > max_val:
            final_gt = k
            max_val = max(v, max_val)
    prelim_ordered_permutations = {k: v for k, v in prelim_ordered_permutations.items() if k[len(k) - 1] == final_gt}
    range_iter = reversed(range(repeater_chain_length))
    ordered_permutations_gt = sorted(prelim_ordered_permutations, key=operator.itemgetter(*range_iter))
    for gt_list in ordered_permutations_gt:
        ordered_permutations[gt_list] = prelim_ordered_permutations[gt_list]
    return ordered_permutations

def display_repeaters_to_console(ordered_permutations, repeater_dict_console):
    i = 1
    sys.stdout.flush()
    clear_console()

    for k, v in ordered_permutations.items():
        v = list(v)
        print(f"\nSubtick {i}\n")
        print(f"{[int(x / 2) for x in v]}")
        v.reverse()
        i += 1
        for gt in v:
            print(repeater_dict_console[gt], end="", flush=True)

def write_repeaters_to_file(ordered_permutations, repeater_dict_console, repeater_dict_txt, args):
    if not args.output:
        return
    i = 1
    with open(args.output, "w", encoding="utf-8") as fstream:
        fstream.write("")
    fstream =  open(args.output, "a", encoding="utf-8")
    for k, v in ordered_permutations.items():
        v = list(v)
        fstream.write(f"Subtick {i}\n")
        fstream.write(f"{[int(x / 2) for x in v]}")
        v.reverse()
        i += 1
        for gt in v:
            fstream.write(repeater_dict_txt[gt])
    fstream.close()

def display_repeaters(ordered_permutations, args):
    repeater_dict_console = \
    {
        2: """
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[0;1;101;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """,
        4: """
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[0;1;101;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """,
        6: """
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[0;1;101;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """,
        8: """
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[4;1;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒\33[0;1;101;91m▓▓\33[0m▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """
    }
    repeater_dict_txt = \
    {
        2: 
"""
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
""",
        4: 
"""
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
""",
        6: 
"""
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
""",
        8: 
"""
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒
            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
"""
    }

    display_repeaters_to_console(ordered_permutations, repeater_dict_console)
    write_repeaters_to_file(ordered_permutations, repeater_dict_console, repeater_dict_txt, args)
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, required=False)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    (repeater_chain_length, outfile) = get_input()
    if outfile:
        args.output = f"{outfile}.txt"
    repeater_list = generate_repeater_list(repeater_chain_length)
    permutations = list(itertools.permutations(repeater_list, repeater_chain_length))
    ordered_permutations = calculate_order(permutations, repeater_chain_length)
    display_repeaters(ordered_permutations, args)
    input("Press any key to continue...")

if __name__ == "__main__":
    main()