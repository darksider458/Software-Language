from __future__ import print_function
import sys, shlex, operator
import re
import string

tk_http, tk_ftp, tk_telnet, tk_mailto,tk_divider, tk_question,tk_at, tk_doubledot, tk_dot, tk_plus, tk_space, tk_string, tk_letter, tk_number, tk_EOI = range(15)

symbols = { '@':tk_at, '+':tk_plus, '/':tk_divider, ':':tk_doubledot, '.':tk_dot, '%':tk_space,'?':tk_question }
keywords = {'http://':tk_http , 'ftp://':tk_ftp , 'telnet://':tk_telnet, 'mailto::':tk_mailto }
letter = list(string.ascii_letters)
number = [str(i) for i in range(0,10)]





# table = { ():[]



# }



def lexicalAnalysis(url):
    pass


def openFile():
    with open('mock.txt', 'r') as samples:
        for line in samples:            
            lexicalAnalysis(line)

if __name__ == "__main__":    
    # openFile()  
    pass  