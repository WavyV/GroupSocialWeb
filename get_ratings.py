import csv
from collections import defaultdict
import pickle


# Get titles and their IDs from selected trilogies.
columns = defaultdict(list)  # each value in each column is appended to a list
with open('selected_trilogies_checked.csv', encoding='utf-8') as f:  # open desired file
    reader = csv.DictReader(f, delimiter=',')  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)  # append the value into the appropriate list  based on column name k
titles = columns['title_movieLens']  # save the movie titles
movieIDs_titles = columns['movieLensID']  # and their corresponding IDs
del columns  # clearing up some memory space

# We will be saving the ratings in the ratings nested list, but let's first set that up
# in a usable format.
ratings = []
for i in range(0, len(movieIDs_titles)):
    ratings.append([movieIDs_titles[i]])

# Get ratings and their IDs from the movieLens dataset.
with open('ratings.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        for i in range(0, len(movieIDs_titles)):
            if row[1] == movieIDs_titles[i]:
                ratings[i].append(row[2])

# Save the ratings object as a .pckl file so we can use it in another script.
f = open('ratings.pckl', 'wb')
pickle.dump(ratings, f)
f.close()

print('I AM FINALLY DONE!')