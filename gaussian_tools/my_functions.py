
#Def functions to extract the data

def last_find(text,target):
    linenum = 0
    for line in text:
        if (line.find(target)) > -1 :
            last_line = linenum
        linenum += 1
    return last_line

def first_find(text,target):
   linenum = 0
   found = False
   for line in text:
      if not found:
        if (line.find(target)) > -1:
          found = True
        else:
          linenum += 1
   return linenum
