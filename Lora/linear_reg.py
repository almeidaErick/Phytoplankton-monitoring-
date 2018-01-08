# linear regression script for 

# import numpy library and matplot
from numpy import *
import matplotlib.pyplot as plt

# here is to be placed a script that
# either loads the data from a file created by another script
# or does the calibrations with the helpf of pushbutton


# generate data
# independent axis is concentration of chlorophyll in sample c
# dependent axis is fluorescence f
# measure begins with absorbance a
# 5 trials
l = 1		# cm
e470 = 907	# M/cm (DMF not water)

a = array([0, 0.353, 0.699, 0.846, 1.461])	# absorbance
c = a/(1.0*l*e470)			# abs/(cm*M/cm) = abs/M
f = array([949, 2796, 3526, 4284, 4979])	# intensity/photon count
# intensity/photocount irrelevant units as long as consistent measurement
# also requires 

# calculate the regression
x = 1.0*c 				# setting the values to use a ready made script
y = 1.0*f
e = 0.1*y			# 1% error
				# first approximation

n = len(x)
xbar = (1/n)*(sum(x))
ybar = (1/n)*(sum(y))
D = sum((x-xbar)**2)
m = (1/D)*sum(multiply((x-xbar), y))
c = ybar - m*xbar


# plot the regression
xlr = linspace(min(x), max(x), 100)
ylr = m*xlr + c

plt.plot(xlr, ylr)
plt.errorbar(x, y, e, fmt='o')
plt.title("Relationship between Flourescence and Concentration")
plt.xlabel("Concentration (Units)")		# Should probably get the units
plt.ylabel("Fluorescence (Units)")		# and do dimensional analysis to be sure
plt.show()					# that this makes sense

# print the regression values
print "f = %d*x + %d" % (m, c)
