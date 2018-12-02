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

print("Looking at state: ", end="")
print(nd_xalpha)

# table = { (nd_start, tk_http):[tk_http,nd_httpaddress],\
#           (nd_start, tk_ftp):[tk_ftp,nd_ftp],\
#           (nd_start, tk_telnet):[tk_telnet,nd_telnet],\
#           (nd_start, tk_mailto):[tk_mailto,nd_mailto],\
#           (nd_httpaddress,letter):[nd_hostport,nd_A],\
#           (nd_httpaddress,number):[nd_hostport,nd_A],\
#           (nd_A,tk_divider):[tk_divider,nd_path, nd_J],\
#           (nd_A,tk_question):[tk_question,nd_search],\
#           (nd_A,tk_dollar):[],\
#           (nd_J, tk_question):[tk_question,nd_search],\
#           (nd_J, tk_dollar):[],\
#           (nd_telnet, letter):[nd_login],\
#           (nd_telnet, number):[nd_login],\
#           (nd_ftp, letter):[nd_login,tk_divider,nd_path],\
#           (nd_ftp, number):[nd_login,tk_divider,nd_path],\
#           (nd_mailto, letter):[nd_xalphas,tk_at,nd_hostname],\
#           (nd_mailto, number):[nd_xalphas,tk_at,nd_hostname],\
#           (nd_login, letter):[nd_user,tk_doubledot,nd_password,tk_at,nd_hostport],\
#           (nd_login, number):[nd_user,tk_doubledot,nd_password,tk_at,nd_hostport],\
#           (nd_hostport, letter):[nd_hostname, nd_C],\
#           (nd_hostport, number):[nd_hostname, nd_C],\
#           (nd_C, tk_divider):[],\
#           (nd_C, tk_question):[],\
#           (nd_C, tk_doubledot):[tk_doubledot, nd_port],\
#           (nd_C, tk_dollar):[],\
#           (nd_hostname, letter):[nd_xalphas, nd_D],\
#           (nd_hostname, number):[nd_xalphas, nd_D],\
#           (nd_D,tk_divider):[],\
#           (nd_D,tk_question):[],\
#           (nd_D,tk_doubledot):[],\
#           (nd_D,tk_dot):[tk_dot, nd_hostname],\
#           (nd_D, tk_dollar):[],\
#           (nd_path,letter):[nd_segment, nd_E],\
#           (nd_path,number):[nd_segment, nd_E],\
#           (nd_E,tk_divider):[tk_divider],\
#           (nd_E,tk_question):[tk_question],\
#           (nd_E,tk_dollar):[],\
#           (nd_segment,letter):[nd_xalpha, nd_I],\
#           (nd_segment,number):[nd_xalpha, nd_I],\
#           (nd_I,tk_divider):[],\
#           (nd_I,tk_question):[],\
#           (nd_I,letter):[nd_segment],\
#           (nd_I,number):[nd_segment],\
#           (nd_I,tk_dollar):[],\
#           (nd_search,letter):[nd_xalphas, nd_F],\
#           (nd_search,letter):[nd_xalphas, nd_F],\
#           (nd_F,tk_plus):[tk_plus,nd_search],\
#           (nd_F,tk_dollar):[],\
#           (nd_password,letter):[nd_xalphas],\
#           (nd_password,number):[nd_xalphas],\
#           (nd_G,tk_divider):[],\
#           (nd_G,tk_question):[],\
#           (nd_G,tk_at):[],\
#           (nd_G,tk_doubledot):[],\
#           (nd_G,tk_dot):[],\
#           (nd_G,tk_plus):[],\
#           (nd_G,tk_dollar):[],\
#           (nd_G,letter):[nd_xalphas],\
#           (nd_G,number):[nd_xalphas],\
#           (nd_port):[nd_digits],\
#           (nd_xalpha,letter):[nd_alpha],\
#           (nd_xalpha,number):[nd_digit, nd_H],\
#           (nd_H,tk_divider):[],\
#           (nd_H, tk_question):[],\
#           (nd_H,number):[nd_digits],\
#           (nd_H,tk_dollar):[],\
#           (nd_alpha,letter):[letter],\
#           (nd_digit,number):[number]
# }

x = lambda array: [f'(nd_l,{c}):[nd_segment]' for c in array]
# print(x(number))
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


# ################### states which are not number or letter, didnt add $ rules
# http
key = (nd_start, tk_http)
value = [tk_http, nd_httpaddress]
table[key] = value
# ftp
key = (nd_start, tk_ftp)
value = [tk_ftp, nd_ftp]
table[key] = value
# telnet
key = (nd_start, tk_telnet)
value = [tk_telnet, nd_telnet]
table[key] = value
# mailto
key = (nd_start, tk_mailto)
value = [tk_mailto, nd_mailto]
table[key] = value
# A
# '/'
key = (nd_A, tk_divider)
value = [tk_divider, nd_path, nd_J]
table[key] = value
# '?'
key = (nd_A, tk_question)
value = [tk_question, nd_search]
table[key] = value
# '$'
key = (nd_A, tk_dollar)
value = [tk_epsilon]
table[key] = value
# J
# '?'
key = (nd_J, tk_question)
value = [tk_question, nd_search]
table[key] = value
# '$'
key = (nd_J, tk_dollar)
value = [tk_epsilon]
table[key] = value
# C
# '/'
key = (nd_C, tk_divider)
value = [tk_epsilon]
table[key] = value
# '?'
key = (nd_C, tk_question)
value = [tk_epsilon]
table[key] = value
# ':'
key = (nd_C, tk_doubledot)
value = [tk_doubledot, nd_port]
table[key] = value
# '$'
key = (nd_C, tk_dollar)
value = [tk_epsilon]
table[key] = value
# D
# '/'
key = (nd_D, tk_divider)
value = [tk_epsilon]
table[key] = value
# '?'
key = (nd_D, tk_question)
value = [tk_epsilon]
table[key] = value
# ':'
key = (nd_D, tk_doubledot)
value = [tk_epsilon]
table[key] = value
# '.'
key = (nd_D, tk_dot)
value = [tk_dot, nd_hostname]
table[key] = value
# '$'
key = (nd_D, tk_dollar)
value = [tk_epsilon]
table[key] = value
# E
# '/'
key = (nd_E, tk_divider)
value = [tk_divider, nd_path]
table[key] = value
# '?'
key = (nd_E, tk_question)
value = [tk_epsilon]
table[key] = value
# '$'
key = (nd_E, tk_dollar)
value = [tk_epsilon]
table[key] = value
# I
# '/'
key = (nd_I, tk_divider)
value = [tk_epsilon]
table[key] = value
# '?'
key = (nd_I, tk_question)
value = [tk_epsilon]
table[key] = value
# '$'
key = (nd_I, tk_dollar)
value = [tk_epsilon]
table[key] = value
# F
# '+'
key = (nd_F, tk_plus)
value = [tk_plus, nd_search]
table[key] = value
# '$'
key = (nd_F, tk_dollar)
value = [tk_epsilon]
table[key] = value
# G
# '/'
key = (nd_G, tk_divider)
value = [tk_epsilon]
table[key] = value
# '?'
key = (nd_G, tk_question)
value = [tk_epsilon]
table[key] = value
# '@'
key = (nd_G, tk_at)
value = [tk_epsilon]
table[key] = value
# ':'
key = (nd_G, tk_doubledot)
value = [tk_epsilon]
table[key] = value
# '.'
key = (nd_G, tk_dot)
value = [tk_epsilon]
table[key] = value
# '+'
key = (nd_G, tk_plus)
value = [tk_epsilon]
table[key] = value
# '$'
key = (nd_G, tk_dollar)
value = [tk_epsilon]
table[key] = value
# H
# '/'
key = (nd_H, tk_divider)
value = [tk_epsilon]
table[key] = value
# '?'
key = (nd_H, tk_question)
value = [tk_epsilon]
table[key] = value
# '$'
key = (nd_H, tk_dollar)
value = [tk_epsilon]
table[key] = value

fillDic()
# print(table)



def lexicalAnalysis(url):
    # print(url)    
    stack, pointer = getFirstType(url)
    if len(stack) == 0 and pointer == -1:
        # print('*** incorect url ****:' + url)
        return False, 0

    # print(stack)
    while True:
        state = stack.pop()
        # print("Current state: ", end="")
        # print(state)  

        # terminalState = isStateTerminal(state)
        

        symbol = isToken(url[pointer])  
        # print("Symbol is:", end=" ")
        # print(symbol)

        # print("If state is str:", end=" ")
        # print(isinstance(state, str))

        if isinstance(symbol, int) and state < 20:
            if state == symbol:
                if state == 16:
                    break                
                pointer += 1
                continue

        # if terminalState != "":
        #     if terminalState == url[pointer]:
        #         pointer += 1
        #         continue

        if isinstance(state, str):
            if state == symbol:
                pointer += 1                
                continue
                # break

        if state == tk_epsilon:
            continue

        if state == tk_dollar  and symbol == tk_dollar:
            break

        values = table[(state, symbol)]
        values
        # print("Values of the state: ", end="")
        # print(values)

        for item in reversed(values):
                stack.append(item)        
        # print(stack)

    print("Whole stack:", end=" ")
    print(stack)                

    return True, 0


def isStateTerminal(state):
    if state < 20:
        for key, value in table.items():
            if value == state:
                return key
    else:
        return ""


def isToken(symbol):    
    key = symbols.get(symbol, "NO")
    if isinstance(key, str):
        return symbol
    else:
        return key

    
def getFirstType(url):
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
    result = re.search(symbol, url)
    if len(re.findall(symbol, url)) == 1 and result.start(0) == 0:
        # print(table[(nd_start, keywords[symbol])])
        # print(url[result.end(0)])
        stack = [tk_dollar]
        stack.append(table[(nd_start, keywords[symbol])][1])
        return stack, result.end(0)
    return [], -1

def openFile():
    with open("mock.txt", "r") as fileInput:
        line_number = 0
        for line in fileInput:
            line_number += 1
            answer, error_column = lexicalAnalysis(line)
            if answer:
                print("The input: " + line + " is correct!!")
            else:
                print("The input: " + line + " is incorrect!!")
                print("Error happened at(" + str(line_number) + ", " + str(error_column) + ")")

if __name__ == "__main__":
    openFile()