#
# Creates nicely colored tex code out of a python program.
#
# (c) Jakob Fredslund 2005 jakobf@birc.au.dk
#
# v5.0: Splits the box after each 39 lines.
# v4.0: Can process itself now, though it doesn't split the box
#       if the program is too long to fit on one page :/
# v1.0: Has some trouble with \'es (gives bad tex when run on itself).

# Uses latex packages lineno and color, put this in your main tex file:
#
#   \usepackage[usenames]{color}
#   \usepackage{lineno}

# Also put color defs like this in your main tex file (you can change
# the coloring by altering these definitions):
#
#   \definecolor{kwcol}{rgb}{0.36,0.50,1.00}
#   \definecolor{pencol}{rgb}{0.00,0.00,0.00}
#   \definecolor{commentcol}{rgb}{1.00,0.00,0.00}
#   \definecolor{stringcol}{rgb}{1.00,0.68,0.33}
#   \definecolor{functioncol}{rgb}{0.11,0.66,0.00}
#   \definecolor{classcol}{rgb}{0.90,0.07,0.90}
#
# (Color definitions needed:
#    kwcol, stringcol, commentcol, and pencol
# respectively the keyword color, string color, comment color and color
# for anything else).


import sys
import re
from os.path import splitext

if len(sys.argv) != 2:
    print "Usage: python python2tex.py <python program file>"
    print "The program then creates a file with the same name and"
    print "extension .tex (replacing any other suffixes)."
    
    sys.exit(0)
    

linebreak = 57 # break lines after this many characters (-1)
linedist = 1   # line distance (in millimeters)

# keywords (put space after the short ones if they must be followed by something
# to avoid replacing substrings of non-keywords):
kw = ['accept', 'and', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'yield']





def breaklines(s, buf):
    # add newlines in s after each linebreak characters. First linebreak
    # should be inserted at index (linebreak-buf)
    
    i = 0
    c = ''
    
    # while more linebreaks should be added:
    while i+linebreak-buf < len(s):    
        # there may be line break markers in string already..
        nl = s.find("G9f%s,.D2g3"%'g', buf)
        if nl > -1 and nl-buf < linebreak:
                c += s[i:nl+10]
                i = nl+10
        else:
            c += s[i:i+linebreak-buf] + '\n\n'
            i += (linebreak-buf)
        buf = 0
    return c + s[i:]

def escape(s):
    # don't change the order..:
    s = s.replace("$", "GF=D%s__F__d"%"q")
    s = s.replace("\\", "$\\backslash$")
    s = s.replace("GF=D%s__F__d"%"q", "\$") # grr, self-referentiality is a bitch
    s = s.replace('#', '\#')
    s = s.replace('&', '\&')
    s = s.replace('_', '\_')
    s = s.replace('^', '$^\wedge$')
    #s = s.replace('@', '$@$')
    s = s.replace('{', '\{')
    s = s.replace('}', '\}')
    return s    

space = re.compile(" +")
qwqw = re.compile("QWQW\d+QWQW")
fj83 = re.compile("fj83\d+FFhb")
comm = re.compile("#.*")
classname = re.compile("class +(\w+) *:")
functionname = re.compile("def +(\w+) *\(")


# longest first:
ping = [ re.compile(r"[^\\]'''.*?[^\\]'''"),
         re.compile(r"[^\\]''.*?[^\\]''"),
         re.compile(r"[^\\]'.*?[^\\]'"),
         re.compile(r'[^\\]""".*?[^\\]"""'),
         re.compile(r'[^\\]".*?[^\\]"') ]


fin = open(sys.argv[1])
foutname = splitext(sys.argv[1])[0]+'.tex'
fout = open(foutname, 'w')

print >> fout, "\\colorbox{codebg}{\\internallinenumbers \\resetlinenumber \\begin{minipage}[r]{\\textwidth}\\begin{tt}"


wholetext = fin.read()
fin.close()





wholetext = wholetext.replace("\n", "G9f%s,.D2g3"%'g')



# non-empty strings and comments:

i = 0
count = 0
dic = {}
copy = ''
previousls = 0 # previous line start

while i<len(wholetext):
    pings = ["'''", "'", '"""', '"','#' ] # longest first
    nextp = None
    nexti = 9999999999999999999
    for pp in pings:
        index = wholetext.find(pp, i)
        if index > -1 and index < nexti: # true <, not leq (important)!
            nextp = pp
            nexti = index
    if not nextp:
        break  # no strings or comments found in remainder of text


    # find index of most recent newline (and line start):
    lb = wholetext[:nexti].rfind("G9f%s,.D2g3"%'g')
    if lb != -1:
        previousls = lb + 10 # the marker has length 10
    else:
        previousls = 0


    # okay: next delimiter is nextp, found in index nexti.
    
    if nextp == '#':  # next delimiter is a comment symbol
        lasti = wholetext.find("G9f%s,.D2g3"%'g', nexti+1)
        if lasti == -1:
            # comment extends through the remainder of the program
            lasti = len(wholetext)-1
        s = escape(wholetext[nexti:lasti])
        print "COMMENT:",s
        copy += wholetext[i:nexti] + "fj83%dFFhb"%count

        s = breaklines(s, nexti - previousls)
        
        dic[count] = "\color{commentcol}%s\color{pencol}"%s
        count += 1
        i = lasti # keep all of the found newline marker
        
    else:
        # Next delimiter is a string ping:
        lennextp = len(nextp)
        lasti = wholetext.find(nextp, nexti+lennextp)
        if lasti == -1:
            sys.exit("Program contains illegal string definition: %s"%wholetext[nexti:])
        while wholetext[lasti-1] == '\\' and wholetext[lasti-2] != '\\':
            lasti = wholetext.find(nextp, lasti+1)
            if lasti == -1:
                sys.exit("Program contains illegal string definition: %s"%wholetext[nexti:])
    
        # Here's a string: wholetext[nexti:lasti+len(pp)]
        s = escape(wholetext[nexti:lasti+lennextp])
        print "STRING:",s

        
        s = breaklines(s, nexti - previousls)
        
        # spaces: # July 7th 2005 ----
        spaces = space.findall(s)
        for spaceblock in spaces:
            lsp = len(spaceblock)
            s = s.replace(spaceblock, "\hspace{%.2fpt}"%((6.6*lsp)), 1)
        # ----|

        
        copy += wholetext[i:nexti] + "QWQW%dQWQW"%count
        dic[count] ="\color{stringcol}%s\color{pencol}"%s
        count += 1
        i = lasti+lennextp

    
    
copy += wholetext[i:]
wholetext = copy

        

# Handle empty strings (disregard sick cases like '''''' and """""").
# - Has to be done after the non-empty strings have been cut out:
for m in ["''", '""']:
    wholetext = wholetext.replace(m, "\color{stringcol}%s\color{pencol}"%m)
       

filelines = wholetext.split("G9f%s,.D2g3"%'g')

linecount = 0
for l in filelines:
    linecount+=1
    if linecount >=39:
        print >> fout, "\end{tt}\end{minipage}}"
        print >> fout, "\\colorbox{codebg}{\\internallinenumbers  \\begin{minipage}[r]{\\textwidth}\\begin{tt}"
        linecount = 0

        
    if l.isspace() or not l:
        print >> fout, r"\vspace{2ex}"
        continue
    
    # function and class names:
    classdef = classname.search(l)
    if classdef:
        l = l.replace(classdef.group(1), "\color{classcol}%s\color{pencol}"%classdef.group(1))

    functiondef = functionname.search(l)
    if functiondef:
        l = l.replace(functiondef.group(1), "\color{functioncol}%s\color{pencol}"%functiondef.group(1))

        
    # newlines:
    l = l.expandtabs() + "\n\n" #.replace("\n", "\n\n")

    # underscores:
    l = l.replace("_", "\_")

    # tabs:
    l = l.replace("\\t", "$\backslash$t").replace(r"\t", "$\backslash$t")

    line = l

    # keywords:
    for w in kw:
        lc = ""
        si = 0
        lenw = len(w)
        lenline = len(line)
        while si<len(line):
            wi = line.find(w, si)
            if wi == -1:
                lc += line[si:]
                break

            if wi != 0 and wi+lenw < lenline:
                # found but not in either end

                if line[wi-1].isspace() and line[wi+lenw].isspace():
                    lc += line[si:wi] + "\color{kwcol}" + w + "\color{pencol}"
                else:
                    lc += line[si:wi+lenw]
                

            elif wi != 0:
                # found at far right end:
                if line[wi-1].isspace():
                    lc += line[si:wi] + "\color{kwcol}" + w + "\color{pencol}"
                else:
                    lc += line[si:wi+lenw]
                

            elif wi+lenw < lenline:
                # found at far left end:
                if line[wi+lenw].isspace():
                    lc += line[si:wi] + "\color{kwcol}" + w + "\color{pencol}"
                else:
                    lc += line[si:wi+lenw]
                
            else:
                # line consists of this keyword only?!
                lc = line.replace(w, "\color{kwcol}%s\color{pencol}"%w)
            si = wi+lenw
        else:
            lc += line[si:]
        line = lc

        
        
        #line = line.replace(w, "\color{kwcol}%s\color{pencol}"%w)
    
    # spaces:
    spaces = space.findall(line)
    for spaceblock in spaces:
        line = line.replace(spaceblock, "\hspace{%.2fpt}"%((6.6*len(spaceblock))), 1)


    # now put strings back in:
    qwqws = qwqw.findall(line)
    for qw in qwqws:
        line = line.replace(qw, dic[int(qw[4:-4])])
        line = line.replace("G9f%s,.D2g3"%'g', "\n\n")

    # now put comments back in:
    fj83s = fj83.findall(line)
    for qw in fj83s:
        line = line.replace(qw, dic[int(qw[4:-4])])
        
    line = line.replace("%", "\%")

    print >> fout, line

print >> fout, "\end{tt}\end{minipage}}"
print "Created file",foutname
fout.close()
