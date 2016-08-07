#Gregory Kehne
#
#This program draws randomly generated lines that squiggle but maintain a roughly
#uniform distance from one another. This is inspired by the growth lines that 
#appear in the cross-sections of geodes, and by the work of artist Sol LeWitt, 
#specifically "Wall Drawing 797".

import math
import random
from PIL import Image, ImageDraw

#this is the squiggle generator!
#step<=gap
#i is the index of the line
#j is the 'height' index within the line
#lines[i][j]=(x-coord, y-coord)
def squiggles(height,width, step, gap):
	#array to contain all relevant points
	lines=[]
	#temp list to store the previous line
	line=[]
	#how far over the lines start
	seed=500

	#generate squiggly lines
	for i in range(0,width, gap):
		if i==0: #generate the original line
			rprev=0.0
			rprevprev=0.0
			rprevprevprev=0.0
			for j in range(0, height/step):
				randomness=random.uniform(-4,4)+random.uniform(-3,3)+random.uniform(-2,2)+.5*rprev+0.25*rprevprev+0.125*rprevprevprev
				line.append((seed+randomness, j*step))
				rprevprevprev=rprevprev
				rprevprev=rprev
				rprev=randomness
				seed=seed+randomness
		else: #generate derivative lines
			newline=[]
			for j in range(0, height/step):
				poss=[]	 #x-value candidates to choose from
				for d in range(-(gap/step)+1, gap/step):
					if j+d>=0 and j+d<height/step: #in y-range
						poss.append(line[j+d][0]+math.sqrt(gap**2 - (d*step)**2))
				newline.append((max(poss)+random.uniform(-0.5,0.5), j*step))

			line=newline	
		lines.append(line)
	return(lines)

#this is the runner method. 
#parameters are dimensions of screen, step within line, gap between lines, output file name
def draw(height, width, step, gap, name):
	#generate squiggles
	lines=squiggles(height,width, step, gap)
	#new image created
	im = Image.new('RGBA', (height, width), (255, 255, 255, 0)) 
	draw = ImageDraw.Draw(im) 
	#draw the lines
	#i iterates horizontally across lines
	for i in range(len(lines)):
		drift=i/len(lines) #make function that drifts from one color to the next. Maybe also have x/y drift? 
		#random line color
		color=(random.randint(int(0+drift*(130)),int(60+drift*100)), random.randint(int(100-(drift*(100-32))), int(190-drift*(190-32))), random.randint(210,220),0)
		#width for line
		w=random.randint(3,5)

		#draw all the individual segments. Here j steps down the vertical axis
		for j in range(len(lines[i])-1):
			draw.line((lines[i][j][0],lines[i][j][1],lines[i][j+1][0],lines[i][j+1][1]), fill=color, width=w)
	
	#these are the two choices for image output
	#im.show()
	im.save(name+".jpg")

#This creates an image 2000x2000 named geode_test.jpg with lines that take 4-pixel steps and sit 30 pixels apart.
draw(2000,2000, 4, 30,"geode_test")



