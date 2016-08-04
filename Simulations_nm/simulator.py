import numpy as np
from LDGM_altered import *
from matplotlib import pyplot as plt

epsilon = .1
t0 = time.time()

def run_task(t):
	t1 = time.time()
	t.distribute()
	t.run()
	# print('trial time ', time.time()-t1)
	return t.peel_successful()

def est_suc(k, n, L, T):
	t2 = time.time()
	t = LDGM_task(k, n, L, 1, T, False, eps=epsilon)
	trials = [run_task(t) for _ in range(10**2)]
	suc = sum(trials) / len(trials)
	print('For n/k = %f, suc=%f' % (n/k, suc))
	# print('time ', time.time()-t2)
	return suc


# k = 1000; L = 32
# ns = np.arange(k, 2*k+1, 20)
# for T in range(2, 3):
# 	print('\nEpsilon estimates for T=%f' % T)
# 	suc_lst = [est_suc(k, n, L, T) for n in ns]
# 	plt.plot(ns / k, suc_lst, label='T=%dmu' % T)
# plt.title('LDGM Success Rate for L=%d (Irregular Left)' % L)
# plt.xlabel('Ratio of machines to jobs (n/k)')
# plt.ylabel('Success Rate')
# plt.legend()
# plt.show()



k = 100;# T = 2
ns = np.arange(k, 2*k+1, 1)
for epsilon in [10**i for i in range(-3, -2)]:
	plt.figure()
	for L in [2**j for j in range(3,4)]:
		print('\nSuccessful Decoding Probabilities for L=%f' % L)
		suc_lst = [est_suc(k, n, L, T) for n in ns]
		plt.plot(ns / k, suc_lst, label='L=%d' % L)
		print('total time for L=%d: ' % L, time.time()-t0)
	plt.title('LDGM Success Rate w/ epsilon=%.3f, k=%d (Regular Left)' % (epsilon, k))
	plt.xlabel('Ratio of machines to jobs (n/k)')
	plt.ylabel('Success Rate')
	plt.legend()
	plt.show()
# print('total time ', time.time()-t0)