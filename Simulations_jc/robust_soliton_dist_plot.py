
import matplotlib; matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
from matplotlib import pyplot as plt
import numpy as np


k = 100
delta = 0.1
c= 0.1

R = c * np.log(k/delta) * (k**0.5)
print R

# robust Soliton distribution

dist = []
dist.append((1.0/k + R/k))


for i in range(2, int(R/k)):
	dist.append((1.0/(i*(i-1)) + R/(i*k)))
	
i = int(R/k)
print i
dist.append((1.0/(i*(i-1)) + R*(np.log(R/delta))/k))


for i in range(int(R/k)+1, k+1):
	dist.append(1.0/(i*(i-1)) )
	
print len(dist)
# for i in range(k):
# 	print dist[i]

beta = sum(dist)

for i in range(k):
	dist[i] = dist[i]/beta
	# print dist[i]


ks = [i for i in range(1,k+1)]	
plt.plot(ks, dist, label='dist' )
plt.title("Robust Soliton Sistribution")
plt.xlabel('k')
plt.ylabel('prob')
plt.legend()
# plt.show()
plt.savefig('f_rob.png')













 