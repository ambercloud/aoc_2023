from typing import List, Iterator
import re

def parse_input(filename: str) -> List[tuple[str,List[int]]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        springs, _, repdata = line.partition(' ')
        repdata = repdata.removesuffix('\n').split(',')
        output.append((springs, repdata))
    return output

def dictionary(pattern: str) -> Iterator[str]:
    #produces full list of possible words for a given pattern
    def testBit(int_type, offset):
        mask = 1 << offset
        return(int_type & mask)
    #save every wildcard position
    wildcards = [i for i, x in enumerate(pattern) if x == '?']
    #mask is a bitmap of false and true for each corresponding wildcard
    #run through every combination of them, 0 replaces '?' with '#', 1 replaces it with '.'
    for mask in range(2**len(wildcards)):
        word = pattern
        #replace every wildcard according to corresponding bit in mask
        for digit, pos in enumerate(wildcards):
            word = word[:pos] + ('#' if testBit(mask, digit) else '.') + word[pos+1:]
        yield word

def create_regex_string(grammar: List[int]) -> str:
    rules = r'\.*'
    for dashnum in grammar[:-1]:
        rules = rules + '#{' + f'{dashnum}' + r'}\.+'
    rules = rules + '#{' + f'{grammar[-1]}' + r'}\.*'
    return rules

def count_variants(input: tuple[str, List[int]]) -> int:
    pattern, grammar = input
    words = 0
    regex = re.compile(create_regex_string(grammar))
    for word in dictionary(pattern):
        if regex.fullmatch(word):
            words += 1
    print(words)
    return words


input = parse_input('input.txt')
variants_numbers = [count_variants(x) for x in input]
print(sum(variants_numbers))