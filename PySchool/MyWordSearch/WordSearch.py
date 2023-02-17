import numpy as np
import random
import string
import fpdf

def word_across(ar, word):
    elem_len = [1]
    while max(elem_len) != 0:
        word_start = random.randint(0, ar.shape[0] - len(word) - 1)
        row = random.randint(0, ar.shape[0] - 1)
        elem_len = [len(i) for i in ar[word_start:word_start + len(word), row]]  
    ar[word_start:word_start + len(word), row] = [*word]


def word_down(ar, word):
    elem_len = [1]
    while max(elem_len) != 0:
        word_start = random.randint(0, ar.shape[0] - len(word) - 1)
        col = random.randint(0, ar.shape[0] - 1)
        elem_len = [len(i) for i in ar[col, word_start:word_start + len(word)]]  
    ar[col, word_start:word_start + len(word)] = [*word]


def fill_letters(ar):
    with np.nditer(ar,op_flags=['readwrite']) as it:
        for x in it:
            if x == '':
                x[...] = random.choice(string.ascii_lowercase)


def make_word_search(ar):
    for wrd in words:
        word_direction = random.choice([1, 2])
        if word_direction == 1:
            word_across(array, wrd)
        if word_direction == 2:
            word_down(array, wrd)
    fill_letters(ar)


words = ['banana', 'split', 'tupelo']
dims = 10
array = np.zeros((dims, dims), dtype=str)
length_checker = np.vectorize(len)

make_word_search(array)
print(array)
