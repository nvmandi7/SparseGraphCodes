from numpy import random
from math import floor
import time
import numpy as np
from matplotlib import pyplot as plt


def gen_dist(k, n, L):
	# Generates a matching of jobs and machines with given parameters, 
	# as a repetition code

	# Long list of all jobs, then split by machines
	jobs = [i % k for i in range(n * L)]
	machines_jobs_list = []
	for j in range(n):
		machines_jobs_list.append(jobs[:L])
		jobs = jobs[L:]
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
	num = int(len(machines_with_times) / len(machines_with_times[0][1]))

	for time, machine in machines_with_times[:num]:
		for j in machine:
			answers[j] = True

		p = sum(answers) / float(len(answers))
		data.append( (time, p) )
	return data


k = 1000
n = 1400
L = 3
sf = 0.1
nt = 10

def single_sim():
	data = step_peel(run_jobs(gen_dist(k, n, L)), k)
	times, fracs = [d[0] for d in data], [d[1] for d in data]
	print(fracs)
	plt.figure()
	plt.plot(times, fracs, 'o', linestyle=' ')
	plt.show()

def multi_sim(num_trials):
	times, fracs = [], []
	successes = 0
	for _ in range(num_trials):
		data = step_peel(run_jobs(gen_dist(k, n, L)), k)
		times.extend([d[0] for d in data])
		fracs.extend([d[1] for d in data])
		if fracs[-1] >= .95: successes += 1
	print(successes / float(num_trials))

	plt.figure()
	plt.plot(times, fracs, 'o', linestyle=' ')
	plt.xlabel('Time (jobs are exponentials with mean 1)')
	plt.ylabel('Fraction of job answers decoded')

	plt.title('Regular-soliton, k=%d, n=%d, L=%d, sf=%.2f' % (k, n, L, sf))
	plt.show()
	# plt.savefig('Figures/k=%d/n=%d/L=%d,sf=%.2f.png' % (k, n, L, sf))
	# plt.savefig('Figures/sf_range/sf=%.2f.png' % sf)


multi_sim(nt)













