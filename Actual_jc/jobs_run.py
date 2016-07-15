import sys
from mpi4py import MPI
from job_worker import job_worker_routine
from job_master import job_master_routine

k = int(sys.argv[1])
n = int(sys.argv[2])
T = float(sys.argv[3]) # time to tolerate
num_edges = int(sys.argv[4])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == num_edges:
	job_master_routine(k,n,T,rank)
else:
	job_worker_routine(k,n,rank)