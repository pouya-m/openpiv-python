import numpy as np
import matplotlib.pyplot as plt
from openpiv import tools

x = np.array([[0, 1, 2],[0, 1, 2]])
y = np.array([[1,1,1],[0,0,0]])
u = np.array([[1,1,0],[1,2,-2]])
v = np.array([[1,0,-1],[2,2,1]])
mask = np.zeros(x.shape)
#plt.quiver(x, y, u, v)
#plt.show()

x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode='rotateCW')
plt.quiver(x, y, u, v)
plt.show()
