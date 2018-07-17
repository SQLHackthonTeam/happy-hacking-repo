
import numpy as np
import matplotlib.pyplot as plt
import sys

N=int(sys.argv[1])
weights=np.ones(N)/N
print("WEIGHTS",weights)

c=np.loadtxt('/home/syd/Documents/stockdata.csv',delimiter=',',
skiprows=(2),usecols=(2,),unpack=True)
sam=np.convolve(weights,c)[N-1:-N+1]
t=np.arange(N-1,len(c))

plt.plot(t,c[N-1:],lw=1.0)
plt.plot(t,sam,lw=2.0)
plt.show()