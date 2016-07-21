from mpi4py import MPI
from job_subroutines import *
from graph_subroutines import *
import numpy as np
import sys


def job_worker_routine(k, n, num_edges, rank):
	comm = MPI.COMM_WORLD

	#initializaiton

	#receive machine_jobs_list data from master
	machines_jobs_list_flat = np.empty(num_edges, np.int32)
	machines_jobs_list_sizes = np.empty(n, np.int32)
	comm.Barrier()
	comm.Bcast([machines_jobs_list_flat, MPI.INT], root = num_edges)
	comm.Bcast([machines_jobs_list_sizes, MPI.INT], root = num_edges)
	
	machines_jobs_list =  get_machines_jobs_list(machines_jobs_list_flat, machines_jobs_list_sizes)
	job_number, local_master_rank, local_process_rank_list = \
		get_worker_info_from_machines_jobs_list(n,k,machines_jobs_list, rank)
	comm.Barrier()

	# run computation
	# output = np.array(run_job(job_number), dtype=np.float32)
	output = np.array(run_job_nothing(job_number), dtype=np.float32)

	# receive, encode and send
	if rank == local_master_rank:	
		output_data = [np.empty(output.shape, output.dtype) for _ in range(len(local_process_rank_list))]
		
		send_data = np.zeros(output.shape, output.dtype)

		rcv_requests = []
		for i in range(1, len(local_process_rank_list)):
			req = comm.Irecv([output_data[i], MPI.FLOAT], source=local_process_rank_list[i], tag=0)
			rcv_requests.append(req)
		MPI.Request.Waitall(rcv_requests)


		for i in range(len(local_process_rank_list)):
			if i == 0:
				output_data[0]  = np.copy(output)
				send_data += output_data[0]
			else:
				send_data += output_data[i]
		
		# send to master
		comm.Send([send_data, MPI.FLOAT], dest=num_edges, tag=1) 
		
	else:
		comm.Send([output, MPI.FLOAT], dest=local_master_rank, tag=0) # send to local master

	comm.Barrier() # end of communication

