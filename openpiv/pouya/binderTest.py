from ipywidgets import interact
import matplotlib.pyplot as plt
import numpy as np

def plotx2(a, b):
  x=np.arange(0,10,0.1)
  y=a*(x**2)+b
  plt.plot(x,y)
  plt.axis([0,10,0,800])
  plt.title(" y = ax^2+b")
  return plt.show()
  
  interact(plotx2, a=(0,10),b=(0,500,50));
