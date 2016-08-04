from numpy import random
from math import floor
from coded_computation import *

'''
This file contains the specific task init method needed for the repetition code simulation. 

It turns out, there's no need to even consider this code, because LDGM converges to 
probability 1 of success long before using even twice as many machines as jobs.
'''

class LDGM_task(Task):

	def __init__(self, k, n, L, mu, T, il):
		self.k = k
		self.n = n
		self.L = L
		self.mu = mu
		self.T = T
		self.irregular_left = False

		self.job_degrees = [math.floor(self.n / self.k) for i in range(self.k)]
		for i in range(n%k):
			self.job_degrees[i] += 1
		self.jobs = [Job(i, d, mu) for d in self.job_degrees]

		self.machines = [Machine(1) for _ in range(self.n)]
