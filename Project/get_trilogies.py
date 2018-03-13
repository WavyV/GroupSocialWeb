import csv
import re
from collections import defaultdict
from fuzzywuzzy import fuzz


# Get trilogy titles from Wikipedia
columns = defaultdict(list)  # each value in each column is appended to a list
with open('trilogies_wiki.csv', encoding='utf-8') as f:  # open desired file
    reader = csv.DictReader(f, delimiter=';')  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)  # append the value into the appropriate list  based on column name k
trilogies_wiki_titles = columns['title']


# Do some cleaning on the strings from the Wikipedia dataset
for i in range(0, len(columns['title'])):
    trilogies_wiki_titles[i] = re.sub("\xa0", " ", trilogies_wiki_titles[i])  # remove weird piece of string from import
    trilogies_wiki_titles[i] = re.sub("\(V\)", "", trilogies_wiki_titles[i])  # remove "(V)"
    trilogies_wiki_titles[i] = re.sub("\(TV\)", "", trilogies_wiki_titles[i])  # remove "(TV)"
    trilogies_wiki_titles[i] = trilogies_wiki_titles[i].strip()  # remove possible white space before and after string


# Get movie titles from movieLens data set
columns2 = defaultdict(list)
with open('movies_dataLens.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for (k, v) in row.items():
            columns2[k].append(v)

movieLens_titles = columns2['title']
movieLens_identifiers = columns2['movieId']

# Remove all titles with uninterpretable characters (Russian and stuff) from the movieLens data
remove_index = []
for i in range(0, len(movieLens_titles)):
    if movieLens_titles[i] is None:
        remove_index.append(i)
for i in reversed(remove_index):
    del movieLens_titles[i]
    del movieLens_identifiers[i]


# This function will select the year of publication from the movie title.
# It splits the title string in different parts using 'space' as delimiter.
# Year is always the last piece in the string, so we simply select that.
# Returning format is [[title #1, year #1], [title #2, year #2], ...].
def get_years(data):
    years = []
    for i in range(0, len(data)):
        years.append(data[i].split(' ')[-1])
    new_data = []
    for i in range(0, len(data)):
        new_data.append([data[i].strip(), years[i]])
    return new_data


# These sets contain the data we're actually going to work with.
# The data is in format [[title #1, year #1], [title #2, year #2], ...].
movieLens = get_years(movieLens_titles)
wiki_titles = get_years(trilogies_wiki_titles)


# This function retrieves all movie titles in data which have the same year of publication as
# the parameter 'year' passed to the function.
def same_year(data, year):
    movie_list = []
    for i in range(0, len(data)):
        if data[i][1] == year:
            movie_list.append(data[i])
    return movie_list


# This function compares two strings and returns their similarity ratio.
def compare(string1, string2):
    ratio = fuzz.ratio(string1, string2)
    return string2, ratio


# This is the core of the script. Here we loop through all titles in the wiki data.
# We compare the wiki title with each movieLens title published in the same year
# and save the movieLens title and corresponding movieLensID for the best possible
# similarity ratio with a minimum of ratio > 75. The returning format is as follows:
# database = [[movie_title #1, movie_title #2, movie_title #3], [mv#1, mv#2, mv#3], ...]
# where we have: movie_title = [number in trilogy, title wiki, title movieLens, movieLens ID]
# It's a double nested list.
database = []
subdata = [0, 0, 0]
for i in range(0, len(trilogies_wiki_titles)-2, 3):  # loop through trilogies
    for j in range(0, len(subdata)):  # loop through each title in the trilogy
        movies_same_year = same_year(movieLens, wiki_titles[i+j][1])  # retrieve all movies with same publication year
        movieLens_title = ''
        title_dummy = ''
        movieLensID = 0
        best_ratio = 0
        for k in range(0, len(movies_same_year)):  # find best possible match in movieLens data
            title_dummy, ratio = compare(wiki_titles[i+j][0], movies_same_year[k][0])
            if ratio > best_ratio and ratio > 75:
                best_ratio = ratio
                movieLens_title = title_dummy

        for l in range(0, len(movieLens)):  # retrieve movieLensID for best match
            if movieLens[l][0] == movieLens_title:
                movieLensID = movieLens_identifiers[l]
                break

        subdata[j] = [j+1, wiki_titles[i+j][0], movieLens_title, movieLensID]  # save data for this movie
    database.append(subdata[:])  # save data of this trilogy


# In this part we delete the trilogies from database on which we do not have complete information.
# If one of the three movies does not have a corresponding title, the entire trilogy is removed.
delete_index = []
for i in range(0, len(database)):  # loop through trilogies
    subdata = database[i]
    for j in range(0, 3):  # loop through titles in trilogy
        if subdata[j][3] == 0:  # if no match for title, remember index of trilogy to be removed
            delete_index.append(i)
            break

# Actually remove the incomplete trilogies we found in the previous part.
data_clean = database
for i in reversed(delete_index):
    del data_clean[i]


# This is a little exporting of the data.
data_print = []
for line in data_clean:
    for i in range(0, 3):
        data_print.append(line[i][0:4])

write_data = open('selected_trilogies.txt', 'w', encoding='utf-8')
for line in data_print:
    write_data.write("%s\n" % line)


