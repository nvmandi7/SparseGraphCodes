from numpy import random
from math import floor
import time

'''
This file contains the classes needed for simulations of jobs and machines
passing messages for by a peeling decoder. See other files for specific 
implementations of coding schemes.

k = number of jobs
n = number of machines
L = number of cores per machine
mu = mean time for computation (modeled as exponential RV)

'''

class Task(object):

	def __init__(self, k, n, L, mu, T, il, eps=10**-3):
		self.k = k
		self.n = n
		self.L = L
		self.mu = mu
		self.T = T
		self.irregular_left = il
		self.epsilon = eps


	def singleton(self, metalst):
		for lst in metalst:
			if len(lst) == 1: return lst
		return [-1]


	def distribute(self):
		t0 = time.time()
		if self.irregular_left:
			for machine in self.machines:
				machine.jobs = list(random.choice(range(self.k), size=machine.degree, replace=False))
				#machine.give_jobs(list(jobs))
			# print('distribute (il) time: ', time.time()-t0)
			return

		# Requires left and right total degrees equal
		all_jobs = []
		for job in self.jobs:
			lst = [job.index for _ in range(job.degree)]
			all_jobs.extend(lst)
		random.shuffle(all_jobs)

		# Fix bug with giving machine same job twice

		for machine in self.machines[::-1]:
			machine.jobs, i, rem = [], 0, machine.degree
			while rem > 0:
				if all_jobs[i] not in machine.jobs:
					machine.jobs.append(all_jobs.pop(i))
					rem -= 1
				else:
					i += 1


		# print('distribute time: ', time.time()-t0)


	def run(self):
		self.return_values = []
		for machine in self.machines:
			if machine.compute(self.T, self.mu, self.epsilon):
				self.return_values.append(machine.jobs)


	def peel_successful(self):
		t0 = time.time()
		#self.return_values.sort(key=len)
		answers = [False for i in range(self.k)]
		while True:
			if all(answers): 
				# print('peel time: (True)', time.time()-t0)
				return True
			job = self.singleton(self.return_values)[0]
			if job == -1: 
				# print('peel time: ()', time.time()-t0)
				return sum(answers) > .99*len(answers)
			answers[job] = True

			for lst in self.return_values:
				if job in lst: lst.remove(job)
			self.return_values.remove([])




# ==================================================

class Job(object):

	def __init__(self, index, degree, mu):
		self.index = index
		self.degree = degree
		self.mu = mu


class Machine(object):

	def __init__(self, degree):
		self.degree = degree

	def give_jobs(self, jobs):
		if len(jobs) != self.degree:
			raise Exception('Wrong number of jobs for this machine')
		self.jobs = jobs
	
	def compute(self, T, mu, eps): # Returns boolean - whether it finished in time
		# times = [random.exponential(mu) for job in self.jobs]
		# return (max(times) <= T)
		return eps < random.random() # Assume constant failure probability
		





