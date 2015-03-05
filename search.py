#!/usr/bin/python
import sys
import getopt
import pickle
import math


the_dictionary = {}
boolean_precedence = {'OR':1,'AND':2,'NOT':3,'(':0}
opp_stack = []
output_stack = []
result_stack = []
#-------------------------------------------------------------------------------
   
    
# def single_query(operator,word_1,word_2 = ""):
#     """ perform a boolean search query on word_1 and word_2 with operator. 
#         if operator is NOT then word_2 will be empty
#     """
#     if(operator == "NOT"):
        

def make_queries():

    """
    goes through each line of the query file building
    a post index queue for the queries and then performing that query
    """
    with open(dict_filename, 'r') as d:
        the_dictionary = pickle.load(d)

    with open(queries_filename,'r') as f, open(post_filename,'r') as p:

        for line in f: ##go through each query
            ##opp_stack = []
           ## output_stack = []
            for token in line.split():

                if '(' in token:
                    left, right = token.split('(')
                    push_to_stack(left)
                    push_to_stack('(')
                    push_to_stack(right)

                elif ')' in token:
                    left, right = token.split(')')
                    push_to_stack(left)
                    push_to_stack(')')
                    push_to_stack(right)

                else:
                    push_to_stack(token)
                    
            while opp_stack:
                output_stack.append(opp_stack.pop())
            for i in output_stack:
               print i
            while output_stack:
                token = output_stack.pop(0)
                if(token in boolean_precedence):
                    operand_1 = result_stack.pop()
                    operand_2 = result_stack.pop()
                    if isinstance(operand_1, str):
                        try:
                            p.seek(the_dictionary[operand_1][1])
                            operand_1 =p.readline().split()
                        except KeyError:
                            operand_1 = []
                    
                    if isinstance(operand_2, str):
                        try:
                            p.seek(the_dictionary[operand_2][1])
                            operand_2 =p.readline().split()
                        except KeyError:
                            operand_2 = []
                    if token == "AND":
                        perform_and(operand_1,operand_2)
                    elif token == "OR": 
                        perform_or(operand_1,operand_2)
                else:
                    result_stack.append(token)

                    #perform_query(operand_1,operand_2,token)



 

def perform_and(operand_1,operand_2):
    """
    performs a boolean and operatioin
    """
    result_list = []
    i=0
    j=0
    while i<len(operand_1) and j<len(operand_2):
        if operand_1[i] == operand_2[j]:
            result_list.append[operand_1[i]]
        elif int(operand_1[i]) < int(operand_2[j]):
            i +=1
        else:
            j +=1

        if i == math.sqrt(len(operand_1)):
            if operand_1[i+math.sqrt(len(posting))] < bill[j]:
                i += math.sqrt(len(posting))
        if j == math.sqrt(len(operand_2)):
            if operand_1[j+math.sqrt(len(posting))] < bill[j]:
                j += math.sqrt(len(posting)) 
    return result_list




                

def push_to_stack(token):
    """
    pushes a given token to a stack in the correct way, maitaining precedence
    """
    if token:
        if (token in boolean_precedence) and (token != '('):
            while opp_stack and boolean_precedence[opp_stack[-1]] > boolean_precedence[token]:
                output_stack.append(opp_stack.pop())
            opp_stack.append(token)
            
        elif token == '(':
                opp_stack.append(token)
        
        elif token == ')':
            while opp_stack[-1] != '(': 
                output_stack.append(opp_stack.pop())
            opp_stack.pop()
            
        else:
            output_stack.append(token)


def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries_filename -o output-file-of-results"

dict_filename = post_filename = queries_filename = output_filename = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except:
    usage()
    sys.exit(2)
        
for o, a in opts:
    if o == '-d':
        dict_filename = a
    elif o == '-p':
        post_filename = a
    elif o == '-q':
        queries_filename = a
    elif o == '-o':
        output_filename = a
    else:
        assert False, "unhandled option"
if dict_filename == None or post_filename == None or queries_filename == None or output_filename == None:
    usage()
    sys.exit(2)


make_queries()