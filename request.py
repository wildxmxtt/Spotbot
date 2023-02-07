import random
file = open("playlist.txt", "r") #Opens the playlist.txt file 
count = 0
for line in file:
    print(line)
    count +=1

requestNum = random.randint(0,count-1)
print("number generated: " + str(requestNum))
with open("playlist.txt", 'r') as fp:
    # lines to read
    line_numbers = [requestNum, count]
    # To store lines
    lines = []
    for i, line in enumerate(fp):
        # read from line 0 and the len of the text file
        if i in line_numbers:
            lines.append(line.strip())
        elif i > count:
            # don't read after line 7 to save time
            break
pre = str(lines)[1:-1] #removes square bracket
print(pre[1:-1]) #removes '' from front and back of the text 