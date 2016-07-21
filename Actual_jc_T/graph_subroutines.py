import matplotlib; matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend; instead, writes files
from matplotlib import pyplot as plt
import numpy as np
import csv

def distribute_jobs(n , k, dist_type='regular-soliton', params=[]):# machines_jobs_list = [[0, 1, 2], [1, 2], [2]]
	# machines_jobs_list = [[0, 1] ,[1]] # k2 n2
	# machines_jobs_list = [[0, 1,2] ,[1,2], [0], [2]] # k3 n4
	# machines_jobs_list = [[0, 1,2] ,[1,2], [0], [2,4], [3], [0,1], [4,5]]  # k6 n7
	# return machines_jobs_list
	# import random; seed0 = random.randint(0,10000)
	# seed0 = 3635
	# print "np seed", seed0
	# np.random.seed(seed0)
	#---------------------

	# Nathan's distribtuion part

	if 'soliton' in dist_type:
		# Default
		if params == []: params = [8, 0.05]
		L, sing_frac = params[0], params[1]

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


		if dist_type == 'regular-soliton':
			# Making regular left degrees
			right_total = sum(machines)
			ave_degree = np.floor(right_total / k)
			remainder = right_total - ave_degree*k
			
			job_degrees = [ave_degree for _ in range(k)]
			for i in range(int(remainder)): job_degrees[i] += 1
		elif dist_type == 'irregular-soliton':
			jobs = range(k)
			for machine in machines:
				m_jobs = list(np.random.choice(jobs, size=machine, replace=False))
				machines_jobs_list.append(m_jobs)
			return machines_jobs_list


	elif dist_type == 'regular-regular':
		if params == []: params = [3, 0.05]
		right_degree, sing_frac = params[0], params[1]

		machines = [1 for _ in range(int(sing_frac*n))]
		rest = n - int(sing_frac*n)
		machines.extend([right_degree for _ in range(rest)])

		# Making regular left degrees
		right_total = sum(machines)
		ave_degree = np.floor(right_total / k)
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
	# print machines_jobs_list
	return machines_jobs_list

def peel_T(machines_jobs_list, arrival_time, n, k, error_floor, get_decode_seq = False):

	job_success = [False for _ in range(k)]

	dec_seq = np.identity(n , dtype = int) 
	dec_ans = [(-1) for _ in range(k)] # decode answer machine number


	arrive_order = sorted(range(len(arrival_time)), key=lambda k: arrival_time[k]) # gets the index of sorted arrival_time list

	current_machines_jobs_list = [[] for _ in range(n)]
	
	# peeling process
	
	# print "arrive order", arrive_order


	suc_T = -1.0 # returns -1 if failed to succeed

	for t_i in range(n):
		arrived_machine = arrive_order[t_i]
		current_machines_jobs_list[arrived_machine] = machines_jobs_list [arrived_machine]
		# print current_machines_jobs_list
		

		#try peeling
		# check singletons
		singleton_exist = True
		while singleton_exist:
			singleton_exist = False
		
			# remove already known job edge from other machines
			for m_i2 in range(len(current_machines_jobs_list)):
				for job_i in current_machines_jobs_list[m_i2]:
					if job_success[job_i]:
						current_machines_jobs_list[m_i2].remove(job_i) #peeling
						if get_decode_seq:
						# calculate decoding sequence 
							dec_seq[m_i2] -= dec_seq[dec_ans[job_i]]
		
			# check singleton
			for m_i in range(len(current_machines_jobs_list)): 
				if (len(current_machines_jobs_list[m_i]) == 1):
					singleton_exist = True
					job_singleton = current_machines_jobs_list[m_i].pop()
					job_success[job_singleton] = True
					if get_decode_seq:
						dec_ans[job_singleton] = m_i


		# print "check singleton",  [job_i for job_i in range(len(job_success)) if job_success[job_i]==True]  
		# print ""

		if sum(job_success) > (1- error_floor)*len(job_success):
			suc_T = arrival_time[t_i]
			break

	return suc_T, dec_seq, dec_ans



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


def read_machines_jobs_list(n, k):
	# read machines_jobs_list from csv column list of (job_number, machine_number, local_master_rank)
	# use rank = -1 to avoid providing local machine info
	
	machines_jobs_list = [[] for i in range(n)]
	local_master_list = [-1 for i in range(n)] # indcates local master's rank

	csv_file = open("machines_jobs_list.csv", "r")
	cr = csv.reader(csv_file)

	for row in cr:
		job_number = int(row[0])
		machine_number = int(row[1])
		local_master_rank = int(row[2])
		machines_jobs_list[machine_number].append(job_number)
		if local_master_list[machine_number] == -1:
			local_master_list[machine_number] = local_master_rank
	csv_file.close()

	master_info = (machines_jobs_list, local_master_list)

	return master_info

def get_machines_jobs_list(machines_jobs_list_flat, machines_jobs_list_sizes):
	machines_jobs_list = [[] for _ in range(len(machines_jobs_list_sizes))]
	m_i = 0
	ct0 = 0
	for i in range(len(machines_jobs_list_flat)):
		machines_jobs_list[m_i].append(machines_jobs_list_flat[i])
		ct0 += 1
		if ct0 == machines_jobs_list_sizes[m_i]:
			m_i += 1
			ct0 = 0
	return machines_jobs_list

def get_worker_info_from_machines_jobs_list(n,k,machines_jobs_list, rank):

	job_number_worker = -1
	local_master_rank = -1
	local_process_rank_list = []

	ct_rank = 0
	ct_master_rank = 0
	for n_i in range(n):
		for job_number in machines_jobs_list[n_i]:
			if rank == ct_rank:
				job_number_worker = job_number
				local_master_rank = ct_master_rank
				local_process_rank_list = [(local_master_rank + i2) for i2 in range(len(machines_jobs_list[n_i]))]
			ct_rank +=1
		ct_master_rank += len(machines_jobs_list[n_i])
	
	return job_number_worker, local_master_rank, local_process_rank_list



def just_get_machine_failed_list(n, eps):
	machine_failed_list = []
	for i in range(n):
		if eps > np.random.random():
			machine_failed_list.append(i)
		else:
			pass
	return machine_failed_list


def save_suc_Tss_list(ns, suc_Tss):
	csv_file = open("suc_Tss_list.csv", "w")
	cw = csv.writer(csv_file , delimiter=',', quotechar='|')

	for i in range(len(ns)):
		row = [str(int(ns[i]))]
		row.extend([ str(suc_T) for suc_T in suc_Tss[i]] )
		cw.writerow(row)
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
	plt.legend(loc = 4)
	# plt.show()
	plt.savefig('f_cluster.png')


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
	plt.legend(loc = 4)
	# plt.show()
	plt.savefig('f_sim.png')


def save_arrival_time_list(arrival_time, n):
	csv_file = open("arrival_time_n%d.csv"%n, "w")
	cw = csv.writer(csv_file , delimiter=',', quotechar='|')
	for i in range(len(arrival_time)):
		cw.writerow([str(arrival_time[i])])
	csv_file.close()

def plot_histogram(suc_Ts, n, k):
	plt.hist(suc_Ts, bins=10, color= 'b')
	plt.title('Success T for k=%d, n=%d' % (k,n))
	plt.xlabel('T')
	plt.ylabel('count')
	# plt.show()
	plt.savefig('f_T_k=%d, n=%d.png' % (k,n))