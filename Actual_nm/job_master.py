from mpi4py import MPI
from job_subroutines import *
from graph_subroutines import *
import time
import sys
import numpy as np

# command line arguments
def job_master_routine(k, n, T,num_edges, rank):
	error_floor = 0.01
	output_shape = (10000) # speicfy computaional job output array shape

	comm = MPI.COMM_WORLD

	# initialization
	(machines_jobs_list, local_master_list) = read_machines_jobs_list(n, k) 

	# Broadcast machines_jobs_list data to workers
	machines_jobs_list_flat =  np.array([x for sublist in machines_jobs_list for x in sublist],dtype = np.int32 ) # flatten lsit of list	
	machines_jobs_list_sizes = np.array([len(jobs_list) for jobs_list in machines_jobs_list], dtype = np.int32)
	comm.Barrier()	
	comm.Bcast([machines_jobs_list_flat , MPI.INT], root = num_edges)
	comm.Bcast([machines_jobs_list_sizes, MPI.INT], root = num_edges)

	completed = [False for _ in range(n)]

	rcv_requests = []
	arrival_time = [-1.0 for _ in range(n)]
	machine_failed_list =[]
	encoded_data = [np.empty(output_shape, dtype=np.float32) for _ in range(n)] # to recieve from local masters

	for i in range(n):
		req = comm.Irecv([encoded_data[i], MPI.FLOAT], source=local_master_list[i], tag=1)
		rcv_requests.append(req)

	comm.Barrier()

	start_time = time.time()

	# receive all encoded data, record time received
	n_done = 0
	while n_done < n:
		for i in range(n):
			if not completed[i] and rcv_requests[i].Test():
				completed[i] = True
				arrival_time[i] = time.time() - start_time
				n_done += 1

	# check every receive process is done
	MPI.Request.Waitall(rcv_requests)


	# print arrival_time

	comm.Barrier() # end of communication
	# print arrival_time


	# get failed machine list
	for i in range(len(arrival_time)):
		if T < arrival_time[i]:
			machine_failed_list.append(i)

	save_arrival_time_list(arrival_time, n)

	# run peeling
	dec_seq, dec_ans, peel_success = \
		peel(machines_jobs_list, machine_failed_list, n, k, error_floor, get_decode_seq = True)

	# decode answers

	# print"enc data",encoded_data
	# print dec_seq
	# print dec_ans
	decoded_data = np.dot(dec_seq, encoded_data)
	# print decoded_data, dec_ans
	decoded_answers = decoded_data[dec_ans]

	print int(peel_success)   # prints to stdout as 0,1 
	# if peel_success:
	# 	print decoded_answers
	# 	pass
