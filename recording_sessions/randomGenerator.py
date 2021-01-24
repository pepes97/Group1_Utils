import matplotlib.pyplot as plt
import matplotlib
from matplotlib import collections  as mc
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
from python_tsp.distances import euclidean_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming

#np.random.seed = 42

x_positions = np.arange(-2, 2.01, 0.25)
y_positions = np.arange(-1.5, 1.51, 0.25)
z_positions = np.arange(1, 6)

print(x_positions)
print(y_positions)
print(z_positions)

samples = []

def insertCube(half_edge_x, half_edge_y, step_x, step_y):
    assert half_edge_x%step_x==0
    assert half_edge_y%step_y==0

    x_positions = np.arange(-half_edge_x, half_edge_x+0.01, step_x)
    y_positions = np.arange(-half_edge_y, half_edge_y+0.01, step_y)
    z_positions = np.arange(1, 6)
    samples = []
    for x in x_positions:
        for y in y_positions:
            if np.abs(x)==half_edge_x or np.abs(y)==half_edge_y:
                for z in z_positions:
                    samples += [(x,y,z)]

    samples.sort(key= lambda x: (x[2], -np.arctan2(x[1], x[0])))
    return samples

def insertRhombus(step):
    
    x_positions = np.arange(-1.5, 1.5+0.01, step)
    y_positions = np.arange(-1.5, 1.5+0.01, step)
    z_positions = np.arange(1, 6)
    samples = []
    for x in x_positions:
        for y in y_positions:
            if x>=0 and y>=0 and y==1.5-x:
                for z in z_positions:
                    samples += [(x,y,z)]
            if x>=0 and y<0 and y==-1.5+x:
                for z in z_positions:
                    samples += [(x,y,z)]
            if x<0 and y>=0 and y==1.5+x:
                for z in z_positions:
                    samples += [(x,y,z)]
            if x<0 and y<0 and y==-1.5-x:
                for z in z_positions:
                    samples += [(x,y,z)]
    samples.sort(key= lambda x: (x[2], -np.arctan2(x[1], x[0])))
    return samples


def plot_layers(samples, name):
    layers = []
    for heigth in range(1,6):

        random_samples_layer = [s for s in samples if s[2]==heigth]
        random_samples_layer.sort(key= lambda x: (x[0],x[1]))
        sources = [[s[0], s[1]] for s in random_samples_layer]
        #sources.sort(key= lambda x: (x[0],x[1]))
        sources = np.array(sources)
        distance_matrix = euclidean_distance_matrix(sources)

        distance_matrix[:, 0] = 0
        permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
        
        random_samples_layer = [random_samples_layer[i] for i in permutation]
        fig, ax = plt.subplots(figsize=(10, 9))
        plt.title(f'2D view height: {heigth}')
        ax = plt.axes()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_xlim(-2.6,2.6)
        ax.set_ylim(-2.1,2.1)

        xs = []
        ys = []
        x_positions = np.arange(-2, 2.01, 0.25)
        y_positions = np.arange(-1.5, 1.51, 0.25)
        for x in x_positions:
            for y in y_positions:
                if np.abs(x)<0.75 and np.abs(y)<0.75:
                    continue
                else:
                    xs += [x]
                    ys += [y]

        ax.scatter(xs, ys, c= 'gray')    

        x = [s[0] for s in random_samples_layer]
        y = [s[1] for s in random_samples_layer]

        ax.scatter(x, y, c= 'red')

        lines = []
        for i, p in enumerate(permutation[:-1]):
            lines += [[(sources[permutation[i]][0], sources[permutation[i]][1]), (sources[permutation[i+1]][0], sources[permutation[i+1]][1])]]

        lc = mc.LineCollection(lines, colors='b', linewidths=2)
        ax.add_collection(lc)
        lines = [[(-2.5, -2), (-2.5, 2)], [(-2.5, 2),(2.5, 2)],[(2.5, 2),(2.5, -2)]]
        lc = mc.LineCollection(lines, colors='gray', linewidths=2)
        ax.add_collection(lc)
        lines = [[(-2.5, -2), (2.5, -2)]]
        lc = mc.LineCollection(lines, colors='cyan', linewidths=2)
        ax.add_collection(lc)
        lines = [[(1, 2), (2, 2)]]
        lc = mc.LineCollection(lines, colors='brown', linewidths=5)
        ax.add_collection(lc)
        plt.savefig(name+f"_heigth_{heigth}.png")
        layers += random_samples_layer
    return layers

def add_n_random_samples(n, samples_to_avoid):
    x_positions = np.arange(-2, 2.01, 0.25)
    y_positions = np.arange(-1.5, 1.51, 0.25)
    z_positions = np.arange(1, 6)
    n_random_samples = n
    random_samples = []

    while len(random_samples)< n_random_samples:
        x_index = np.random.randint(len(x_positions))
        y_index = np.random.randint(len(y_positions))
        z_index = int(len(random_samples)/(n_random_samples/len(z_positions)))

        x = x_positions[x_index]
        y = y_positions[y_index]
        z = z_positions[z_index]

        if np.abs(x)<0.75 and np.abs(y)<0.75:
            continue
        elif (x,y,z) not in samples_to_avoid and (x,y,z) not in random_samples:
            random_samples += [(x,y,z)]
    return random_samples

def writeCSV(list_of_samples):
    
    with open('positions.csv', 'w', newline='') as file:
        file.write("X, Y, Z\n")
        for s in list_of_samples:
            file.write(f"{s[0]}, {s[1]}, {s[2]}\n")
        

samples_cube1 = insertCube(1.5, 1.5, 0.5, 0.5)
samples_cube2 = insertCube(1, 1, 0.5, 0.5)
#samples_rhombus = insertRhombus(0.5)

total_samples = samples_cube1 + samples_cube2

random_samples1 = add_n_random_samples(80, samples)
total_samples += random_samples1


fig, ax = plt.subplots(figsize=(10, 9))
plt.title('3D view')
ax = plt.axes(projection ="3d")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z (Layers)')


x = [s[0] for s in total_samples]
y = [s[1] for s in total_samples]
z = [s[2] for s in total_samples]

ax.scatter3D(x, y, z, zdir='z', c='red')
plt.savefig("map3D.png")
#plt.show()

random_samples1 = plot_layers(random_samples1, "random80")
#print(random_samples1)
total_samples = samples_cube1 + samples_cube2 + random_samples1

writeCSV(total_samples)

plt.show()