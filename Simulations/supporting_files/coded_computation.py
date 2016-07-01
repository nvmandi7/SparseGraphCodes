from numpy import random
from math import floor

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

	def __init__(self, k, n, L, mu, T, il):
		self.k = k
		self.n = n
		self.L = L
		self.mu = mu
		self.T = T
		self.irregular_left = il


	def singleton(self, metalst):
		for lst in metalst:
			if len(lst) == 1: return lst
		return [-1]


	def distribute(self):
		if self.irregular_left:
			for machine in self.machines:
				jobs = random.choice(range(self.k), size=machine.degree, replace=False)
				machine.give_jobs(list(jobs))
			return

		all_jobs = []
		for job in self.jobs:
			lst = [job.index for _ in range(self.job_degree)]
			all_jobs.extend(lst)
		random.shuffle(all_jobs)

		for machine in self.machines:
			jobs = [all_jobs.pop() for _ in range(machine.degree)]
			machine.give_jobs(jobs)


	def run(self):
		self.return_values = []
		for machine in self.machines:
			if machine.compute(self.T, self.mu):
				self.return_values.append(machine.jobs)


	def peel_successful(self):
		answers = [False for i in range(self.k)]
		while True:
			if all(answers): return True
			job = self.singleton(self.return_values)[0]
			if job == -1: return sum(answers) > .99*len(answers)
			answers[job] = True

			for lst in self.return_values:
				if job in lst: lst.remove(job)



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
	
	def compute(self, T, mu): # Returns boolean - whether it finished in time
		times = [random.exponential(mu) for job in self.jobs]
		return (max(times) <= T)
		





