import numpy as np
import csv
from math import floor
from numpy import random

def distribute_jobs(n , k, dist_type='regular-soliton', params=[]):
	# machines_jobs_list = [[0,1,2], [1, 2], [2]]
	# machines_jobs_list = [[0,1] ,[1]]
	# machines_jobs_list = [[0,1,2] ,[1,2], [0], [2]]
	# machines_jobs_list = [[0,1,2] ,[1,2], [0], [2,4], [3], [0,1], [4,5]]
	# return machines_jobs_list
	if dist_type == 'regular-soliton':
		# Default
		if params == []: params = [8, 0.05]
		L, sing_frac = params[0], params[1]

		# Making soliton right degrees
		L_soliton = [0]*(L+1) # Pseudo 1-indexed
		for k in range(2, L+1):
			L_soliton[k] = 1/float((k * (k-1)))

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
		ave_degree = floor(right_total / k)
		remainder = right_total - ave_degree*k
		
		job_degrees = [ave_degree for _ in range(k)]
		for i in range(int(remainder)): job_degrees[i] += 1


		# Distributing
		all_jobs = []
		for i in range(len(job_degrees)):
			lst = [i for _ in range(int(job_degrees[i]))]
			all_jobs.extend(lst)
		random.shuffle(all_jobs)

		# Don't give machine same job twice
		machines_jobs_list = []
		for machine in machines[::-1]:
			m_jobs, i, rem = [], 0, machine
			while rem > 0:
				if all_jobs[i] not in m_jobs:
					m_jobs.append(all_jobs.pop(i))
					rem -= 1
				else:
					i += 1
			machines_jobs_list.append(m_jobs)
		print machines_jobs_list
		return machines_jobs_list
		

	elif dist_type == 'irregular-soliton':
		pass





	elif dist_type == 'regular-regular':
		pass
		













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