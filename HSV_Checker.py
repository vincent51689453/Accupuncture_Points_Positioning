import numpy as np
import cv2

HSV_image = None

def load_image():
	image_path = "./test_imgs/capture_3.jpg"
	img = cv2.imread(image_path)
	print("Image Dimensions: Height = {} and Widht = {} ".format(img.shape[0],img.shape[1]))
	return img

def color_info(event,x,y,flag,param):
	global HSV_image
	if event == cv2.EVENT_LBUTTONDOWN:  #When Left is clicked in the mouse
		pixel = HSV_image[y,x]
		upper_limit = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
		lower_limit = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
		print("HSV Pixel:",pixel)
		print("Lower_Limit: ",lower_limit)
		print("Upper_Limit: ",upper_limit)
		print('\n')
		#Display the masking result of the threshold value
		image_mask = cv2.inRange(HSV_image,lower_limit,upper_limit)
		cv2.imshow("Mask",image_mask)

def masking(input_image):
	global HSV_image
	#Taking the mid point of the image to mask the forearm in HSV space
	mid_x = int(input_image.shape[1]/2)
	mid_y = int(input_image.shape[0]/2)
	print("Masking sampling coorindates: ({},{})".format(mid_x,mid_y))
	HSV_image = cv2.cvtColor(input_image,cv2.COLOR_BGR2HSV)
	#Mouse Picker to improve masking
	cv2.namedWindow('HSV_Picker')                  
	cv2.imshow("HSV_Picker",HSV_image)             
	cv2.setMouseCallback('HSV_Picker',color_info)  


def main():
	raw_image = load_image()
	masking(raw_image)

	cv2.waitKey(0)
	cv2.destroyAllWindows()
	


if __name__ == "__main__":
	main()


