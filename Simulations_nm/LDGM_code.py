from numpy import random
from math import floor, log
from supporting_files.coded_computation import *

'''
This file contains the specific task init method needed for the LDGM simulation.
The right node degree distribution is soliton. 
'''

class LDGM_task(Task):

	def __init__(self, k, n, L, mu, T, il, eps=10**-3):
		t0 = time.time()
		self.k = k
		self.n = int(n)
		self.L = L
		self.mu = mu
		self.T = T
		self.irregular_left = il
		self.epsilon = eps

		L_soliton = [0]*(self.L+1) # Pseudo 1-indexed
		L_soliton[1] = 1/L
		for k in range(2, L+1):
			L_soliton[k] = 1/(k * (k-1))

		# Making robust
		M = self.L
		for i in range(1, M):
			L_soliton[i] + 1/(i*M)
		L_soliton[M] += log(self.L/(M*self.epsilon)) / M

		# Normalizing
		L_soliton = [a/sum(L_soliton) for a in L_soliton]

		# Sampling
		self.machines =  [Machine(random.choice(range(self.L+1), p=L_soliton)) for _ in range(self.n)]

		right_total = sum([m.degree for m in self.machines])
		ave_degree = floor(right_total / self.k)
		remainder = right_total - ave_degree*self.k
		
		job_degrees = [ave_degree for _ in range(self.k)]
		for i in range(remainder): job_degrees[i] += 1
		self.jobs = [Job(i, job_degrees[i], mu) for i in range(self.k)]
		print('init time: ', time.time()-t0)










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
