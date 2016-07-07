import numpy as np
from LDGM_altered import *
from matplotlib import pyplot as plt

epsilon = .01

def run_task(t):
	t.distribute()
	t.run()
	return t.peel_successful()

def est_suc(k, n, L, T):
	t = LDGM_task(k, n, L, 1, T, True, eps=epsilon)
	trials = [run_task(t) for _ in range(10**2)]
	suc = sum(trials) / len(trials)
	print('For n/k = %f, suc=%f' % (n/k, suc))
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



# 

k = 500; T = 2
ns = np.arange(k, 2*k+1, k/10)
for L in [2**i for i in range(3,6)]:
	print('\nSuccessful Decoding Probabilities for L=%f' % L)
	suc_lst = [est_suc(k, n, L, T) for n in ns]
	plt.plot(ns / k, suc_lst, label='L=%d' % L)
plt.title('LDGM Success Rate w/ epsilon=%f (Irregular Left)' % epsilon)
plt.xlabel('Ratio of machines to jobs (n/k)')
plt.ylabel('Success Rate')
plt.legend()
plt.show()