from graph_subroutines import *

#input
k = 6
n = 7
eps = 0.1 # error probability -> depend on T
n_trial = 1

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

success_rate = run_multiple_trials(k, n, eps, n_trial)
print success_rate
	

