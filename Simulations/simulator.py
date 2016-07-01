import numpy as np
from LDGM_code import *
from matplotlib import pyplot as plt



def run_task(t):
	t.distribute()
	t.run()
	return t.peel_successful()

def est_eps(k, n, L, T):
	t = LDGM_task(k, n, L, 1, T, True)
	trials = [run_task(t) for _ in range(10**2)]
	eps = sum(trials) / len(trials)
	print('For n/k = %f, eps=%f' % (n/k, eps))
	return eps


k = 1000; L = 64
ns = np.arange(k, 1.5*k+1, k/20)
for T in range(4, 5):
	print('\nEpsilon estimates for T=%f' % T)
	eps_lst = [est_eps(k, n, L, T) for n in ns]
	plt.plot(ns / k, eps_lst, label='T=%dmu' % T)
plt.title('LDGM Success Rate for L=%d (Irregular Left)' % L)
plt.xlabel('Ratio of machines to jobs (n/k)')
plt.ylabel('Success Rate')
plt.legend()
plt.show()