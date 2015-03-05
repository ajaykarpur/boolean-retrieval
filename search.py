#!/usr/bin/python
import sys
import getopt
import pickle


the_dictionary ={}
boolean_precedence = {'OR':1,'AND':2,'NOT':3,'(':0}
opp_stack = []
output_stack = []
result_stack = []
#-------------------------------------------------------------------------------
   

def make_dict():
    """
    unpickels the dictionary.txt file to creat a python dictionary
    """
    with open(dict_filename, 'r') as f:
        the_dictionary = pickle.load(f)
    with open(post_filename,'r') as f:
        f.seek(the_dictionary["bill"][1])
        test_list = []
        test_list = f.readline().split()
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
    with open(queries_filename,'r') as f:
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
            # while output_stack:
            #     token = output_stack(0)
            #     if(token in boolean_precedence and token != 'NOT'):
            #         operand_1 = result_stack.pop()
            #         operand_2 = result_stack.pop()

                    #perform_query(opperand_1,opperand_2,token)



 

#def perform_query(operand_1,opperand_2,operator):
    """
    performs a boolean operatioin by looking up
    """



                

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

make_dict()
#make_queries()