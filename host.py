import vist
import datetime as dt

class Host():
	request_count = 0
	def __init__(self, name):
		self.name = name #ip address
		self.vists =[]

	def count_req_date (self, date):			
		for i, val in enumerate (self.vists):		#compare only dates and not times aswlel
			if val.time.date() == date:
				self.request_count = self.request_count + 1		
		return self.request_count
		
	def count_vists (self):
		total = len(self.vists)
		total_collisons = 0 #number of times illigitmate vists were made
		for i in range(1,len(self.vists)-1):
			if abs(( self.vists[i-1].time - self.vists[i].time).total_seconds()) < 3600:	#seconds in a hour
				total_collisons = total_collisons + 1
		return total-total_collisons 
