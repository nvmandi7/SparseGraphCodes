#!/usr/bin/python
from math import ceil
import subprocess
from graph_subroutines import *
import time


#input
k = 5
# ns = range(int(1.0*k), int(2*k+1), int(ceil(k/float(3))))
ns = [10]
n_trial = 10
fail_rate_limit = 0.2

RUN_LOCAL = True
# RUN_LOCAL = False

def spawn_process_linux(machines_jobs_list, k, n, run_local = False, DEBUG = False):
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
			"-np", str(num_edges+1), "python", "jobs_run.py", str(k), str(n), str(num_edges)
			]
		if DEBUG:
			subprocess.call(cmd_arg); out=1.0 # run with printing in stdout (for debug)
		else:
			proc = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = proc.communicate()
			exitcode = proc.returncode
		pass

	else:
		#run mpi process on local machine
		cmd_arg = [
			"mpirun",
			"-np", str(num_edges+1), "python", "jobs_run.py", str(k), str(n), str(num_edges)
			]
		if DEBUG:
			subprocess.call(cmd_arg); out = 1.0 # run with printing in stdout (for debug), fix output 1
		else:
			proc = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = proc.communicate()
			exitcode = proc.returncode

	#returns 1 if decode success, otherwise 0
	return float(out)


def run_trial(k, n, RUN_LOCAL):
	machines_jobs_list = distribute_jobs(n , k)
	save_machines_jobs_list(machines_jobs_list)
	return spawn_process_linux(machines_jobs_list, k, n, run_local = RUN_LOCAL)

def run_multiple_trials(k, n, n_trial, RUN_LOCAL):
	suc_Ts = []
	for i in range(n_trial):
		suc_Ts.append( run_trial(k,n, RUN_LOCAL) )
	return suc_Ts
	

if RUN_LOCAL == True:
	print "Running T on Local machine..."
else:
	print "Running T on cluster.."	

suc_Tss = []
fail_rates = []
print "running k=", k
for n in ns:
	start_time = time.time()
	suc_Ts = run_multiple_trials(k, n, n_trial, RUN_LOCAL)
	run_time = time.time() - start_time
	fail_rate = sum([1 for suc_T in suc_Ts if suc_T < 0]) / float(n_trial)
	print "for n/k=%.2f" % (n/float(k)), ",fail rate:", fail_rate , "took %.2f "%run_time , "sec"
	fail_rates.append(fail_rate)
	suc_Tss.append(suc_Ts)
save_suc_Tss_list(ns, suc_Tss)

# plotting histgram
for i in range(len(ns)):
	if fail_rates[i] < fail_rate_limit:
		plot_histogram(suc_Tss[i], k, n)

