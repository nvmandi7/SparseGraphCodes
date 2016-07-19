import numpy as np
import time

def run_job_nothing(job_number):
	# time.sleep(1)
	return job_number +0.0
 

def run_job(job_number):
	# simple matrix multiplication
	n = 1000
	size = (100,100)

	for i in range(n):
		a1 = np.random.normal(0,1,size)
		b1 = np.random.normal(0,1,size)
		a1 = np.dot(a1,b1)

	# !! remember to specify output shape in job_master.py!!!
	# output should be numpy flattened!!! -> output shape should be int
	return a1.flatten()
