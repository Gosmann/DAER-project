import cv2
import random
import string
from datetime import datetime
random.seed(datetime.now())

def random_name():
    name = ""
    for x in range(15):
        name = name+random.choice(string.ascii_letters + string.digits)
    #print (name)
    return name

vidcap = cv2.VideoCapture('ERS 030_10min.mp4')
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
target_number = 100
probability = target_number/length

print('Total number of frames: ', length )
print('Target number of frames: ', target_number )
print('Probability: ', probability )
print(random.random())
print(random.random())

success,image = vidcap.read()
count = 0

while success:
    chance = random.random()
    
    if(chance <= probability):
        print(str(count)+" "+str(chance)+" "+str(probability)+"!!!")
        cv2.imwrite("frames/"+random_name()+".jpg", image)     # save frame as JPEG file      
    else:
        print(str(count)+" "+str(chance)+" "+str(probability)
              )
    success,image = vidcap.read()  
    count += 1

print('Finished all! ')
