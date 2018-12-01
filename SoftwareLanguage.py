from __future__ import print_function
import sys, shlex, operator
import re


tk_http, tk_ftp, tk_telnet, tk_mailto, tk_at, tk_plus, tk_divider, tk_doubledot, tk_dot, tk_space = range(10)

synbols = { '@':tk_at, '+':tk_plus, '/':tk_divider, ':':tk_doubledot, '.':tk_dot, '%':tk_space }
keywords = {'http://':tk_http , 'ftp://':tk_ftp , 'telnet://':tk_telnet, 'mailto::':tk_mailto }
the_col = 0
the_line = 1
the_ch = "" # dummy char
input_file = None
def error(line, col, msg):
    print(line, col, msg)
    
def next_ch():
    global the_ch, the_col, the_line
 
    the_ch = input_file.read(1)
    the_col += 1
    if the_ch == '\n':
        the_line += 1
        the_col = 0
    return the_ch


# main ***

file = open('mock.txt', 'r')


