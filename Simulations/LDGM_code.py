from numpy import random
from math import floor
from supporting_files.coded_computation import *

'''
This file contains the specific task init method needed for the LDGM simulation. 
'''

class LDGM_task(Task):

	def __init__(self, k, n, L, mu, T, il):
		self.k = k
		self.n = n
		self.L = L
		self.mu = mu
		self.T = T
		self.irregular_left = il

		H_L = 1 / sum([1/i for i in range(1,L+1)])
		machine_degrees = []
		for i in range(1,L+1):
			lst = [i for _ in range(floor(n*H_L/i))]
			machine_degrees.extend(lst)
		while len(machine_degrees) != n:
			machine_degrees.append(random.randint(1, L+1))

		if not self.irregular_left:
			while sum(machine_degrees) % k != 0:
				machine_degrees[0] += 1  # Forces self.job_degree to be an integer

			self.job_degree = int(sum(machine_degrees) / k)
			self.jobs = [Job(i, self.job_degree, mu) for i in range(k)]

		self.machines = [Machine(d) for d in machine_degrees]
