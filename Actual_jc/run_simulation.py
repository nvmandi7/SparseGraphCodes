#!/usr/bin/python
from math import ceil
from graph_subroutines import *

#input
k = 100

ns = range(int(1.0*k), int(2*k+1), int(ceil(k/float(10))))
# ns = [7,8,9]
epss = [0.1, 0.01, 0.001] # list of epsilons

n_trial = 100
error_floor = 0.01


def run_trial(k, n, eps):
	machines_jobs_list = distribute_jobs(n , k)
	machine_failed_list = just_get_machine_failed_list(n, eps)
	_, _, peel_success = peel(machines_jobs_list, machine_failed_list, n, k, error_floor, get_decode_seq = False)
	return peel_success

def run_multiple_trials(k, n, eps, n_trial):
	ct_success = 0
	for i in range(n_trial):
		ct_success += int(run_trial(k,n,eps))
	success_rate = ct_success / float(n_trial)
	return success_rate

success_rates_epss = []
for eps in epss:
	success_rates = []
	print "running sim eps=", eps, ", k=", k
	for n in ns:
		success_rate = run_multiple_trials(k, n, eps, n_trial)
		print "success_rate", success_rate, "for n/k=%f"%(k/float(n))
		success_rates.append(success_rate)
	success_rates_epss.append(success_rates)
	save_success_rate_list_sim(ns, success_rates, eps)

plotting_sim(k, ns, epss, success_rates_epss)



