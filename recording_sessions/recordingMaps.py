import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random

width  = 17  # Fixed (x-axis)
height = 13  # Fixed (y-axis) 
depth  = 5   # Vertical layers (z-axis)

# Force positions to form a cube/parallepiped of specific legth
# Formatted as [x-length/2, y-length/2, x-increment, y-increment]
# Each number must be a multiple of 0.25
parallelepipeds = [[1.5, 1.5, 0.75, 0.75]]

n = 50 # Total number of positions per vertical layer (including random ones)

map = np.zeros((depth,height,width))
layer = []
exclude = []
toInclude = []

def populate(it):
  global toInclude, layer
  layer = []
  if it is 0:
    exclude.extend([74, 75, 76, 77, 78, 91, 92, 93, 94, 95, 108, 109, 110, 
              111, 112, 125, 126, 127, 128, 129, 142, 143, 144, 145, 146])

    for parallelepiped in parallelepipeds:
      dispX = int(parallelepiped[0]/parallelepiped[2])
      dispY = int(parallelepiped[1]/parallelepiped[3])
      multX = int(parallelepiped[2]/0.25)
      multY = int(parallelepiped[3]/0.25)
      for r in range(8-dispX*multX, 8+dispX*multX+1, multX):
        toInclude.append((6-dispY*multY)*17+r)
      for r in range(8-dispX*multX, 8+dispX*multX+1, multX):
        toInclude.append((6+dispY*multY)*17+r)
      for r in range(6-dispY*multY, 6+dispY*multY+1, multY):
        toInclude.append(r*17+(8-dispX*multX))
      for r in range(6-dispY*multY, 6+dispY*multY+1, multY):
        toInclude.append(r*17+(8+dispX*multX))
      toInclude = list(set(toInclude))

  for num in range(221):
    if (num not in exclude and num not in toInclude):
      layer.append(num)

def addInMap(pos):
  pos_x = int((pos/17)%13)
  pos_y = int(pos%17)
  map[k][pos_x][pos_y] = 1

populate(0)
if (n-len(toInclude)) <= 0:
  print("NOTE: No random points have been generated")
for k in range(depth):
  for e in range(n-len(toInclude)):
    pos = layer.pop(random.randint(0,len(layer)-1))
    addInMap(pos)
  for e in range(len(toInclude)):
    pos = toInclude[e]
    addInMap(pos)
  populate(k+1)

z,y,x = map.nonzero()


fig, ax = plt.subplots(figsize=(10, 9))
plt.title('3D view')
ax = plt.axes(projection ="3d")
ax.scatter3D(x, y, z, zdir='z', c= 'red')
ax.scatter3D(8, 6, 2, zdir='z', c="blue")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z (Layers)')
ax.set_xlim(-0.2,16.2)
ax.set_ylim(-0.2,12.2)
ax.set_zlim(-0.2,4.2)

plt.savefig("map3D.png")
plt.show()

counts = max(n,len(toInclude))
for layer in range(depth):
  xc = x[layer*counts:(layer+1)*counts]
  yc = y[layer*counts:(layer+1)*counts]
  fig, ax = plt.subplots(figsize=(10, 9))
  plt.title('Map layer'+str(layer))
  ax.grid(True)
  ax.scatter(xc, yc, c='red')
  ax.scatter(8, 6, c='blue')
  ax.set_xlim(-0.2,16.2)
  ax.set_ylim(-0.2,12.2)
  plt.savefig("map"+str(layer)+".png")
  plt.show()
  
plt.clf()
print("### Maps generated ###\n Each of the", depth,"layers has", counts,"defined positions.\n",
        "Have a good recording session!")