from numpy import random
from math import floor, log
from supporting_files.coded_computation import *

'''
This file contains the specific task init method needed for the LDGM simulation.
The right node degree distribution is soliton. 
'''

class LDGM_task(Task):

	def __init__(self, k, n, L, mu, T, il, eps=10**-1):
		self.k = k
		self.n = int(n)
		self.L = L
		self.mu = mu
		self.T = T
		self.irregular_left = il
		self.epsilon = eps

		L_soliton = [0]*(self.L+1) # Pseudo 1-indexed
		for k in range(2, L+1):
			L_soliton[k] = 1/(k * (k-1))

		# Adding 5% singletons, normalizing
		L_soliton = [.95*a/sum(L_soliton) for a in L_soliton]
		L_soliton[1] = .05

		# Sampling
		#self.machines =  [Machine(random.choice(range(self.L+1), p=L_soliton)) for _ in range(self.n)]

		num_machines = [round(self.n*l) for l in L_soliton]
		num_machines[1] += self.n - sum(num_machines)

		self.machines = []
		for d in range(len(num_machines)):
			self.machines.extend([Machine(d) for _ in range(num_machines[d])])











		# # Old Code, just here for reference

		# H_L = 1 / sum([1/i for i in range(1,L+1)])
		# machine_degrees = []
		# for i in range(1,L+1):
		# 	lst = [i for _ in range(floor(n*H_L/i))]
		# 	machine_degrees.extend(lst)
		# while len(machine_degrees) != n:
		# 	machine_degrees.append(random.randint(1, L+1))

		# if not self.irregular_left:
		# 	while sum(machine_degrees) % k != 0:
		# 		machine_degrees[0] += 1  # Forces self.job_degree to be an integer

		# 	self.job_degree = int(sum(machine_degrees) / k)
		# 	self.jobs = [Job(i, self.job_degree, mu) for i in range(k)]

		# self.machines = [Machine(d) for d in machine_degrees]
