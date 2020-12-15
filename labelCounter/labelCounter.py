# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 2020

@author: Felipe Fitarelli
"""
import os, re, copy, csv, math

dir_images = 'images\\' #Aqui pode-se trocar o nome da pasta das imagens
name_out_csv = 'saida' #Aqui pode-se trocar o nome do arquivo CSV de saída
dirname = os.getcwd()

class Classes:
    def __init__(self, name, ref_numb):
        self.name = name
        self.ref_numb = ref_numb
        self.qtde = 0

#Faz a leitura do arquivo de classes e salva a relação classe-número
f_classes = open("classes.txt", "r")

classesTot_dict={}
image_dict={}
reset_dict={}

#Monta os dicts necessários
i=0
for line in f_classes:
    reset_dict[line]=Classes(line,i)
    classesTot_dict[line]=Classes(line,i)
    i += 1

#Muda para a pasta onde há as pastas com todas as imagens e labels
dirImag = os.path.join(dirname, dir_images)
os.chdir(dirImag)

tags=0
#Salva todas as subpastas
folders = []
for root, direct, fil in os.walk(dirImag):
    for folder in direct:
        folders.append(folder)
    tags += len(fil)/2

lista=[]
finalList=[]
header=[]

#Criação do header do arquivo CSV
header.append("imageName")
for var in reset_dict:
    var = reset_dict.get(var)
    header.append(var.name.rstrip())
finalList.append(header)

imageCount = 0
objectsCount = 0
imagePercent = 0
oldImagePercent = 0
#Em cada uma das subpastas faz a contagem
for fol in folders:
    files = []
    
    dirFol = os.path.join(dirImag, fol + '\\')
    os.chdir(dirFol)
    
    #Identifica todos os arquivos .txt
    for root, direct, fil in os.walk(dirFol):
        for file in fil:
            if '.txt' in file:
                files.append(file)
    
    #Varre todos os aquivos .txt salvos
    for f in files:
        f_imag = open(f, "r")
        
        image_dict.clear()
        image_dict = copy.deepcopy(reset_dict)
        
        for line in f_imag:
            number = int(re.search(r'\d+', line).group())            
            for classe in classesTot_dict:
                classe = classesTot_dict.get(classe)
                classe_image = image_dict.get(classe.name)
                
                if classe.ref_numb == number:
                    classe.qtde += 1
                    classe_image.qtde += 1
                    objectsCount += 1
        
        #Monta um list com nome da imagem e quantidade de objetos de cada classe
        lista.clear()
        lista.append(f)
        
        for var in image_dict:
            var = image_dict.get(var)
            lista.append(var.qtde)
        finalList.append(copy.deepcopy(lista))
        
        f_imag.close()
        imageCount += 1
        
        #Exibe o progresso de conversão
        imagePercent = math.trunc((imageCount/tags)*100)
        if(imagePercent > oldImagePercent):
            print("Progresso: " + str(imagePercent) + "%")
            oldImagePercent = imagePercent

#Cria o arquivo final CSV
os.chdir(dirname)
with open(name_out_csv + '.csv', 'w', newline='') as outCSV:
    writer = csv.writer(outCSV)
    writer.writerows(finalList)
    
#IMPORTANTE: a variável classesTot_dict salva a quantidade total de objetos de cada classe, caso seja necessário!
f = open("quantidadeTotal.txt", "w")
f.write("====== TOTAL INFO ======\n")
f.write("Total images: " + str(imageCount) + "\n")
f.write("Total objects: " + str(objectsCount) + "\n\n")
f.write("====== TOTAL OBJECTS BY CLASS ======\n")
for obj in classesTot_dict:
    classe = classesTot_dict.get(obj)
    f.write(classe.name.rstrip() + ": " + str(classe.qtde) + "\n")

f.close()