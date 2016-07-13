import matplotlib; matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend; instead, writes files
from matplotlib import pyplot as plt
import numpy as np
import csv

def distribute_jobs(n , k):
	# machines_jobs_list = [[0, 1, 2], [1, 2], [2]]
	# machines_jobs_list = [[0, 1] ,[1]]
	# machines_jobs_list = [[0, 1,2] ,[1,2], [0], [2]]
	machines_jobs_list = [[0, 1,2] ,[1,2], [0], [2,4], [3], [0,1], [4,5]]
	return machines_jobs_list


def save_machines_jobs_list(machines_jobs_list):
	# save machines_jobs_list as csv column list of (job_number, machine_number, local_master_rank)
	csv_file = open("machines_jobs_list.csv", "w")
	cw = csv.writer(csv_file , delimiter=',', quotechar='|')

	local_master_rank = 0
	for i1 in range(len(machines_jobs_list)):
		for i2 in range(len(machines_jobs_list[i1])):
			job_number = machines_jobs_list[i1][i2]
			machine_number = i1
			cw.writerow([str(job_number), str(machine_number), str(local_master_rank)])
		local_master_rank += len(machines_jobs_list[i1])

	csv_file.close()


def read_machines_jobs_list(n, k, rank):
	# read machines_jobs_list from csv column list of (job_number, machine_number, local_master_rank)
	# use rank = -1 to avoid providing local machine info
	
	machines_jobs_list = [[] for i in range(n)]
	local_master_list = [-1 for i in range(n)] # indcates local master's rank
	
	my_local_master_rank = -2
	my_machine_number = -2
	my_job_number = -2
	my_local_process_rank_list = []
	global_master_rank = -2


	csv_file = open("machines_jobs_list.csv", "r")
	cr = csv.reader(csv_file)

	ct_rank = 0
	for row in cr:
		job_number = int(row[0])
		machine_number = int(row[1])
		local_master_rank = int(row[2])
		machines_jobs_list[machine_number].append(job_number)
		if local_master_list[machine_number] == -1:
			local_master_list[machine_number] = local_master_rank
		if rank == ct_rank:
			my_machine_number = machine_number
			my_job_number = job_number
			my_local_master_rank = local_master_rank

		ct_rank += 1
	csv_file.close()

	if rank != -1:
		my_local_process_rank_list = \
			[(my_local_master_rank + i) for i in range(len(machines_jobs_list[my_machine_number]))]
		global_master_rank = sum([len(machines_jobs_list[i]) for i in range(len(machines_jobs_list))])

	master_info = (machines_jobs_list, local_master_list)
	worker_info = (my_job_number, my_machine_number, my_local_master_rank, my_local_process_rank_list, global_master_rank)

	if rank == -1:
		return master_info
	else:
		return worker_info


def peel(machines_jobs_list, machine_failed_list, n, k, error_floor, get_decode_seq = True):
	job_success = [False for _ in range(k)]

	dec_seq = np.identity(n , dtype = int) 
	dec_ans = [(-1) for _ in range(k)]

	# eliminate jobs from failed machine
	for machine_index in machine_failed_list:
		machines_jobs_list[machine_index] = []

	# peeling process
	singleton_exist = True
	while singleton_exist:
		singleton_exist = False
		for m_i in range(len(machines_jobs_list)): 
			# check singleton
			if (len(machines_jobs_list[m_i]) == 1):
				singleton_exist = True
				job_singleton = machines_jobs_list[m_i].pop()
				job_success[job_singleton] = True
				if get_decode_seq:
					dec_ans[job_singleton] = m_i

				#remove singleton job from other machine
				for m_i2 in range(len(machines_jobs_list)):
					if job_singleton in machines_jobs_list[m_i2]:
						machines_jobs_list[m_i2].remove(job_singleton)
						
						if get_decode_seq:
							# calculate decoding sequence 
							dec_seq[m_i2] -= dec_seq[m_i] 

	# check all job-machine edges peeled (not used for right now)
	# if sum(len(machine) for machine in machine_jobs) == 0:
	# 	peel_success = True 
	# else:
	# 	peel_success = False

	# check if successfully got job value
	if sum(job_success) > (1- error_floor)*len(job_success):
		peel_success = True
	else:
		peel_success = False
	# print job_success

	return dec_seq, dec_ans, peel_success

def just_get_machine_failed_list(n, eps):
	machine_failed_list = []
	for i in range(n):
		if eps > np.random.random():
			machine_failed_list.append(i)
		else:
			pass
	return machine_failed_list


def save_success_rate_list(ns, success_rates, T):
	csv_file = open("success_rate_list_T%.2f.csv" % T, "w")
	cw = csv.writer(csv_file , delimiter=',', quotechar='|')

	for i in range(len(ns)):
		cw.writerow([str(ns[i]), str(success_rates[i])])
	csv_file.close()

def save_success_rate_list_sim(ns, success_rates, eps):
	csv_file = open("success_rate_list_eps%f.csv" % eps, "w")
	cw = csv.writer(csv_file , delimiter=',', quotechar='|')

	for i in range(len(ns)):
		cw.writerow([str(ns[i]), str(success_rates[i])])
	csv_file.close()


def plotting(k, ns, Ts, success_rates_Ts):
	ndivk = [ns[i]/float(k) for i in range(len(ns))]
	# print "n/k", ndivk
	# ndivk = [1.0, 1.2, 1.4]
	# success_rates_Ts = [[0.2, 0.6, 0.8], [0.9, 0.95, 1.0]]
	
	for i in range(len(Ts)):
		plt.plot(ndivk, success_rates_Ts[i], label='T=%.2f'% Ts[i])
	
	plt.title('LDGM Success Rate for k=%d' % k)
	plt.xlabel('Ratio of machines to jobs (n/k)')
	plt.ylabel('Success Rate')
	plt.legend()
	# plt.show()
	plt.savefig('f1.png')


def plotting_sim(k, ns, epss, success_rates_epss):
	ndivk = [ns[i]/float(k) for i in range(len(ns))]
	# print "n/k", ndivk
	
	# ndivk = [1.0, 1.2, 1.4]
	# success_rates_Ts = [[0.2, 0.6, 0.8], [0.9, 0.95, 1.0]]
	

	for i in range(len(epss)):
		plt.plot(ndivk, success_rates_epss[i], label='eps=%f'% epss[i])
	
	plt.title('LDGM Success Rate (sim) for k=%d' % k)
	plt.xlabel('Ratio of machines to jobs (n/k)')
	plt.ylabel('Success Rate')
	plt.legend()
	# plt.show()
	plt.savefig('f_sim.png')