import cv2
import numpy as np
import matplotlib.pyplot as plt

def mediaMovel(vetor):
    vet = np.copy(vetor)
    somatorio = 0
    diferenca = 0
    amostra   = 0
    thresholdDaDiferenca = 2
    for i in range(len(vet)):
        if len(vet) <2: return vet[0]
        if i == 0:
            diferenca = vet[i] - vet[i+1]
            if diferenca > thresholdDaDiferenca:
                vet[i] = (vet[i+1] + vet[i+2])/2
        elif (0 < i) and (i < (len(vet)-1)):
            diferenca = vet[i] - vet[i-1]
            if diferenca > thresholdDaDiferenca:
                vet[i] = (vet[i-1] + vet[i+1])/2
        elif i == (len(vet) - 1):
            diferenca = vet[i] - vet[i-1]
            if diferenca > thresholdDaDiferenca:
                vet[i] = (vet[i-2] + vet[i-1])/2
        somatorio = somatorio + vet[i]
    return somatorio/len(vet)

def filtro(vetor, pos, amostras):
    vetorFiltrado = 0.
    if pos < amostras:
        vetorFiltrado = mediaMovel(vetor[0:pos+1])
    else:
        vetorFiltrado = mediaMovel(vetor[pos-amostras+1:pos+1])
    return vetorFiltrado

def tratamento(img):
    k1 = np.ones((3,3),dtype=np.uint8)/9
    k2 = np.ones((4,4),dtype=np.uint8)
    k3 = np.ones((5,5),dtype=np.uint8)
    imgOrig = img
    img = cv2.filter2D(img, -1, k1)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, k2)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    img = cv2.dilate(img, k3, iterations = 3)
    img = cv2.bitwise_and(imgOrig, img)
    img = cv2.dilate(img, k3)
    return img

def criaBoundingBox(img):
    THRESHOLD_DA_AREA = 500
    contornos = \
        cv2.findContours(tratado, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    for contorno in contornos:
      (x, y, w, h) = cv2.boundingRect(contorno)
      if cv2.contourArea(contorno) > THRESHOLD_DA_AREA:
          cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    return img
    
    
N_AMOSTRAS_MM = 10  #numero de amostras da media movel
THRESHOLD  = 2  #limiar do movimento para salvar os frames
video      = cv2.VideoCapture("motion_detection_test/0HDJPJO1.mp4")
largura    = video.get(cv2.CAP_PROP_FRAME_WIDTH)
altura     = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
pixeisVert = int(altura * 0.9)

numeroDeFrames     = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

mediaDaDif  = np.zeros(numeroDeFrames)
DifFiltrada = np.zeros(numeroDeFrames)

backGND = cv2.bgsegm.createBackgroundSubtractorMOG()

for i in range(numeroDeFrames):
    frame = video.read()[1][0:pixeisVert]
    mog = backGND.apply(frame)
    tratado = tratamento(mog)
    mediaDaDif[i] = np.log10(np.mean(tratado) + 1)
    DifFiltrada[i] = filtro(mediaDaDif, i, N_AMOSTRAS_MM)
    criaBoundingBox(frame)
    cv2.imshow('VIDEO', frame)
    if cv2.waitKey(1) & 0xFF == ord('p'): 
        while True:
            if cv2.waitKey(1) & 0xFF == ord('d'): 
                break
    if cv2.waitKey(1) & 0xFF == ord('q'): break
    # if i > (N_AMOSTRAS_MM - 1):
    #     media[i - (N_AMOSTRAS_MM - 1)] = np.mean(mediaMovel)
    #     if media[i - (N_AMOSTRAS_MM - 1)] > THRESHOLD:
    #         print(str(i))
    #         cv2.imwrite('frames/'+str(i)+'.jpg', frameNovo)

video.release()
cv2.destroyAllWindows()
plt.ylim(0, 1)
plt.plot(DifFiltrada)