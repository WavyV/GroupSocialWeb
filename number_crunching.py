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
trilogy_stdev = []
trilogy_nratings = []
trilogy_deltas = []
for i in range(0, len(ratings), 3):
    averages = np.zeros((1, 3))
    stdev = np.zeros((1,3))
    nratings = np.zeros((1,3))
    deltas = np.zeros((1,3))
    for j in range(0, 3):
        averages[0, j] = np.average(ratings[i+j][1])
        stdev[0, j] = np.std(ratings[i+j][1])/np.size(ratings[i+j][1])
        nratings[0, j] = np.size(ratings[i+j][1])
    for j in range(0, 2):
        deltas[0, j] = averages[0, j+1] - averages[0, j]
    deltas[0, 2] = averages[0, 2] - averages[0, 0]

    trilogy_averages.append(averages)
    trilogy_stdev.append(stdev)
    trilogy_nratings.append(nratings)
    trilogy_deltas.append(deltas)

print(trilogy_averages)
print(trilogy_stdev)
print(trilogy_nratings)
print(trilogy_deltas)

# Plotting some shit
x = np.array([1, 2, 3])
for i in range(0, len(trilogy_averages)):
    for j in range(0, 3):
        if np.isnan(trilogy_averages[i][0, j]) == True:
            break
        y = trilogy_averages[i][:]
        plt.plot(x, y[0])
plt.show()

delta12 = []
delta23 = []
delta13 = []
for i in range(0, len(trilogy_deltas)):
    for j in range(0, 3):
        if np.isnan(trilogy_deltas[i][0, j]) == True:
            break
        if j == 0:
            delta12.append(trilogy_deltas[i][0, 0])
        if j == 1:
            delta23.append(trilogy_deltas[i][0, 1])
        if j == 2:
            delta13.append(trilogy_deltas[i][0, 2])

plt.hist(delta12)
plt.show()

plt.hist(delta23)
plt.show()

plt.hist(delta13)
plt.show()

totaltrilogies = 0
complete_decrease = 0
two_decrease_three_increase = 0
two_increase_three_increase = 0
complete_increase = 0

for i in range(0, len(trilogy_averages)):
    totaltrilogies = totaltrilogies + 1
    #rating 1 > 2 > 3
    if trilogy_averages[i][0, 0] > trilogy_averages[i][0, 1]:
        if trilogy_averages[i][0, 1] > trilogy_averages[i][0, 2]:
            complete_decrease = complete_decrease + 1
            #print(trilogy_averages[i][0, 0],trilogy_averages[i][0, 1], trilogy_averages[i][0, 2],"--> 100% decrease")
            
    #rating 1 > 2 < 3
    if trilogy_averages[i][0, 0] > trilogy_averages[i][0, 1]:
        if trilogy_averages[i][0, 1] < trilogy_averages[i][0, 2]:
            two_decrease_three_increase = two_decrease_three_increase + 1
            #print(trilogy_averages[i][0, 0],trilogy_averages[i][0, 1], trilogy_averages[i][0, 2],"--> Second movie decrease, third increase")

    #rating 1 < 2 > 3
    if trilogy_averages[i][0, 0] < trilogy_averages[i][0, 1]:
        if trilogy_averages[i][0, 1] > trilogy_averages[i][0, 2]:
            two_increase_three_increase = two_increase_three_increase + 1
            #print(trilogy_averages[i][0, 0],trilogy_averages[i][0, 1], trilogy_averages[i][0, 2],"--> Second movie increase, third decrease")

    #rating 1 < 2 < 3
    if trilogy_averages[i][0, 0] < trilogy_averages[i][0, 1]:
        if trilogy_averages[i][0, 1] < trilogy_averages[i][0, 2]:
            complete_increase = complete_increase + 1
            #print(trilogy_averages[i][0, 0], trilogy_averages[i][0, 1], trilogy_averages[i][0, 2],"--> 100% increase")

print("Total number of trilogies are", totaltrilogies)
percentage_decrease = (complete_decrease/totaltrilogies)*100
percentage_increase = (complete_increase/totaltrilogies)*100
print("Complete decrease in", complete_decrease, "trilogies, which is in", round(percentage_decrease),"% of total trilogies")
print("Complete increase in", complete_increase, "trilogies, which is in", round(percentage_increase),"% of total trilogies")
