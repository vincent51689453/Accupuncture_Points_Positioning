import numpy as np
import cv2
import linear_solver as linear
# LEFT HAND VERSION

HSV_image = None


def load_image():
	image_path = "./test_imgs/capture_5.jpg"
	img = cv2.imread(image_path)
	print("Image Dimensions: Height = {} and Widht = {} ".format(img.shape[0],img.shape[1]))
	return img


def input_AI_zoom(input_image):
	x_min = input("AI->left = ")
	x_max = input("AI->right = ")
	y_min = input("AI->top = ")
	y_max = input("AI->bottom = ")
	x_min = int(x_min)
	x_max = int(x_max)
	y_min = int(y_min)
	y_max = int(y_max)
	#x_min = 48
	#x_max = 976
	#y_min = 78
	#y_max = 554
	cv2.rectangle(input_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
	return x_min,y_min,x_max,y_max


def fit_forearm_alpha(input_image,x_min,y_min,y_max):
	hsv_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2HSV)
	#Get (y_min,x_min) HSV values
	#+20 is offset. Otherwise, it is detecting the rectangle box
	x_min = x_min+20
	y_min = y_min+10
	backup_y = y_min
	pixel = hsv_image[y_min,x_min]
	#print("Origin HSV:",pixel)
	#Starting moving to contours-ALPHA
	matched = False
	previous_H = int(pixel[0])
	previous_S = int(pixel[1])
	previous_V = int(pixel[2])
	while(matched==False):
		pixel = hsv_image[y_min,x_min]
		if(abs(previous_S - pixel[1])>30):
			matched = True
		if(abs(y_max-y_min)<20):
			#Prevent over shrinking
			y_min = backup_y
			matched = True
		y_min+=1
	cv2.putText(input_image,"Alpha",(x_min,y_min-20), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255,0,0), 1, cv2.LINE_AA)
	cv2.circle(input_image,(x_min,y_min),5,(255,0,0),-1)
	#cv2.imshow("Detector",input_image)
	return input_image,x_min,y_min


def fit_forearm_beta(input_image,x_min,y_min,y_max):
	hsv_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2HSV)
	#Get (y_max,x_min) HSV values
	#20 is offset. Otherwise, it is detecting the rectangle box
	x_min = x_min+20
	y_max = y_max-10
	backup_y = y_max
	pixel = hsv_image[y_max,x_min]
	#print("Origin HSV:",pixel)
	#Starting moving to contours-BETA
	matched = False
	previous_H = int(pixel[0])
	previous_S = int(pixel[1])
	previous_V = int(pixel[2])
	while(matched==False):
		pixel = hsv_image[y_max,x_min]
		if(abs(previous_S - pixel[1])>30):
			matched = True
		if(abs(y_max-y_min)<20):
			#Prevent overshrinking
			y_max = backup_y
			matched = True
		y_max-=1
	cv2.putText(input_image,"Beta",(x_min,y_max+30), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255,0,0), 1, cv2.LINE_AA)
	cv2.circle(input_image,(x_min,y_max),5,(255,0,0),-1)
	#cv2.imshow("Detector",input_image)
	return input_image,x_min,y_max

def fit_forearm_gamma(input_image,x_max,y_min,y_max):
	hsv_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2HSV)
	#Get (y_max,x_min) HSV values
	#20 is offset. Otherwise, it is detecting the rectangle box
	x_max = x_max-20
	y_min = y_min+10
	pixel = hsv_image[y_min,x_max]
	backup_y = y_min
	#print("Origin HSV:",pixel)
	#Starting moving to contours-GAMMAR
	matched = False
	previous_H = int(pixel[0])
	previous_S = int(pixel[1])
	previous_V = int(pixel[2])
	while(matched==False):
		pixel = hsv_image[y_min,x_max]
		#print("New HSV:",pixel)
		if(abs(previous_S - pixel[1])>30):
			matched = True
		if(abs(y_max-y_min)<20):
			#Prevent over shrinking
			y_min=backup_y
			matched = True
		y_min+=1
	cv2.putText(input_image,"Gamma",(x_max-60,y_min-30), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255,0,0), 1, cv2.LINE_AA)
	cv2.circle(input_image,(x_max,y_min),5,(255,0,0),-1)
	#cv2.imshow("Detector",input_image)
	return input_image,x_max,y_min

def fit_forearm_delta(input_image,x_max,y_min,y_max):
	hsv_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2HSV)
	#Get (y_max,x_min) HSV values
	#20 is offset. Otherwise, it is detecting the rectangle box
	x_max = x_max-20
	y_max = y_max-10
	backup_y = y_max
	pixel = hsv_image[y_max,x_max]
	#print("Origin HSV:",pixel)
	#Starting moving to contours-DELTA
	matched = False
	previous_H = int(pixel[0])
	previous_S = int(pixel[1])
	previous_V = int(pixel[2])
	while(matched==False):
		pixel = hsv_image[y_max,x_max]
		#print("New HSV:",pixel)
		if(abs(previous_S - pixel[1])>30):
			matched = True
		if(abs(y_max-y_min)<20):
			#Prevent overshrinking
			y_max = backup_y
			matched = True
		y_max-=1
	cv2.putText(input_image,"Delta",(x_max-60,y_max+30), cv2.FONT_HERSHEY_SIMPLEX,0.8, (255,0,0), 1, cv2.LINE_AA)
	cv2.circle(input_image,(x_max,y_max),5,(255,0,0),-1)
	#cv2.imshow("Detector",input_image)
	return input_image,x_max,y_max

	

def main():
	raw_image = load_image()
	x1,y1,x2,y2 = input_AI_zoom(raw_image)

	#Active shrinking 
	raw_image,alpha_x,alpha_y=fit_forearm_alpha(raw_image,x1,y1,y2)
	raw_image,beta_x,beta_y=fit_forearm_beta(raw_image,x1,y1,y2)
	raw_image,gamma_x,gamma_y=fit_forearm_gamma(raw_image,x2,y1,y2)
	raw_image,delta_x,delta_y=fit_forearm_delta(raw_image,x2,y1,y2)
	print("Acitve shrinking finished!")

	#Draw Trapezium for acupuncture points localization
	cv2.line(raw_image,(alpha_x,alpha_y),(beta_x,beta_y),(0, 0, 255),2)
	cv2.line(raw_image,(gamma_x,gamma_y),(delta_x,delta_y),(0, 0, 255),2)
	cv2.line(raw_image,(alpha_x,alpha_y),(gamma_x,gamma_y),(0, 0, 255),2)
	cv2.line(raw_image,(beta_x,beta_y),(delta_x,delta_y),(0, 0, 255),2)

	#Concurrent Ratio = 12
	mid_alpha_beta_x = int((alpha_x+beta_x)/2)
	mid_alpha_beta_y = int((alpha_y+beta_y)/2)
	mid_gamma_delta_x = int((gamma_x+delta_x)/2)
	mid_gamma_delta_y = int((gamma_y+delta_y)/2)
	#Horizontal Plane
	cv2.line(raw_image,(mid_alpha_beta_x,mid_alpha_beta_y),(mid_gamma_delta_x,mid_gamma_delta_y),(153,255,255),2)
	#Equation (y = mx + c)
	h_m,h_c = linear.linear_equation_solver(mid_alpha_beta_x,mid_alpha_beta_y,mid_gamma_delta_x,mid_gamma_delta_y)
	

	#+1/2 and -1/2 of horizontal plane
	mid_1 = int((mid_alpha_beta_y+alpha_y)/2)
	mid_1_end = int((mid_gamma_delta_y+gamma_y)/2)
	cv2.line(raw_image,(alpha_x,mid_1),(delta_x,mid_1_end),(153,255,255),2)
	#Equation (y = mx + c)
	h1_m,h1_c = linear.linear_equation_solver(alpha_x,mid_1,delta_x,mid_1_end)


	mid_2 = int((mid_alpha_beta_y+beta_y)/2)
	mid_2_end = int((mid_gamma_delta_y+delta_y)/2)
	cv2.line(raw_image,(alpha_x,mid_2),(delta_x,mid_2_end),(153,255,255),2)
	#Equation (y = mx + c)
	h2_m,h2_c = linear.linear_equation_solver(alpha_x,mid_2,delta_x,mid_2_end)

	ratio = 12
	i = 0
	distance = delta_x - alpha_x
	interval = int(distance/12)
	while(i<=12):
		x_shift = alpha_x+i*interval
		cv2.line(raw_image,(x_shift,alpha_y),(x_shift,beta_y+40),(255,255,0),2)
		#Acupuncture Positioning
		if(i == 0):
			midy = int((alpha_y+beta_y)/2)
			cv2.circle(raw_image,(x_shift,midy),5,(178,102,255),-1)
			cv2.putText(raw_image,"0",(x_shift+10,midy-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)
			
			cv2.circle(raw_image,(x_shift,mid_1),5,(178,102,255),-1)
			cv2.putText(raw_image,"2",(x_shift+10,mid_1-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)

			cv2.circle(raw_image,(x_shift,mid_2),5,(178,102,255),-1)
			cv2.putText(raw_image,"1",(x_shift+10,mid_2-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)

		if(i == 5):
			y = int(h1_m*x_shift+h1_c)
			cv2.circle(raw_image,(x_shift,y),5,(178,102,255),-1)
			cv2.putText(raw_image,"8",(x_shift+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)			
			
		if(i == 9):
			y = int(h_m*x_shift+h_c)
			cv2.circle(raw_image,(x_shift,y),5,(178,102,255),-1)
			cv2.putText(raw_image,"6",(x_shift+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)	

		if(i == 11):
			y = int(h1_m*x_shift+h1_c)
			cv2.circle(raw_image,(x_shift,y),5,(178,102,255),-1)
			cv2.putText(raw_image,"7",(x_shift+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)			

		if(i == 12):
			y = int(h1_m*x_shift+h1_c)
			cv2.circle(raw_image,(x_shift,y),5,(178,102,255),-1)
			cv2.putText(raw_image,"3",(x_shift+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)	
			y = int(h2_m*x_shift+h2_c)
			cv2.circle(raw_image,(x_shift,y),5,(178,102,255),-1)
			cv2.putText(raw_image,"4",(x_shift+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)		
			y = int(h_m*x_shift+h_c)
			cv2.circle(raw_image,(x_shift,y),5,(178,102,255),-1)
			cv2.putText(raw_image,"5",(x_shift+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(178,102,255), 1, cv2.LINE_AA)		

		i+=1
	

	cv2.imshow("Acupunture Points Detector[Forearm]",raw_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	


if __name__ == "__main__":
	main()


