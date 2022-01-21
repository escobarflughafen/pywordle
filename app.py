from ast import arg
import random
import os
import sys
import time
import argparse

parser=argparse.ArgumentParser(description="Wordle: a word guessing game")
parser.add_argument('-l', '--length', type=int, default=5)
parser.add_argument('-t', '--attempt', type=int, default=6)
parser.add_argument('-m', '--mode', type=str, default="normal")
opt = parser.parse_args()

PATH = './'
FILENAME = '30k_most_freq.txt'
WORDLENGTH = opt.length
ATTEMPT_COUNT = opt.attempt

wordfile = open(os.path.join(PATH, FILENAME), 'r')
words = wordfile.read().split('\n')
wordfile.close()

def init(words):
    return list(
        filter(
            lambda x: len(x) == WORDLENGTH,
            list(
                map(lambda x: x.split('\t')[0], words)
            )
        )
    )

words = init(words)

class term_bg_colors:
    BLACK = u'\u001b[40m'
    RED = u'\u001b[41m'
    GREEN = u'\u001b[42m'
    YELLOW = u'\u001b[43m'
    BLUE = u'\u001b[44m'
    MAGENTA = u'\u001b[45m'
    CYAN = u'\u001b[46m'
    WHITE = u'\u001b[47m'


class term_text_colors:
    BLACK = u'\u001b[30m'
    RED = u'\u001b[31m'
    GREEN = u'\u001b[32m'
    YELLOW = u'\u001b[33m'
    BLUE = u'\u001b[34m'
    MAGENTA = u'\u001b[35m'
    CYAN = u'\u001b[36m'
    WHITE = u'\u001b[37m'
    BOLD = u'\u001b[1m'
    UNDERLINE = u'\u001b[4m'
    REVERSED = u'\u001b[7m'
    RESET = u'\u001b[0m'


print(term_text_colors.RESET)


class Character():
    CORRECT_SPOT = 1
    WRONG_SPOT= 0
    NOT_IN_ANY_SPOT= -1

    bg_color = {
        CORRECT_SPOT:       term_bg_colors.GREEN, 
        WRONG_SPOT:         term_bg_colors.CYAN,
        NOT_IN_ANY_SPOT:    term_bg_colors.BLACK
    }

    text_color = {
        CORRECT_SPOT:       term_text_colors.BLACK, 
        WRONG_SPOT:         term_text_colors.BLACK,
        NOT_IN_ANY_SPOT:    term_text_colors.WHITE
    }

    blocks={
        CORRECT_SPOT:       '🟩', 
        WRONG_SPOT:         '🟨',
        NOT_IN_ANY_SPOT:    '⬜'
    }

    def __init__(self, ch, status):
        self.ch = ch
        self.status = status

    def get_esc_str(self):
        return self.bg_color[self.status] + self.text_color[self.status] + self.ch
    
    def get_blocks(self):
        return self.blocks[self.status]

class Word():
    def __init__(self, seq):
        self.seq = seq

    def get_print_seq(self):
        print_seq = ''.join(list(map(lambda ch: ch.get_esc_str(), self.seq)))
        print_seq += term_text_colors.RESET+' '
        return print_seq

    def get_block_seq(self):
        return ''.join(list(map(lambda ch: ch.get_blocks(), self.seq)))



class Wordle():
    NOT_IN_VOCABULARY = 1
    MATCHED = 0
    MISSED = -1

    def __init__(self, opt=None):
        self.round = 0
        self.word = words[random.randint(0, len(words)-1)]
        self.remain_attempts = ATTEMPT_COUNT
        self.history = []
        if opt:
            self.mode=opt.mode
    
    def reset(self):
        self.word = words[random.randint(0, len(words)-1)]
        self.remain_attempts = ATTEMPT_COUNT
        self.history = []

    def print_attempts(history):
        for attempt in history:
            print(attempt)

    def guess(self):
        history_seq = (list(map(lambda x: '\t'+x.get_print_seq(), self.history)))
        print('\n'.join(history_seq))
        input_word = input(term_text_colors.UNDERLINE+'?({}):\t'.format(self.remain_attempts))[:WORDLENGTH]
        if not input_word in words:
            return self.NOT_IN_VOCABULARY
        print_seq = term_text_colors.RESET+"\t"
        guessed_chars = []
        for i in range(len(self.word)):
            if self.word[i] == input_word[i]:
                guessed_chars.append(Character(input_word[i], Character.CORRECT_SPOT))
            elif input_word[i] in self.word:
                guessed_chars.append(Character(input_word[i], Character.WRONG_SPOT))
            else:
                guessed_chars.append(Character(input_word[i], Character.NOT_IN_ANY_SPOT))

        guessed_word = Word(guessed_chars)
        self.history.append(guessed_word)
        print(term_text_colors.RESET+'\t'+guessed_word.get_print_seq())

        if self.word == input_word:
            return self.MATCHED
        return self.MISSED

    def share(self):
        s = '\n\tWordle {} {}/{}\n\n'.format(self.round, len(self.history), self.remain_attempts+len(self.history))
        s += '\n'.join(
            list(map(lambda word: '\t'+word.get_block_seq(), self.history))
        )
        s += '\n'
        return s


    def play(self):
        word = self.word
        log = open('./log.txt', 'a')
        log.write('{}\n'.format(self.word))
        log.close()
        matched = False
        while self.remain_attempts > 0:
            print('')
            result = self.guess()
            if(result==self.NOT_IN_VOCABULARY):
                print("{}\tnot in word list".format(term_text_colors.RESET))
                continue
            self.remain_attempts -= 1
            if(result==self.MATCHED):
                matched=True
                break

        self.round += 1

        print('\n\t')
        if matched:
            print("做得好！English Credit + {}".format(random.randint(self.remain_attempts*100,self.remain_attempts*200)))
        else:
            print("朋友是一个坚韧不拔的纪录片😑, {}".format(self.word))

        print(self.share())
        self.reset()
        return matched


if __name__ == '__main__':
    game = Wordle(opt)
    game.play()

