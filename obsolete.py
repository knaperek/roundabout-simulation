# class LaneResource(simpy.resources.resource.PriorityResource):
# 	""" Quater of circle in the roundabout. """

# 	def __init__(self, *args, **kwargs):
# 		ret = super(LaneResource, self).__init__(*args, **kwargs)
# 		# initialize references to resources around
# 		self.previous = None
# 		self.next = None
# 		return ret

# 	def enter_circle(self):
# 		""" For cars entering the roundabout. They have lower priority. """
# 		# TODO: implement checking previous LaneResource()
# 		# with self.request(priority=0, preempt=False) as event:
# 		# 	yield event
# 		# 	# 
# 		return self.request(priority=0, preempt=False)

# 	def continue_driving(self):
# 		""" For cars that are already in the roundabout, finishing one quarter and starting another one. They have higher priority. """
# 		return self.request(priority=1, preempt=False)
