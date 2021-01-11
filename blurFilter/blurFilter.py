# -*- coding: utf-8 -*-
"""
@author: Felipe Fitarelli
"""

import cv2, shutil, glob, math, copy, numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box
from PIL import Image, ImageFilter

dir_yolo_raw = 'Input/' #Pasta de entrada
dir_striped = '/Output' #Pasta de saída

files_yolo_raw = glob.glob(dir_yolo_raw+"/*/*.txt")
len_yolo_raw = len(files_yolo_raw)

classesTxt = np.genfromtxt('classes.txt',dtype='str')

count = 0
imagePercent = 0
oldImagePercent = 0

#Função que verifica se há interseção entre as bounding boxes
def hasIntersection(matrix, dh, dw, file_name):
    #Varre todos os objetos entre si
    for obj in range(len(matrix)):
        
        x1 = matrix[obj,1]
        y1 = matrix[obj,2]
        w1 = matrix[obj,3]
        h1 = matrix[obj,4]
        
        l1 = int((x1 - w1 / 2) * dw)
        r1 = int((x1 + w1 / 2) * dw)
        t1 = int((y1 - h1 / 2) * dh)
        b1 = int((y1 + h1 / 2) * dh)
        
        # shapely.geometry.box(minx, miny, maxx, maxy, ccw=True)
        box1 = box(l1, b1, r1, t1, ccw=True)
        
        for line in range(len(matrix)):
            if(not(line == obj)):
                x2 = matrix[line,1]
                y2 = matrix[line,2]
                w2 = matrix[line,3]
                h2 = matrix[line,4]
        
                l2 = int((x2 - w2 / 2) * dw)
                r2 = int((x2 + w2 / 2) * dw)
                t2 = int((y2 - h2 / 2) * dh)
                b2 = int((y2 + h2 / 2) * dh)
                
                box2 = box(l2, b2, r2, t2, ccw=True)
                
                if(box1.intersects(box2)):
                    print("Há interseção na imagem " + file_name + "! Objeto da linha " + str(obj) + " com objeto da linha " + str(line) + " ")
                    return True
                
    return False

#Varre todos os arquivos salvos nas pastas
for temp in range(len_yolo_raw):
    file_txt = files_yolo_raw[temp]
    file_jpg = file_txt[:-4] + ".jpg"
    
    #Adquire o nome de cada arquivo
    bars = 0
    for x in range(len(file_txt)):
        if(file_txt[x] == '\\'):
            bars += 1
        if(bars == 2):
            position_bar = x + 1
            break
    
    file_name = file_txt[position_bar:]
    file_name = file_name[:-4]
    
    #Lê o arquivo .txt
    matrix = np.loadtxt(file_txt, usecols=range(5))
    if (matrix.ndim == 1):
        matrix = matrix.reshape(1, 5)
    
    qtClasses = len(classesTxt)
    qtObj = len(matrix)
    classes = [[] for _ in range(qtClasses)]
    
    #Monta a matrix que agrupa os objetos de acordo com cada classe
    for pos in range(qtObj):
        if(matrix[pos,0] < qtClasses):
            classes[int(matrix[pos,0])].append(pos)
    
    #Quantidade de classes diferentes presentes no arquivo .txt
    qtClassesInFile = len(list(filter(None,classes)))
    
    #img = cv2.imread(file_jpg)
    #dh, dw, _ = img.shape
    
    img = Image.open(file_jpg)
    dw, dh = img.size
    
    hadAlteration = False
    #Apenas faz alterações se há mais de uma classe e não há interseções entre as bounding boxes
    if(qtClassesInFile > 1 and not hasIntersection(matrix, dh, dw, file_name)):
        
        for pos1 in range(qtClasses):
            if(len(classes[pos1]) > 0):
                
                #Montagem do arquivo .txt de tags
                first = True
                lines = np.array([])
                for line in classes[pos1]:
                    if(first):
                        lines = np.append(lines, matrix[line])
                        lines = lines.reshape(1, 5)
                        first = False
                    else:
                        lines = np.vstack([lines, matrix[line]])
                        
                final_txt = "Output/" +  file_name + "-" + str(pos1) + ".txt"
                fmt = '%d', '%1.15f', '%1.15f', '%1.15f','%1.15f'
                np.savetxt(final_txt, lines, fmt=fmt)
                
                #Montagem da imagem .jpg
                modImg = copy.deepcopy(img)
                for pos2 in range(qtClasses):
                    if(len(classes[pos2]) > 0 and pos2 != pos1):
                        
                        for pos in classes[pos2]:
                            x = matrix[pos,1]
                            y = matrix[pos,2]
                            w = matrix[pos,3]
                            h = matrix[pos,4]
                            
                            # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
                            # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
                            l = int((x - w / 2) * dw)
                            r = int((x + w / 2) * dw)
                            t = int((y - h / 2) * dh)
                            b = int((y + h / 2) * dh)
                            
                            if l < 0:
                                l = 0
                            if r > dw - 1:
                                r = dw - 1
                            if t < 0:
                                t = 0
                            if b > dh - 1:
                                b = dh - 1
                        
                            #cv2.rectangle(modImg, (l, t), (r, b), (0, 0, 0), -1)
                            cropped_image = modImg.crop((l,t,r,b))
                            blurred_image = cropped_image.filter(ImageFilter.GaussianBlur(radius=7))
                            modImg.paste(blurred_image,(l,t,r,b))
                            hadAlteration = True
                            
                if(hadAlteration):
                    #plt.imshow(img)
                    #plt.show()
                            
                    final_image = "Output/" + file_name + "-" + str(pos1) + ".jpg"
                    #cv2.imwrite(final_image, modImg)
                    modImg.save(final_image)
                    hadAlteration = False
    else:
        shutil.copy(file_jpg, 'Output/')
        shutil.copy(file_txt, 'Output/')
        
    #Exibe o progresso de conversão
    count += 1
    imagePercent = math.trunc((count/len_yolo_raw)*100)
    if(imagePercent > oldImagePercent):
        print("Progresso: " + str(imagePercent) + "%")
        oldImagePercent = imagePercent
                
                
        
    

