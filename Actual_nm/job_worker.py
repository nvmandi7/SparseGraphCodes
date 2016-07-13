from mpi4py import MPI
from job_subroutines import *
from graph_subroutines import *
import numpy as np
import sys


k = int(sys.argv[1])
n = int(sys.argv[2])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

#initializaiton
(job_number, machine_number, local_master_rank, local_process_rank_list, global_master_rank) = \
	read_machines_jobs_list(n, k, rank) 

comm.Barrier()

# run computation
output = np.array(run_job(job_number), dtype=np.float32)

# receive, encode and send
if rank == local_master_rank:	
	output_data = [np.empty(output.shape, output.dtype) for _ in range(len(local_process_rank_list))]
	
	send_data = np.zeros(output.shape, output.dtype)
	for i in range(len(local_process_rank_list)):
		if i == 0:
			output_data[0]  = np.copy(output)
			send_data += output_data[0]
		else:
			comm.Recv([output_data[i], MPI.FLOAT], source=local_process_rank_list[i], tag=0) 
			send_data += output_data[i]
	
	# send to master
	comm.Send([send_data, MPI.FLOAT], dest=global_master_rank, tag=1) 
	
else:
	comm.Send([output, MPI.FLOAT], dest=local_master_rank, tag=0) # send to local master
	


comm.Barrier() # end of communication