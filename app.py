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

class Wordle():
    NOT_IN_VOCABULARY = 1
    MATCHED = 0
    MISSED = -1

    def __init__(self, opt=None):
        self.word = words[random.randint(0, len(words)-1)]
        self.remain_attempts = ATTEMPT_COUNT
        self.history = []
        if opt:
            self.mode=opt.mode

    def guess(self):
        for seq in self.history:
            print(seq)
        input_word = input(term_text_colors.UNDERLINE+'?({}):\t'.format(self.remain_attempts))[:5]
        if not input_word in words:
            return self.NOT_IN_VOCABULARY
        print_seq = term_text_colors.RESET+"\t"
        for i in range(len(self.word)):
            if self.word[i] == input_word[i]:
                print_seq += term_bg_colors.GREEN+term_text_colors.BLACK+input_word[i]
            elif input_word[i] in self.word:
                print_seq += term_bg_colors.BLUE+term_text_colors.YELLOW+input_word[i]
            else:
                print_seq += term_text_colors.RESET + input_word[i]
        
        print_seq += term_text_colors.RESET+' '
        self.history.append(print_seq)
        print(print_seq)
        
        if self.word == input_word:
            return self.MATCHED
        return self.MISSED

    def play(self):
        while self.remain_attempts > 0:
            print('')
            result = self.guess()
            if(result==self.NOT_IN_VOCABULARY):
                print("{}\tnot in word list".format(term_text_colors.RESET))
                continue
            if(result==self.MATCHED):
                print("做得好！English Credit + {}".format(random.randint(self.remain_attempts*100,self.remain_attempts*200)))
                self.__init__()
                return True
            else:
                self.remain_attempts -= 1
        
        print("朋友是一个坚韧不拔的纪录片😑, {}".format(self.word))
        self.__init__()
        return False
        
        
            
if __name__ == '__main__':
    game = Wordle(opt)
    game.play()
    
