from __future__ import print_function
import sys, shlex, operator
import re
import string

tk_http, tk_ftp, tk_telnet, tk_mailto,tk_divider, tk_question,tk_at, tk_doubledot, tk_dot, tk_plus, tk_space, tk_string, tk_letter, tk_number, tk_EOI, tk_epsilon,tk_dollar = range(17)

nd_start,nd_ftp,nd_telnet,nd_mailto,nd_httpaddress,nd_hostport,nd_A,nd_path,nd_J,nd_search,nd_login,nd_path,nd_user,nd_password,nd_xalphas,nd_hostname,nd_C,\
nd_port,nd_D,nd_segment, nd_E,nd_xalpha, nd_I, nd_F,nd_G,nd_digits,nd_alpha,nd_digit,nd_H = range(20, 20 + 29)
symbols = { '@':tk_at, '+':tk_plus, '/':tk_divider, ':':tk_doubledot, '.':tk_dot, '%':tk_space,'?':tk_question, '$':tk_dollar }
keywords = {'http://':tk_http , 'ftp://':tk_ftp , 'telnet://':tk_telnet, 'mailto::':tk_mailto }
letter = list(string.ascii_letters)
number = [str(i) for i in range(0,10)]
states = {nd_start:"start", nd_ftp:"ftpaddress", nd_telnet:"telnetaddress", nd_mailto:"mailtoaddress", nd_httpaddress:"httpaddress", nd_A:"A", nd_J:"J", nd_login:"login", nd_hostport:"hostport", 
nd_C:"C", nd_hostname:"hostname", nd_D:"D", nd_path:"path", nd_E:"E", nd_segment:"segment", nd_I:"I", nd_search:"search", nd_F:"F", nd_password:"password", nd_user:"user",
nd_xalphas:"xalphas", nd_G:"G", nd_port:"port", nd_xalpha:"xalpha", nd_digits:"digits", nd_H:"H", nd_alpha:"alpha", nd_digit:"digit"}

table ={}

def fillDic():
    for i in number:
        key = (nd_httpaddress,i)
        value = [nd_hostport, nd_A]
        table[key] = value

        key = (nd_telnet,i)
        value = [nd_login]
        table[key] = value

        key = (nd_ftp,i)
        value = [nd_login, tk_divider, nd_path]
        table[key] = value

        key = (nd_mailto,i)
        value = [nd_xalphas, tk_at, nd_hostname]
        table[key] = value

        key = (nd_login,i)
        value = [nd_user, tk_doubledot, nd_password, tk_at, nd_hostport]
        table[key] = value

        key = (nd_hostport,i)
        value = [nd_hostname, nd_C]
        table[key] = value

        key = (nd_path,i)
        value = [nd_segment, nd_E]
        table[key] = value

        key = (nd_segment,i)
        value = [nd_xalphas, nd_I]
        table[key] = value

        key = (nd_I,i)
        value = [nd_segment]
        table[key] = value

        key = (nd_search,i)
        value = [nd_xalphas, nd_F]
        table[key] = value

        key = (nd_password,i)
        value = [nd_xalphas]
        table[key] = value

        key = (nd_user,i)
        value = [nd_xalphas]
        table[key] = value

        key = (nd_xalphas,i)
        value = [nd_xalpha, nd_G]
        table[key] = value

        key = (nd_G,i)
        value = [nd_xalphas]
        table[key] = value

        key = (nd_port,i)
        value = [nd_digits]
        table[key] = value

        key = (nd_xalpha,i)
        value = [nd_digit]
        table[key] = value

        key = (nd_digits,i)
        value = [nd_digit, nd_H]
        table[key] = value

        key = (nd_H,i)
        value = [nd_digits]
        table[key] = value

        key = (nd_digit,i)
        value = [i]
        table[key] = value

    for i in letter:
       
        key = (nd_httpaddress,i)
        value = [nd_hostport, nd_A]
        table[key] = value

        key = (nd_telnet,i)
        value = [nd_login]
        table[key] = value

        key = (nd_ftp,i)
        value = [nd_login, tk_divider, nd_path]
        table[key] = value

        key = (nd_mailto,i)
        value = [nd_xalphas, tk_at, nd_hostname]
        table[key] = value

        key = (nd_login,i)
        value = [nd_user, tk_doubledot, nd_password, tk_at, nd_hostport]
        table[key] = value

        key = (nd_hostport,i)
        value = [nd_hostname, nd_C]
        table[key] = value

        key = (nd_hostname,i)
        value = [nd_xalphas, nd_D]
        table[key] = value

        key = (nd_path,i)
        value = [nd_segment, nd_E]
        table[key] = value

        key = (nd_segment,i)
        value = [nd_xalpha, nd_I]
        table[key] = value

        key = (nd_I,i)
        value = [nd_segment]
        table[key] = value

        key = (nd_search,i)
        value = [nd_xalphas, nd_F]
        table[key] = value

        key = (nd_password,i)
        value = [nd_xalphas]
        table[key] = value

        key = (nd_user,i)
        value = [nd_xalphas]
        table[key] = value

        key = (nd_xalphas,i)
        value = [nd_xalpha, nd_G]
        table[key] = value

        key = (nd_G,i)
        value = [nd_xalphas]
        table[key] = value

        key = (nd_xalpha,i)
        value = [nd_alpha]
        table[key] = value

        key = (nd_alpha,i)
        value = [i]
        table[key] = value


keys = ((nd_start, tk_http),(nd_start, tk_ftp),(nd_start, tk_telnet),(nd_start, tk_mailto),(nd_A, tk_divider),\
(nd_A, tk_question),(nd_A, tk_dollar),(nd_J, tk_question),(nd_J, tk_dollar),(nd_C, tk_divider),(nd_C, tk_question),(nd_C, tk_doubledot),\
(nd_C, tk_dollar),(nd_D, tk_divider),(nd_D, tk_question),(nd_D, tk_doubledot),(nd_D, tk_dot), (nd_D, tk_dollar),\
(nd_E, tk_divider),(nd_E, tk_question),(nd_E, tk_dollar),(nd_I, tk_divider),(nd_I, tk_question),(nd_I, tk_dollar),\
(nd_F, tk_plus),(nd_F, tk_dollar), (nd_G, tk_divider),(nd_G, tk_question),(nd_G, tk_at),(nd_G, tk_doubledot),(nd_G, tk_dot),(nd_G, tk_plus),\
(nd_G, tk_dollar),(nd_H, tk_divider),(nd_H, tk_question),(nd_H, tk_dollar))

values = ([tk_http, nd_httpaddress],[tk_ftp, nd_ftp],[tk_telnet, nd_telnet],[tk_mailto, nd_mailto],[tk_divider, nd_path, nd_J],\
[tk_question, nd_search],[tk_epsilon],[tk_question, nd_search],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_doubledot, nd_port],\
[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_dot, nd_hostname],[tk_epsilon],\
[tk_divider, nd_path],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon],\
[tk_plus, nd_search],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon],\
[tk_epsilon],[tk_epsilon],[tk_epsilon],[tk_epsilon])




def printTopStack(state):
    """This function prints current state of stack so that user can undestand the steps how it got to it"""
    if isinstance(state, str):
        if state in number:
            # print("Top of stack: " + state)
            print("Current top of stack is token: 'number'")
        if state in letter:
            # print("Top of stack: " + state)
            print("Current top of stack is token: 'letter'")
    elif state < 20:
        if state < 4:
            for key, value in keywords.items():
                if state == value:
                    print("Current top of stack is a token: '" + key + "'")
                    break
        else:

            for key, value in symbols.items():
                if state == value:
                    print("Current top of stack is a token: '" + key + "'")
                    break
    else:
        printNonTerminalState(state)

def printNonTerminalState(state):
    """Print non terminal characters in humanly undestandable syntax"""
    value = states[state]
    print("Current top of the stack is state: '" + value + "'")

def lexicalAnalysis(url):  
    """Main part of the analyzer which the main loop of the program and logic"""
    stack, pointer = getFirstType(url)
    if len(stack) == 0 and pointer == -1:
        return False, 0
    
    while True:
        state = stack.pop()
        print("Currently working with char: '" + url[pointer] + "'")
        symbol = isToken(url[pointer]) 
        
                 
        printTopStack(state)

        if isinstance(symbol, int) and state < 20:
            if state == symbol:
                if state == 16:
                    break                
                pointer += 1
                continue

        if isinstance(state, str):
            if state == symbol:
                pointer += 1                
                continue                

        if state == tk_epsilon:
            print("Epsilon rule")
            continue

        if state == tk_dollar  and symbol == tk_dollar:
            break

        doesntExist = table.get((state, symbol), True)
        if isinstance(doesntExist, bool):
            return False, pointer
        values = table[(state, symbol)]
        values        

        for item in reversed(values):
                stack.append(item)                                   

    return True, 0


def isStateTerminal(state):
    """Functions cheks if the state which got from stack is terminal character"""
    if state < 20:
        for key, value in table.items():
            if value == state:
                return key
    else:
        return ""


def isToken(symbol):  
    """Check if symbol which is on input can be substitute for token"""  
    key = symbols.get(symbol, "NO")
    if isinstance(key, str):
        return symbol
    else:
        return key

    
def getFirstType(url):
    """First parse the begining of the URL if the protocol is right and determine next steps of the program"""
    stack, pointer = parseBegining(url, "http://")
    if len(stack) == 2 and pointer != -1:
        return stack, pointer
    stack, pointer = parseBegining(url, "ftp://")
    if len(stack) == 2 and pointer != -1:
        return stack, pointer
    stack, pointer = parseBegining(url, "telnet://")
    if len(stack) == 2 and pointer != 0:
        return stack, pointer
    stack, pointer = parseBegining(url, "mailto::")
    if len(stack) == 2 and pointer != 0:
        return stack, pointer    
    return stack, pointer

def parseBegining(url, symbol):
    """Parse the begining of the URL"""
    result = re.search(symbol, url)
    if len(re.findall(symbol, url)) == 1 and result.start(0) == 0:        
        stack = [tk_dollar]
        stack.append(table[(nd_start, keywords[symbol])][1])
        return stack, result.end(0)
    return [], -1

def openFile():
    """Function which opens file and reads the input from it, then redirects the input to Lexical Analyzer function"""
    with open("mock.txt", "r") as fileInput:
        line_number = 0
        for line in fileInput:
            line_number += 1
            line = re.sub("\n", "$", line)
            answer, error_column = lexicalAnalysis(line)
            line = re.sub("$", "", line)
            if answer:
                print("The input: " + line + " is correct!!")
            else:
                print("The input: " + line + " is incorrect!!")
                print("Error happened at(" + str(line_number) + ", " + str(error_column) + ")")
                if error_column == 0:
                    print("There is problem in protocol used")
            print("******** Next line ***********")

if __name__ == "__main__":
    for i in range(0,len(keys)):
        table[keys[i]] = values[i]
    fillDic()
    openFile()