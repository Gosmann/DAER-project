# -*- coding: utf-8 -*-
"""
Esse script implementa o filtro com o aproach "ingênuo" de selecionar
classe por classe conforme o vetor rank
"""
import os, re, copy, csv, shutil
import glob, numpy as np


dir_yolo_raw = '1/' #Aqui pode-se trocar o nome da pasta das imagens
dir_filtered = '/1_filtered' #Aqui pode-se trocar o nome do arquivo CSV de saída

len_yolo_raw = len(glob.glob(dir_yolo_raw+"/*.txt"))
files_yolo_raw = glob.glob(dir_yolo_raw+"/*.txt")

#print(len_yolo_raw)
#print(files_yolo_raw[5])
#files_yolo_raw[5] = files_yolo_raw[5,5:10]

yolo_names = [[] for i in range(len_yolo_raw)]

yolo_selected = []

#CLASSES
# 0 -> CAR
# 1 -> TRUCK
# 2 -> BUS
# 3 -> MOTORCYCLE

goal_car = 215
goal_truck = 215
goal_bus = 215
goal_motorcycle = 215

goals = [goal_car, goal_truck, goal_bus, goal_motorcycle]

rank = [3,2,1,0]
state = 0

flag_found = 0
x = 0
while (x < len_yolo_raw):
    temp_string = files_yolo_raw[x]
    yolo_names[x] = temp_string[2:]
    #print (yolo_names[x])
    print (str(goals)+" "+str(x)+" "+yolo_names[x]+" "+str(len(yolo_selected)))

    matrix = np.loadtxt(dir_yolo_raw+yolo_names[x], usecols=range(5))
    #print(matrix.ndim)
    if (matrix.ndim == 1):
        matrix = matrix.reshape(1, 5)

    flag_found = 0
    for y in range (int(matrix.size/5)):
        if(flag_found == 0 and not(yolo_names[x] in yolo_selected)  ):
            #print(int(matrix.size/5))
            if(matrix[y, 0] == rank[state]):  #found motorcycle
                
                for y in range (int(matrix.size/5)):
                    goals[int(matrix[y][0])] -= 1
                    
                if(goals[int(matrix[y][0])] < 0):
                    for y in range (int(matrix.size/5)):
                        goals[int(matrix[y][0])] += 1
                else:
                    flag_found = 1
                    yolo_selected.append(yolo_names[x])
                    
                
    if ( all ( i == 0 for i in goals ) ):
        print("************************************")
        print("TODOS OBJETOS RECOLHIDOS COM SUCESSO")
        print("************************************")
        yolo_selected.append(yolo_names[x])
        print (str(goals)+" "+str(x)+" "+yolo_names[x]+" "+str(len(yolo_selected)))
        break

    if(goals[rank[state]] <= 0):   
        if(state == 0):  
            print("************************************")
            print("!!!! OBJETIVO DE MOTOS CONLUIDO !!!!")
            print("************************************")
            state = 1
            x=0
        elif(state == 1):
            print("************************************")
            print("!!!! OBJETIVO DE ONIBUS CONLUIDO !!!")
            print("************************************")
            state = 2
            x=0
        elif(state == 2):
            print("************************************")
            print("!! OBJETIVO DE CAMINHAO CONLUIDO !!!")
            print("************************************")
            state = 3
            x=0
        elif(state == 3):
            print("************************************")
            print("!!! OBJETIVO DE CARROS CONLUIDO !!!!")
            print("************************************")
            print (str(goals)+" "+str(x)+" "+yolo_names[x]+" "+str(len(yolo_selected)))
            break
            state = 4
            x=0            

    x += 1
    #elif ( all ( i >= 0 for i in goals ) ):    # verifica se todos são maiores que zero
    #elif (goals[3] >= 0):
        #yolo_selected.append(yolo_names[x])
                  
    #elif ():
    #    for y in range (int(matrix.size/5)):
    #        goals[int(matrix[y,0])] += 1

for x in range (len(yolo_selected)):
    yolo_jpg = yolo_selected[x]
    yolo_jpg = yolo_jpg[:-4] 
    #print(yolo_jpg)
    #print (yolo_selected[x])    
    # target filename is /dst/dir/file.ext
    shutil.copy('1/'+yolo_selected[x], '1_filtered/')
    shutil.copy('1/'+yolo_jpg+'.jpg', '1_filtered/') 

        







