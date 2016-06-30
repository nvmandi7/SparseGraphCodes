import numpy as np
from LDGMCode import *
from matplotlib import pyplot as plt



def run_task(t):
	t.distribute(True)
	t.run()
	return t.peel_successful()

def est_eps(k, n, L, T):
	t = Task(k, n, L, 1, T)
	trials = [run_task(t) for _ in range(10**2)]
	eps = sum(trials) / len(trials)
	print('For n/k = %f, eps=%f' % (n/k, eps))
	return eps


k = 500; L = 32
ns = np.arange(k, 2*k+1, k/20)
for T in range(2, 6):
	print('\nEpsilon estimates for T=%f' % T)
	eps_lst = [est_eps(k, n, L, T) for n in ns]
	plt.plot(ns / k, eps_lst)
plt.title('LDGM Success Rate for L=%d (Irregular Left)' % L)
plt.xlabel('Ratio of machines to jobs (n/k)')
plt.ylabel('Success Rate')
plt.show()