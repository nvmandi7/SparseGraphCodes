from numpy import random
from math import floor, log
from supporting_files.coded_computation import *

'''
This file contains the specific task init method needed for the regular-regular simulation.
Both left and right are regularly distributed. 
'''

class Regular(Task):

	def __init__(self, k, n, L, eps, left_degree):
		# t0 = time.time()		
		self.k = k
		self.n = int(n)
		self.L = L
		self.epsilon = eps
		self.mu, self.T = 1, 2
		self.irregular_left = False

		self.jobs = [Job(i, left_degree, 1) for i in range(self.k)]

		singleton_percent = 0.05
		self.machines = [Machine(1) for _ in range(int(singleton_percent*self.n))]
		rest = self.n - int(singleton_percent*self.n)

		right_degree = floor(left_degree*self.k / rest)
		rem = left_degree*self.k - right_degree*rest
		right_degrees = [right_degree for _ in range(rest)]
		for i in range(rem): right_degrees[i] += 1
		self.machines.extend([Machine(d) for d in right_degrees])


	def distribute(self):
		# Requires left and right total degrees equal
		all_jobs = []
		for job in self.jobs:
			lst = [job.index for _ in range(job.degree)]
			all_jobs.extend(lst)
		random.shuffle(all_jobs)

		# Fix bug with giving machine same job twice

		for machine in self.machines:
			machine.jobs, i, rem = [], 0, machine.degree
			try:
				while rem > 0:
					if all_jobs[i] not in machine.jobs:
						machine.jobs.append(all_jobs.pop(i))
						rem -= 1
					else:
						i += 1
			except IndexError:
				machine.jobs = all_jobs

