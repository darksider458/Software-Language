from __future__ import print_function
import sys, shlex, operator
import re


tk_http, tk_ftp, tk_telnet, tk_mailto, tk_at, tk_plus, tk_divider, tk_doubledot, tk_dot, tk_space, tk_string, tk_EOI = range(12)

synbols = { '@':tk_at, '+':tk_plus, '/':tk_divider, ':':tk_doubledot, '.':tk_dot, '%':tk_space }
keywords = {'http://':tk_http , 'ftp://':tk_ftp , 'telnet://':tk_telnet, 'mailto::':tk_mailto }
the_col = 0
the_line = 1
the_ch = "" # dummy char
input_file = None

regexes = {'http://','ftp://','telnet://','mailto::'}

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

def gettok():
    err_line = the_line
    err_col  = the_col

    if len(the_ch) == 0: return tk_EOI, err_line,err_col
    elif the_ch in synbols:
        sym = synbols[the_ch]
        next_ch()
        return sym, err_line, err_col
    
def getType():
    global input_file
    line = input_file.readline()
    err_line = the_line
    err_col  = the_col

    
    for exp in regexes:
        searchObject =  re.search(exp,line)
        if searchObject:
            return keywords[exp],err_line,err_col
                    
    
# main ***

input_file = open('mock.txt', 'r')
typeOfUrl = getType()

print(typeOfUrl)