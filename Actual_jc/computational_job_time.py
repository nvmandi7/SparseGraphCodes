import time
import numpy as np

n_trial = 100

n = 1000
size = (100,100)



start_time = time.time()
for i in range(n):
	a1 = np.random.normal(0,1,size)
	b1 = np.random.normal(0,1,size)
	a1 = np.dot(a1,b1)
	# a1 += b1
run_time = time.time() - start_time

print a1
print run_time


