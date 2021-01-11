# -*- coding: utf-8 -*-
"""
Esse script tem o objetivo de separar 1 classe de um conjunto de arquivos
"misturados" substituindo o background por 
"""
import os, re, copy, csv, shutil, cv2 as cv
import glob, numpy as np


dir_yolo_raw = '1/' #Aqui pode-se trocar o nome da pasta das imagens
dir_filtered = '/1_filtered' #Aqui pode-se trocar o nome do arquivo CSV de saída

len_yolo_raw = len(glob.glob(dir_yolo_raw+"/*.txt"))
files_yolo_raw = glob.glob(dir_yolo_raw+"/*.txt")

#print(len_yolo_raw)
#print(files_yolo_raw[0])
#files_yolo_raw[5] = files_yolo_raw[5,5:10]

yolo_names = [[] for i in range(len_yolo_raw)]

yolo_selected = []

#CLASSES
# 0 -> CAR
# 1 -> TRUCK
# 2 -> BUS
# 3 -> MOTORCYCLE
target_class = 0

files = 0
margin_x = 2
margin_y = 2

print(len_yolo_raw)
      
while(files < len_yolo_raw):
    
    temp_string = files_yolo_raw[files]
    yolo_names[files] = temp_string[2:-4]
    print (yolo_names[files])

    img = cv.imread('1/'+str(yolo_names[files])+'.jpg')
    height, width, channels = img.shape
    #cv.imshow("Display window", img)
    
    temp_string = files_yolo_raw[files]
    yolo_names[files] = temp_string[2:]
    matrix = np.loadtxt(dir_yolo_raw+yolo_names[files], usecols=range(5))
    if (matrix.ndim == 1):
        matrix = matrix.reshape(1, 5)

    img2 = np.zeros((height, width, 3), np.uint8)
    found_class = 0

    #percorre um arquivos txt buscando a classe específica
    
    for z in range (int(matrix.size/5)):
        if(matrix[z,0] == target_class): #found specific class
            found_class+=1
            coords = [0,0,0,0]
            coords[0] = int((matrix[z,1]-matrix[z,3]*0.5)*width)   #posicao em x esquerda
            coords[1] = int((matrix[z,1]+matrix[z,3]*0.5)*width)   #posicao em x direita
            coords[2]= int((matrix[z,2]-matrix[z,4]*0.5)*height)   #posicao em y acima
            coords[3] = int((matrix[z,2]+matrix[z,4]*0.5)*height)  #posicao em y abaixo
            #print(str(coord1)+" "+str(coord2)+" "+str(coord3)+" "+str(coord4))
                                            
            for y in range(coords[3]-coords[2] + margin_y*2):
                for x in range(coords[1]-coords[0] + margin_x*2):
                    if(coords[2]+y-margin_y < 0 or coords[2]+y-margin_y >= height):
                        break
                    elif(coords[0]+x-margin_x < 0 or coords[0]+x-margin_x >= width):
                        break
                    else:
                        img2[coords[2]+y-margin_y, coords[0]+x-margin_x] = img[coords[2]+y-margin_y, coords[0]+x-margin_x]

            
            # salva os arquivos txt
                # ajusta questoes de nome
            temp_string = files_yolo_raw[files]
            yolo_names[files] = temp_string[2:-4]

            if(found_class == 1):
                f = open('1_filtered/'+yolo_names[files]+'-'+str(target_class)+'.txt', "w")
                f.write(str(int(matrix[z,0]))+' '+str(matrix[z,1])+' '+str(matrix[z,2])+' '+str(matrix[z,3])+' '+str(matrix[z,4])+'\n')
                f.close()
            else:
                f = open('1_filtered/'+yolo_names[files]+'-'+str(target_class)+'.txt', "a")
                f.write(str(int(matrix[z,0]))+' '+str(matrix[z,1])+' '+str(matrix[z,2])+' '+str(matrix[z,3])+' '+str(matrix[z,4])+'\n')
                f.close()                

    #salva as imagens finais
    if(found_class != 0):
        temp_string = files_yolo_raw[files]
        yolo_names[files] = temp_string[2:-4]
        cv.imwrite('1_filtered/'+str(yolo_names[files])+'-'+str(target_class)+'.jpg', img2)                        

    #incrementa o contador dos arquivos percorridos
    files += 1

        








