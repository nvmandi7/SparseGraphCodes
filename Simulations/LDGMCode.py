from numpy import random
from math import floor

'''
This file contains all the classes needed for the LDGM simulation. 
Later we will move toward a more generalized API.

k = number of jobs
n = number of machines
L = number of cores per machine
mu = mean time for computation (modeled as exponential RV)

'''

class Task(object):

	def __init__(self, k, n, L, mu, T):
		self.k = k
		self.n = n
		self.L = L
		self.mu = mu
		self.T = T

		H_L = 1 / sum([1/i for i in range(1,L+1)])
		machine_degrees = []
		for i in range(1,L+1):
			lst = [i for _ in range(floor(n*H_L/i))]
			machine_degrees.extend(lst)
		while len(machine_degrees) != n:
			machine_degrees.append(1)
		while sum(machine_degrees) % k != 0:
			machine_degrees[0] += 1  # Forces self.job_degree to be an integer
		self.machines = [Machine(d) for d in machine_degrees]

		self.job_degree = int(sum(machine_degrees) / k)
		self.jobs = [Job(i, self.job_degree, mu) for i in range(k)]


	def singleton(self, metalst):
		for lst in metalst:
			if len(lst) == 1: return lst
		return [-1]


	def distribute(self, irregular_left=False):
		if irregular_left:
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
		answers = [False for job in self.jobs]
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
		





