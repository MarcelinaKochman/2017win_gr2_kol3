import unittest
from kol1 import Simulator
from kol1 import Aircraft
from kol1 import Gust

#kol1_KingaPiasecka

class TestFlightSimulator(unittest.TestCase):
	
	def test_set_aircraft_properties_correct(self):
		aircraft = Aircraft()
		gust = Gust()
		simulator = Simulator(aircraft, gust)

if __name__ == '__main__':
    unittest.main()
