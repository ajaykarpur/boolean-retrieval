def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

input_file_b = input_file_t = output_file = n = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:n:')
except:
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
        
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    elif o == '-n':
        n = int(a)
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)