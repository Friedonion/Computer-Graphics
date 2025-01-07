import numpy as np

M = np.arange(2,27)
print(M,end="\n\n")
M=M.reshape(5,5)
print(M,end="\n\n")
for i in range(1,4):
	for j in range(1,4):
		M[i][j]=0
print(M,end="\n\n")
M=M@M
print(M,end="\n\n")
v = M[0,:]
v = v*v;
a = 0
for i in range(0,5):
	a+=v[i]
print(np.sqrt(a))




