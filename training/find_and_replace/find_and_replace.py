import glob

print (glob.glob("*.txt"))  # Returns a list of all .txt files, with path info

for item in glob.glob("*.txt"):
    temp = []  # Might be useful to use a temp list before overwriting your file
    with open(item, "r") as f:
        for line in f:
            temp.append(line)
                
    print (str(len(temp))+" "+str(temp)+" "+str(item) )  # Do something useful here        

    x=0
    y=len(temp)
    
    while(x < y):
        if(temp[x][0] == '0'):
            temp[x] = '2'+temp[x][1:]
        elif(temp[x][0] == '1'):
            temp[x] = '7'+temp[x][1:]
        elif(temp[x][0] == '2'):
            temp[x] = '5'+temp[x][1:]
        elif(temp[x][0] == '3'):
            temp[x] = '3'+temp[x][1:]
                                        
        x+=1

    print(str(len(temp))+" "+str(temp)+" "+str(item) )
                    
    with open(item, "w") as f:
        f.writelines(temp)
