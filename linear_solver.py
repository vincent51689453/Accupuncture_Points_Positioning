import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq



def linear_equation_solver(x_start,y_start,x_end,y_end):
	points = [(x_start,y_start),(x_end,y_end)]
	x_coords, y_coords = zip(*points)
	A = vstack([x_coords,ones(len(x_coords))]).T
	m, c = lstsq(A, y_coords)[0]
	#print("Line Solution is y = {m}x + {c}".format(m=m,c=c))
	return m,c

	
	
