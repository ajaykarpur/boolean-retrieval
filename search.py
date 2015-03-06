#!/usr/bin/python
import sys
import getopt
import pickle
import math
import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

the_dictionary = {}
boolean_precedence = {'OR':1,'AND':2,'NOT':3,'(':0}
opp_stack = []
output_stack = []
result_stack = []
universal_set = []
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
    with open(dict_filename, 'r') as d,open("all_doc_ids.txt",'r') as u:
        the_dictionary = pickle.load(d)
        universal_set = pickle.load(u)
    #print the_dictionary
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

            while output_stack:
                token = output_stack.pop(0)
                if token == "NOT":
                    operand = result_stack.pop()
                    if isinstance(operand, basestring):
                        try:
                            p.seek(the_dictionary[operand][1])
                            operand = p.readline().split()
                            operand.insert(0,"NOT")
                        except KeyError:
                            operand = ["0"]
                            operand.insert(0,"NOT")
                    elif operand[0] == "NOT": # NOT NOT cancels
                        operand.pop(0)
                    else :
                        operand.insert(0,"NOT")
                    result_stack.append(operand)
                elif(token in boolean_precedence and token != "NOT"):
                    operand_1 = result_stack.pop()
                    operand_2 = result_stack.pop()
                    if isinstance(operand_1, basestring):
                        try:
                            p.seek(the_dictionary[operand_1][1])
                            operand_1 =p.readline().split()
                        except KeyError:
                            operand_1 = ["0"]
                    
                    if isinstance(operand_2, basestring):
                        try:
                            p.seek(the_dictionary[operand_2][1])
                            operand_2 = p.readline().split()
                        except KeyError:
                            operand_2 = ["0"]
                    if token == "AND":
                        if(operand_1[0] == "NOT" or operand_2[0] == "NOT"):
                            result_stack.append(perform_not_and(operand_1,operand_2))
                        else:
                            result_stack.append(perform_and(operand_1,operand_2))
                    elif token == "OR":
                        if(operand_1[0] == "NOT" or operand_2[0] == "NOT"):
                            result_stack.append(perform_not_or(operand_1,operand_2)) 
                        else:  
                            result_stack.append(perform_or(operand_1,operand_2))
                else:
                    result_stack.append(token)
            result = result_stack.pop()
            if result[0] == "NOT":
                result.pop(0)
                result = a_less_b(universal_set,result)
            print "here is the result"
            print result


 
def perform_not_or(operand_1,operand_2):
    result_list = []
    if(operand_1[0] == "NOT" and operand_2[0] == "NOT"):
        result_list = perform_and(operand_1.pop(0),operand_2.pop(0))
        result_list.insert(0,"NOT")
    elif(operand_1[0] == "NOT"):
        result_list = operand_1
    else:
        result_list = operand_2
    return result_list

def perform_not_and(operand_1,operand_2):
    result_list = []
    if(operand_1[0] == "NOT" and operand_2[0] == "NOT"):
        result_list = perform_or(operand_1.pop(0),operand_2.pop(0))
        result_list.insert(0,"NOT")
    elif(operand_1[0] == "NOT"):
        operand_1.pop(0)
        result_list = a_less_b(operand_2,operand_1)
    else:
        operand_2.pop(0)
        result_list = a_less_b(operand_1,operand_2)
    return result_list

def a_less_b(operand_1,operand_2):
    """
    returns the set operand_1 less everything thats in the set operand_2
    """
    i = j = 0
    skip_1 = int(math.sqrt(len(operand_1)))
    skip_2 = int(math.sqrt(len(operand_2)))
    while i<len(operand_1) and j<len(operand_2):
        if operand_1[i] == operand_2[j]:
            operand_1.pop(i)
            i +=1
            j +=1
        elif int(operand_1[i]) < int(operand_2[j]):
            i +=1
        else:
            j +=1

        if (i == skip_1) and ((i+skip_1) < len(operand_1)):
            if operand_1[i+skip_1] < operand_2[j]:
                i += skip_1
        if (j == skip_2) and ((i+skip_2) < len(operand_2)):
            if operand_2[j+skip_2] < operand_1[j]:
                j += skip_2
    return operand_1





def perform_and(operand_1,operand_2):
    """
    performs a boolean and operatioin
    """

    result_list = []
    if operand_1[0] == "0" or operand_2[0] == "0":
        return ["0"]
    i = j = 0
    skip_1 = int(math.sqrt(len(operand_1)))
    skip_2 = int(math.sqrt(len(operand_2)))
    while i<len(operand_1) and j<len(operand_2):
        if operand_1[i] == operand_2[j]:
            result_list.append(operand_1[i])
            i +=1
            j +=1
        elif int(operand_1[i]) < int(operand_2[j]):
            i +=1
        else:
            j +=1

        if (i == skip_1) and ((i+skip_1) < len(operand_1)):
            if operand_1[i+skip_1] < operand_2[j]:
                i += skip_1
        if (j == skip_2) and ((i+skip_2) < len(operand_2)):
            if operand_2[j+skip_2] < operand_1[j]:
                j += skip_2
    
    return result_list


def perform_or(operand_1,operand_2):
    """
    performs a boolean or operation
    """
    i = j = 0

    while i < len(operand_1) and j < len(operand_2):
        if operand_1[i] != operand_2[j]:
            if operand_2[j] < operand_1[i]:
                operand_1.insert(i, operand_2[j])
                j +=1
            else:
                while (operand_2[j] > operand_1[i]):
                    j+=1
                if (operand_2[j] != operand_1[i]):
                    operand_1.insert(i, operand_2[j])
        i+=1
        j+=1
    return operand_1

                

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
            token = stemmer.stem(token).lower()
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