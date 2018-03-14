import numpy as np
import pickle
from matplotlib import pyplot as plt

# Import ratings.pckl file
with (open('ratings.pckl', 'rb')) as f:
    ratings_import = pickle.load(f)

# Structure the ratings object such that we can easily do stuff with the numbers.
# Structure: [[movieID #1, rating array #1], [movieID #2, rating array #2], ...]
ratings = []
for i in range(0, len(ratings_import)):
    numbers = np.zeros((1, int(len(ratings_import[i])-1)))
    for j in range(1, len(ratings_import[i])):
        numbers[0, j-1] = float(ratings_import[i][j])
    ratings.append([int(ratings_import[i][0]), numbers])

# Getting average for each movie and saving them
trilogy_averages = []
for i in range(0, len(ratings), 3):
    averages = np.zeros((1,3))
    for j in range(0, 3):
        averages[0, j] = np.average(ratings[i+j][1])
    trilogy_averages.append(averages)

print(trilogy_averages)


# Plotting some shit
x = np.array([1, 2, 3])
print(x)
for i in range(0, len(trilogy_averages)):
    for j in range(0,3):
        if np.isnan(trilogy_averages[i][0,j]) == True:
            break
        y = trilogy_averages[i][:]
        plt.plot(x, y[0])
plt.show()