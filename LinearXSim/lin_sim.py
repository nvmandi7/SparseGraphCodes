from numpy import random
from math import floor
import time
import numpy as np
from matplotlib import pyplot as plt


def gen_dist(k, n, L, sing_frac):
	# Generates a random matching of jobs and machines with given parameters, 
	# according to a regular-soliton model

	# Making soliton right degrees
	L_soliton = [0]*(L+1) # Pseudo 1-indexed
	for i in range(2, L+1):
		L_soliton[i] = 1/float((i * (i-1)))

	# Adding some percentage of singletons, normalizing
	L_soliton = [(1-sing_frac)*a/sum(L_soliton) for a in L_soliton]
	L_soliton[1] = sing_frac

	num_machines = [round(n*l) for l in L_soliton]
	num_machines[1] += n - sum(num_machines)

	machines = []
	for d in range(len(num_machines)):
		machines.extend([d for _ in range(int(num_machines[d]))])

	# Making regular left degrees
	right_total = sum(machines)
	ave_degree = np.floor(right_total / k)
	#print(right_total / float(k))
	remainder = right_total - ave_degree*k
	
	job_degrees = [ave_degree for _ in range(k)]
	for i in range(int(remainder)): job_degrees[i] += 1



	# Distributing
	all_jobs = []
	for i in range(len(job_degrees)):
		lst = [i for _ in range(int(job_degrees[i]))]
		all_jobs.extend(lst)
	np.random.shuffle(all_jobs)

	# Don't give machine same job twice
	succeeded = False
	while not succeeded:
		np.random.shuffle(all_jobs)
		machines_jobs_list = []
		for machine in machines[::-1]:
			m_jobs, i, rem = [], 0, machine
			while rem > 0:
				if i >= len(all_jobs):
					rem = -1
				elif all_jobs[i] not in m_jobs:
					m_jobs.append(all_jobs.pop(i))
					rem -= 1
				else:
					i += 1
			machines_jobs_list.append(m_jobs)
		if len(machines_jobs_list) == len(machines):
			succeeded = True

	# # Save a histogram of the degree distribution
	# plt.figure()
	# plt.bar([i+0.6 for i in range(L)], num_machines[1:], 0.8)

	# plt.xlabel('Degree')
	# plt.ylabel('Number of machines (n=%d)' % n)
	# plt.title('Right Degree Distribution for Regular-Soliton\n k=%d, n=%d, L=%d, sf=%.2f' % (k, n, L, sf))
	# plt.savefig('dist.png')

	return machines_jobs_list



def run_jobs(machines_jobs_list):
	machines_with_times = []
	for machine in machines_jobs_list:
		t = random.exponential(1)
		machines_with_times.append( (t, machine) ) 
	return sorted(machines_with_times)



def step_peel(machines_with_times, k):
	# Returns data points for time vs fraction of job answers recovered
	data = []
	answers = [False for i in range(k)]
	available = []

	for time, machine in machines_with_times:
		for i in range(k):
			if answers[i] and i in machine: machine.remove(i)

		available.append(machine)
		available.sort(key=len)

		while available and len(available[0]) <= 1:
			if len(available[0]) == 0:
				available.pop(0)
			else:
				job = available.pop(0)[0]
				answers[job] = True
				for machine in available:
					if job in machine: machine.remove(job)
				available.sort(key=len)

		p = sum(answers) / float(len(answers))
		data.append( (time, p) )
	return data


k = 1000
n = 1400
L = 8
sf = 0.15
nt = 10

def single_sim():
	data = step_peel(run_jobs(gen_dist(k, n, L, sf)), k)
	times, fracs = [d[0] for d in data], [d[1] for d in data]
	print(fracs)
	plt.figure()
	plt.plot(times, fracs, 'o', linestyle=' ')
	plt.show()

def multi_sim(num_trials):
	times, fracs = [], []
	successes = 0
	for _ in range(num_trials):
		data = step_peel(run_jobs(gen_dist(k, n, L, sf)), k)
		times.extend([d[0] for d in data])
		fracs.extend([d[1] for d in data])
		if fracs[-1] >= 1.00: successes += 1
	print(successes / float(num_trials))

	plt.figure()
	plt.plot(times, fracs, 'o', linestyle=' ')
	plt.xlabel('Time (jobs are exponentials with mean 1)')
	plt.ylabel('Fraction of job answers decoded')
	plt.xlim(0, 2)

	plt.title('Regular-soliton, k=%d, n=%d, L=%d, sf=%.2f' % (k, n, L, sf))
	plt.show()
	# plt.savefig('Figures/k=%d/n=%d/L=%d,sf=%.2f.png' % (k, n, L, sf))
	# plt.savefig('Figures/sf_range/sf=%.2f.png' % sf)


multi_sim(nt)













