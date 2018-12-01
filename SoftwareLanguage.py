from __future__ import print_function
import sys, shlex, operator
import re


tk_http, tk_ftp, tk_telnet, tk_mailto,tk_divider, tk_question,tk_at, tk_doubledot, tk_dot, tk_plus, tk_space, tk_string,tk_letter,tk_number, tk_EOI = range(15)

synbols = { '@':tk_at, '+':tk_plus, '/':tk_divider, ':':tk_doubledot, '.':tk_dot, '%':tk_space,'?':tk_question }
keywords = {'http://':tk_http , 'ftp://':tk_ftp , 'telnet://':tk_telnet, 'mailto::':tk_mailto }

table = { ():[]




}

the_col = 0
the_line = 1
current_line = ""
input_file = None

regexes = {'http://','ftp://','telnet://','mailto::'}

def error(line, col, msg):
    #print(line, col, msg)
    return tk_EOI,line,col

def gettok(char):
    err_line = the_line
    err_col  = the_col

    if len(char) == 0: return tk_EOI, err_line,err_col
    elif char in synbols:
        sym = synbols[char]
        return sym, err_line, err_col
    elif char.isalpha() == True: return tk_letter,err_line, err_col
    elif char.isalpha() == False: return tk_number,err_line, err_col
    
def getType():
    global input_file,current_line
    current_line = input_file.readline()
    err_line = the_line
    err_col  = the_col

    
    for exp in regexes:
        searchObject =  re.search(exp,current_line)
        if searchObject:
            return keywords[exp],err_line,err_col
    
    return error(err_line,err_col, "false identifyer of url correct are http:// ,ftp:// , telnet://, mailto::")

def HTTP_Analyze():
    global current_line 
    current_line = current_line.split(' ')
    line = current_line[0]
    line = line[7:]
   
    for char in line:
        token = gettok(char)
        print(token)
        pass



def FTP_Analyze():

    pass  
def TelNet_Analyze():

    pass  
def MailTo_Analyze():

    pass         
    
# main ***

input_file = open('mock.txt', 'r')

while True:
    typeOfUrl = getType()
    value = typeOfUrl[0]


    if value == tk_http:
        HTTP_Analyze()
    elif value == tk_ftp:
        FTP_Analyze()
        pass
    elif value == tk_telnet:
        TelNet_Analyze()
        pass
    elif value == tk_mailto:
        MailTo_Analyze()
        pass
    elif value == tk_EOI:
        break
