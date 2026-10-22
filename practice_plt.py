import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

x = [1,2,3,4]
y = [5,6,7,8]
plt.figure(figsize=(10,10))
plt.plot(x, y)
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title("Simple Line Plot")
plt.grid(True, alpha=0.3)
plt.show()


