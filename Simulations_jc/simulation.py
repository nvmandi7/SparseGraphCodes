
import matplotlib; matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
from matplotlib import pyplot as plt
import numpy as np
	
#config
k = 100 # number of jobs
ns = range(int(1.0*k), int(2*k), k/10)

L = 8 # number of cores on each machine
eps = 0.0001 # failure probability of machine
singleton_fraction = 0.01
num_trials = 1000

def run_trial(n, k, L, eps, singleton_fraction):
	machine_job_degrees = []
	machine_jobs = []
	machine_success = [True for _ in range(n)]
	job_success = [False for _ in range(k)]

	# dec_seq = np.identity(n , dtype = int) # used when decoding
	# dec_ans = [(-1) for _ in range(k)]
	# job_ans = list(np.random.rand(k))


	# distribute part
	# give singleton
	for _ in range(int(np.floor(singleton_fraction * n))):
		machine_job_degrees.append(1)

	H_L = sum([1/float(i) for i in range(1,L+1)])
	# print "H_L",H_L

	# check machine degree
	c_beta = 1/sum([1/(H_L*(i-1)*i) for i in range(2, L+1)]) # normalize constant for beta

	for i in range(2,L+1):
		beta_i = c_beta * (1/(H_L*(i-1)*i)) # probability of machine with degree i
		ct_machine = int(np.floor(beta_i * n * (1 - singleton_fraction)))  # number of machines with degree i
		# print "ct_mach", ct_machine, "i", i
		for _ in range(ct_machine):
			machine_job_degrees.append(i)

	# fill remaining machines
	# print "filled by dist",len(machine_job_degrees), "/", n

	# assert len(machine_job_degrees) < n, "no place to assign singleton!"
	
	# assign any number of jobs for remaining machine
	while len(machine_job_degrees) < n:
		machine_job_degrees.append(np.random.randint(1, k+1))
	
	# while sum(machine_job_degrees) % k != 0:
	# 	machine_degrees[0] += 1  # Forces job_degree to be an integer for irregular left
	
	# assign jobs
	for job_degree in machine_job_degrees:
		machine_jobs.append(list(np.random.choice(k, job_degree, replace = False)))



	# run & decode part

	# encode job data based on job-machine graph
	# machine_enc_data = []
	# for jobs in machine_jobs:
	# 	tmp_encode = 0
	# 	for job in jobs:
	# 		tmp_encode += job_ans[job]
	# 	machine_enc_data.append(tmp_encode)
	# machine_enc_data = np.array(machine_enc_data)

	# after running, failure occurs

	# constant fraction error
	# ct_fail = int(np.floor( n * eps ))
	# for i in list(np.random.choice(n, ct_fail, replace = False)):
	# 	machine_success[i] = False
	# 	machine_jobs[i] = []

	# ..or roll the dice for every machine
	tmp_uniform = np.random.uniform(0,1,n)
	for i in range(n):
		if tmp_uniform[i] < eps:
			machine_success[i] = False
			machine_jobs[i] = []
		else:
			machine_success[i] = True


	# peeling process
	singleton_exist = True
	while singleton_exist:
		singleton_exist = False
		for m_i in range(len(machine_jobs)):
			# check singleton
			if (len(machine_jobs[m_i]) == 1):
				singleton_exist = True
				job_singleton = machine_jobs[m_i].pop()
				job_success[job_singleton] = True
				# dec_ans[job_singleton] = m_i

				#remove singleton job from other machine
				for m_i2 in range(len(machine_jobs)):
					if job_singleton in machine_jobs[m_i2]:
						machine_jobs[m_i2].remove(job_singleton)
						
						# print dec_seq, m_i2, m_i, len(machine_jobs)
						# dec_seq[m_i2] -= dec_seq[m_i] # getting to know decoding sequence

	# check all job-machine edges peeled
	if sum(len(machine) for machine in machine_jobs) == 0:
		peel_success = True 
	else:
		peel_success = False

	# check if successfully got job value
	if sum(job_success) == len(job_success):
		decode_success = True
	else:
		decode_success = False
	
	# if decode_success != decode_success2:
	# 	print "there was job not assigned?"

	# run decoding process
	# if decode_success:
	# 	# decode
	# 	job_ans2 = []
	# 	for job in range(k):
	# 		tmp_job_ans = np.dot(machine_enc_data,dec_seq[dec_ans[job]])
	# 		job_ans2.append(tmp_job_ans)
	# 	# check with answer
	# 	for job in range(k):
	# 		# print abs(job_ans[job] - job_ans2[job])
	# 		if abs(job_ans[job] - job_ans2[job]) > 0.0001:
	# 			print "Decode wrong!!!"

	return decode_success

def run_multiple_trials(num_trials, n, k, L, eps, singleton_fraction):
	# Run trial
	ct_success = 0;
	for i in range(num_trials):
		if run_trial(n, k, L, eps, singleton_fraction):
			ct_success +=1
		# if i % 100 == 0: print "running trial", i 
	success_rate = (ct_success / float(num_trials))
	print "success rate:", success_rate, "at n=", n
	return success_rate

success_rates = []
for n in ns:
	success_rates.append(run_multiple_trials(num_trials, n, k, L, eps, singleton_fraction))

ndivk = [n/float(k) for n in ns]	
plt.plot(ndivk, success_rates, label='TTT' )
plt.title('LDGM Success Rate for L=%d (Irregular Left)' % L)
plt.xlabel('Ratio of machines to jobs (n/k)')
plt.ylabel('Success Rate')
plt.legend()
# plt.show()
plt.savefig('f1.png')





