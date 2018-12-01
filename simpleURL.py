from __future__ import print_function
import sys, shlex, operator
import re
import string

tk_http, tk_ftp, tk_telnet, tk_mailto,tk_divider, tk_question,tk_at, tk_doubledot, tk_dot, tk_plus, tk_space, tk_string, tk_letter, tk_number, tk_EOI, tk_epsilon,tk_dollar = range(17)

nd_start,nd_ftp,nd_telnet,nd_mailto,nd_httpaddress,nd_hostport,nd_A,nd_path,nd_J,nd_search,nd_login,nd_path,nd_user,nd_password,nd_xalphas,nd_hostname,nd_C,\
nd_port,nd_D,nd_segment, nd_E,nd_xalpha, nd_I, nd_F,nd_G,nd_digits,nd_alpha,nd_digit,nd_H = range(29)

symbols = { '@':tk_at, '+':tk_plus, '/':tk_divider, ':':tk_doubledot, '.':tk_dot, '%':tk_space,'?':tk_question }
keywords = {'http://':tk_http , 'ftp://':tk_ftp , 'telnet://':tk_telnet, 'mailto::':tk_mailto }
letter = list(string.ascii_letters)
number = [str(i) for i in range(0,10)]



        # current state, current token, : what to push
table = { (nd_start, tk_http):[tk_http,nd_httpaddress],\
          (nd_start, tk_ftp):[tk_ftp,nd_ftp],\
          (nd_start, tk_telnet):[tk_telnet,nd_telnet],\
          (nd_start, tk_mailto):[tk_mailto,nd_mailto],\
          (nd_httpaddress,letter):[nd_hostport,nd_A],\
          (nd_httpaddress,number):[nd_hostport,nd_A],\
          (nd_A,tk_divider):[tk_divider,nd_path, nd_J],\
          (nd_A,tk_question):[tk_question,nd_search],\
          (nd_A,tk_dollar):[],\
          (nd_J, tk_question):[tk_question,nd_search],\
          (nd_J, tk_dollar):[],\
          (nd_telnet, letter):[nd_login],\
          (nd_telnet, number):[nd_login],\
          (nd_ftp, letter):[nd_login,tk_divider,nd_path],\
          (nd_ftp, number):[nd_login,tk_divider,nd_path],\
          (nd_mailto, letter):[nd_xalphas,tk_at,nd_hostname],\
          (nd_mailto, number):[nd_xalphas,tk_at,nd_hostname],\
          (nd_login, letter):[nd_user,tk_doubledot,nd_password,tk_at,nd_hostport],\
          (nd_login, number):[nd_user,tk_doubledot,nd_password,tk_at,nd_hostport],\
          (nd_hostport, letter):[nd_hostname, nd_C],\
          (nd_hostport, number):[nd_hostname, nd_C],\
          (nd_C, tk_divider):[],\
          (nd_C, tk_question):[],\
          (nd_C, tk_doubledot):[tk_doubledot, nd_port],\
          (nd_C, tk_dollar):[],\
          (nd_hostname, letter):[nd_xalphas, nd_D],\
          (nd_hostname, number):[nd_xalphas, nd_D],\
          (nd_D,tk_divider):[],\
          (nd_D,tk_question):[],\
          (nd_D,tk_doubledot):[],\
          (nd_D,tk_dot):[tk_dot, nd_hostname],\
          (nd_D, tk_dollar):[],\
          (nd_path,letter):[nd_segment, nd_E],\
          (nd_path,number):[nd_segment, nd_E],\
          (nd_E,tk_divider):[tk_divider],\
          (nd_E,tk_question):[tk_question],\
          (nd_E,tk_dollar):[],\
          (nd_segment,letter):[nd_xalpha, nd_I],\
          (nd_segment,number):[nd_xalpha, nd_I],\
          (nd_I,tk_divider):[],\
          (nd_I,tk_question):[],\
          (nd_I,letter):[nd_segment],\
          (nd_I,number):[nd_segment],\
          (nd_I,tk_dollar):[],\
          (nd_search,letter):[nd_xalphas, nd_F],\
          (nd_search,letter):[nd_xalphas, nd_F],\
          (nd_F,tk_plus):[tk_plus,nd_search],\
          (nd_F,tk_dollar):[],\
          (nd_password,letter):[nd_xalphas],\
          (nd_password,number):[nd_xalphas],\
          (nd_G,tk_divider):[],\
          (nd_G,tk_question):[],\
          (nd_G,tk_at):[],\
          (nd_G,tk_doubledot):[],\
          (nd_G,tk_dot):[],\
          (nd_G,tk_plus):[],\
          (nd_G,tk_dollar):[],\
          (nd_G,letter):[nd_xalphas],\
          (nd_G,number):[nd_xalphas],\
          (nd_port):[nd_digits],\
          (nd_xalpha,letter):[nd_alpha],\
          (nd_xalpha,number):[nd_digit, nd_H],\
          (nd_H,tk_divider):[],\
          (nd_H, tk_question):[],\
          (nd_H,number):[nd_digits],\
          (nd_H,tk_dollar):[],\
          (nd_alpha,letter):[letter],\
          (nd_digit,number):[number]
}

print(table)

def lexicalAnalysis(url):
    pass


def openFile():
    with open('mock.txt', 'r') as samples:
        for line in samples:            
            lexicalAnalysis(line)

if __name__ == "__main__":    
    openFile()    