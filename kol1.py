###Flight simulator. 
#Write a code in python that simulates the tilt correction of the plane (angle between plane wings and earth). 
##The program should:
# - print out current orientation
# - applied tilt correction
# - run in infinite loop
# - until user breaks the loop
#Assume that plane orientation in every new simulation step is random angle with gaussian distribution (the planes is experiencing "turbulations"). 
#With every simulation step the orentation should be corrected, applied and printed out.
#If you can thing of any other features, you can add them.
#This code shoud be runnable with 'python kol1.py'.
#If you have spare time you can implement: Command Line Interface, generators, or even multiprocessing.
#Do your best, show off with good, clean, well structured code - this is more important than number of features.
#After you finish, be sure to UPLOAD this (add, commit, push) to the remote repository.
#Good Luck
import random
import time
import math

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    ENDC = '\033[0m'


class Aircraft:
	
	def __init__(self):
		self.speed = None
		self.orientation = None
		self.direction = None
		
	def gaussian_random(self, mean_and_standard_dev):
		return random.gauss(mean_and_standard_dev[0], mean_and_standard_dev[1])
		
	def set_aircraft_properties(self):
		self.speed = self.gaussian_random((700, 100/3))
		self.orientation = self.gaussian_random((10, 10/3))
		self.direction = self.gaussian_random((180, 100/3))

	def tilt_correction(self, desired_orientation):
		tilt_step = (self.orientation - desired_orientation) / 10
		
		while math.fabs(self.orientation - desired_orientation) > math.fabs(tilt_step):
			self.orientation = self.orientation - tilt_step
			time.sleep(0.5)
			print bcolors.WARNING + """
			FLT ORI: {0:10.2f}""".format(self.orientation) + bcolors.ENDC
			
		print bcolors.OKGREEN + """
		FLT ORI: {0:10.2f}""".format(self.orientation) + bcolors.ENDC
		self.aircraft_console()
			
		
		
	def direction_correction(self, desired_direction):
		correction_step = (self.direction - desired_direction) / 10
		
		while math.fabs(self.direction - desired_direction) > math.fabs(correction_step):
			self.direction= self.direction - correction_step
			time.sleep(0.5)
			print bcolors.WARNING + """
			FLT DIR: {0:10.2f}""".format(self.direction) + bcolors.ENDC
			
		print bcolors.OKGREEN + """
		FLT DIR: {0:10.2f}""".format(self.direction) + bcolors.ENDC
		self.aircraft_console()
		
		
	def aircraft_console(self):
		print """
		SPEED: {0:10.2f} km/h
		FLT DIR: {1:10.2f}
		FLT ORI: {2:10.2f}""".format(self.speed, self.direction, self.orientation)
		
	
class Gust:

	gust_vertical_directions = (('upward', 1), ('down', -1))
	gust_horizontal_directions = (('left', 1), ('right', -1))
	mean_and_standard_dev = (200, 10/3)

	def rand_gust_direction(self):
		return random.randint(0,len(self.gust_vertical_directions)-1)
		
	def rand_vertical_gust_for_turbulations(self):
		direction = self.rand_gust_direction()
		gust_direction =  self.gust_vertical_directions[direction]
		gust_speed =  random.gauss(self.mean_and_standard_dev[0], self.mean_and_standard_dev[1])
		return (gust_direction, gust_speed)
		
	def rand_side_gust(self):
		direction = self.rand_gust_direction()
		gust_direction =  self.gust_horizontal_directions[direction]
		gust_speed =  random.gauss(self.mean_and_standard_dev[0], self.mean_and_standard_dev[1])
		return (gust_direction, gust_speed)


class Simulator:

	aircraft = None
	gust = None
	mean_and_standard_dev = None

	def __init__(self, aircraft, gust):
		self.aircraft = aircraft
		self.aircraft_desired_orientation = None
		self.aircraft_desired_direction = None
		self.gust = gust
		self.mean_and_standard_dev = (10, 50/3)
		
	def set_desired_aircraft_properties(self):
		self.aircraft_desired_direction = self.aircraft.direction
		self.aircraft_desired_orientation = self.aircraft.orientation
			
	def invoke_turbulations(self):
		print """
		turbulations!"""
		self.simulate_speed_changes(None)
		gust_values = self.gust.rand_vertical_gust_for_turbulations()
		angle_change_value = math.atan(gust_values[1] / self.aircraft.speed) * gust_values[0][1]
		self.aircraft.orientation = self.aircraft.orientation + angle_change_value
		print bcolors.WARNING + """
		FLT ORI: {0:10.2f}""".format(self.aircraft.orientation) + bcolors.ENDC
		print """
		appling the tilt correction..."""
		self.aircraft.tilt_correction(self.aircraft_desired_orientation)
		
	def simulate_speed_changes(self, wind_speed):
		
		if wind_speed is None:
			speed_change = random.gauss(self.mean_and_standard_dev[0], self.mean_and_standard_dev[1])
			self.aircraft.speed = self.aircraft.speed + speed_change
		else:
			self.aircraft.speed = math.sqrt(math.pow(self.aircraft.speed, 2) - math.pow(wind_speed[1], 2))
	def simulate_side_wind(self):
		gust_values = self.gust.rand_side_gust()
		print """
		{0} side wind: {1:.2f}!""".format(gust_values[0][0], gust_values[1])
		self.simulate_speed_changes(gust_values);
		angle_change_value = math.asin(gust_values[1] / self.aircraft.speed) * gust_values[0][1]
		self.aircraft.direction = self.aircraft.direction + angle_change_value
		print bcolors.WARNING + """
		FLT DIR: {0:10.2f}""".format(self.aircraft.direction) + bcolors.ENDC
		print """
		appling correction..."""
		self.aircraft.direction_correction(self.aircraft_desired_direction)
		
		
	def random_simulator_procedure(self):
		random.choice([self.invoke_turbulations, self.simulate_side_wind])()
		
	def start_simulator(self):
		print "Flight simulator\nTo exit press Ctrl + c"
		time.sleep(2)
		self.aircraft.set_aircraft_properties()
		self.set_desired_aircraft_properties()

		print """
		Starting..."""
	
	
		try:
			while True:
				self.aircraft.aircraft_console()
				time.sleep(2)
				self.random_simulator_procedure()
		except KeyboardInterrupt:
			exit()
		

if __name__ == '__main__':
	aircraft = Aircraft()
	gust = Gust()
	simulator = Simulator(aircraft, gust)
	simulator.start_simulator()

	
