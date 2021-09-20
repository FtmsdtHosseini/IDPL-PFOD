#requirement library
from bidi.algorithm import get_display
from skimage.util import random_noise
from PIL import Image,ImageFilter
from PIL import ImageDraw
from PIL import ImageFont
from PIL import features
import arabic_reshaper
import pandas as pd
from cv2 import cv2
import numpy as np
import random
import glob
import csv
import re
import os

#import modules
import items
import textGen_White_Noisy
import textGen_Texture

pics = glob.glob("pic/*.png")
fonts = glob.glob("fonts/*.ttf")
source = "main_text.txt"
text = open(source, 'r')
lines = text.readlines()

#--------------------------------------------------------------------------------------------------------
randlist = []
for i in range(1,len(lines)+1):
	randlist.append(i)
random.shuffle(randlist)

infolist = []
count = 1
for i in range(len(lines)):
	try:
		line=lines[i]
		name = str(count) 
		name = (5 - len(name)) * "0" + name
		font = random.choice(fonts)
		pic = random.choice(pics)
		size_text = random.choice([10,11,12,13,14,15,16])
		noise = random.choice(['gaussian','s&p','poisson','speckle'])
		rand = randlist[i]
		func, rotate, distorsion, blur, flag = items.choice(rand)
		count += 1
		
		if func == 'White Noisy' and (distorsion == 'None' or distorsion == 'slope') :
			picture = textGen_White_Noisy.textGen_W_N_rot(line, font, rotate, size_text, blur, noise, flag)
			cv2.imwrite("out/" + name + ".tif", picture)
				
		elif func == 'White Noisy' and distorsion == 'sin wave' :
			picture = textGen_White_Noisy.textGen_W_N_sin(line, font, size_text, blur, noise, flag)
			cv2.imwrite("out/" + name + ".tif", picture)
					
		elif func == 'Texture' and (distorsion == 'None' or distorsion == 'slope') :
			picture = textGen_Texture.textGen_T_rot(line, font, rotate, size_text, pic, blur)
			cv2.imwrite("out/" + name + ".tif", picture)
			
		elif func == 'Texture' and distorsion == 'sin wave' :
			picture = textGen_Texture.textGen_T_sin(line, font, size_text, pic, blur)
			cv2.imwrite("out/" + name + ".tif", picture)
#--------------------------------------------------------------------------------------------------------		
		if func == 'White Noisy' and flag == 1 :
			backgroung = 'Noisy' + '(' + noise + ')'

		elif func == 'White Noisy' and flag == 0 :
			backgroung = 'Plain white'
		else :
			backgroung = 'Texture'
	
		if distorsion == 'slope':
			distorsion = 'slope with angle' + str(rotate)
#--------------------------------------------------------------------------------------------------------
		infolist.append([name, func, font[6:-5], size_text, distorsion, blur, line])	
#--------------------------------------------------------------------------------------------------------	
		print(i, 'Done!')	
	except Exception as e:
		print(e)
#--------------------------------------------------------------------------------------------------------
with open('INFO.csv', 'a') as csvfile:
			writer = csv.writer(csvfile)

			for item in infolist:
				writer.writerow(item)
				
df = pd.read_csv("INFO.csv", header=None)
df.to_csv("INFO.csv", header=['Name of Image', 'kind of func', 'kind of Font', 'kind of Font size', 'kind of distorsion', 'kind of Blur', 'true text'], index=False)
