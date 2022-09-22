import matplotlib.pyplot as plt
import numpy as np
import math


point3posX = -37.5
point3posY = -64.951905283832899
point3posZ = 400

cos = math.acos(0)


def create_circle():
	circle = plt.Circle((0,0), radius= 75)
    
	return circle


def show_shape(patch):
	ax=plt.gca()
	ax.add_patch(patch)
	plt.axis('scaled')
	plt.show()

	
if __name__== '__main__':
	c = create_circle()

	line1_Xend = np.cos(np.deg2rad(0)) * 75
	line1_Yend = np.sin(np.deg2rad(0)) * 75

	line2_Xend = np.cos(np.deg2rad(120)) * 75
	line2_Yend = np.sin(np.deg2rad(120)) * 75

	line3_Xend = np.cos(np.deg2rad(240)) * 75
	line3_Yend = np.sin(np.deg2rad(240)) * 75
	plt.plot([[0,0,0],[line1_Xend,line2_Xend,line3_Xend]],[[0,0,0],[line1_Yend,line2_Yend,line3_Yend]],color="r",marker="o")
	for i in range(180):
		plt.cla()
		line1_Xend = np.cos(np.deg2rad(0 + i)) * 75
		line1_Yend = np.sin(np.deg2rad(0 + i)) * 75

		line2_Xend = np.cos(np.deg2rad(120 + i)) * 75
		line2_Yend = np.sin(np.deg2rad(120 + i)) * 75

		line3_Xend = np.cos(np.deg2rad(240 + i)) * 75
		line3_Yend = np.sin(np.deg2rad(240 + i)) * 75
		plt.plot([[0,0,0],[line1_Xend,line2_Xend,line3_Xend]],[[0,0,0],[line1_Yend,line2_Yend,line3_Yend]],color="r",marker="o")
		plt.pause(0.001)
	show_shape(c)
    # show_shape(a)


