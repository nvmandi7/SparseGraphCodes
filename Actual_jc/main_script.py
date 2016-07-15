#!/usr/bin/python
from math import ceil
import subprocess
from graph_subroutines import *


#input
k = 10
ns = range(int(1.0*k), int(2*k+1), int(ceil(k/float(10))))
# ns = [4]
Ts = [5.0,7.0]
n_trial = 10
RUN_LOCAL = True
# RUN_LOCAL = False

def spawn_process_linux(machines_jobs_list, k, n, T, run_local = False, DEBUG = False):
	# DEBUG = True

	num_edges = sum([len(machines_jobs_list[i]) for i in range(len(machines_jobs_list))]) # number of total worker processes

	hostnames = ["node%03d" % (i) for i in range(1,n+1)] # hostname format for starcluster configured cluster
	
	#write hostfile for mpi to read
	host_file = open("myhosts", "w")

	for i1 in range(len(machines_jobs_list)):
		for i2 in range(len(machines_jobs_list[i1])):
			host_file.write("%s\n" % hostnames[i1])
	host_file.write("master\n")
	host_file.close()

	# run mpi processes
	if not run_local:
		# run mpi processes on cluster
		cmd_arg = [
			"mpirun.openmpi", "-mca", "rmaps", "seq", "-hostfile", "myhosts",
			"-np", str(num_edges+1), "python", "jobs_run.py", str(k), str(n), str(T), str(num_edges)
			]
		if DEBUG:
			subprocess.call(cmd_arg); out=1 # run with printing in stdout (for debug)
		else:
			proc = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = proc.communicate()
			exitcode = proc.returncode
		pass

	else:
		#run mpi process on local machine
		cmd_arg = [
			"mpirun",
			"-np", str(num_edges+1), "python", "jobs_run.py", str(k), str(n), str(T), str(num_edges)
			]
		if DEBUG:
			subprocess.call(cmd_arg); out = 1 # run with printing in stdout (for debug), fix output 1
		else:
			proc = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = proc.communicate()
			exitcode = proc.returncode

	#returns 1 if decode success, otherwise 0
	return int(out)


def run_trial(k, n, T, RUN_LOCAL):
	machines_jobs_list = distribute_jobs(n , k)
	save_machines_jobs_list(machines_jobs_list)
	return spawn_process_linux(machines_jobs_list, k, n, T, run_local = RUN_LOCAL)

def run_multiple_trials(k, n, T, n_trial, RUN_LOCAL):
	ct_success = 0
	for i in range(n_trial):
		ct_success += run_trial(k,n,T, RUN_LOCAL)
	success_rate = ct_success / float(n_trial)
	return success_rate

if RUN_LOCAL == True:
	print "Running on Local machine..."
else:
	print "Running on cluster.."	

success_rates_Ts = []
for T in Ts:
	success_rates = []
	print "running T=", T, "sec, k=", k
	for n in ns:
		success_rate = run_multiple_trials(k, n, T, n_trial, RUN_LOCAL)
		print "success_rate", success_rate, "for n/k=%f"%(n/float(k))
		success_rates.append(success_rate)
	success_rates_Ts.append(success_rates)
	save_success_rate_list(ns, success_rates, T)

# plotting part
# print success_rates_Ts
plotting(k, ns, Ts, success_rates_Ts)

