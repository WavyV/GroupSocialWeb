# The Social Web

This is the repository of Group 10 for the project for The Social Web course at the Vrije Universiteit, Amsterdam. 

## The Data

In this project we will be analysing a dataset. The dataset we chose for this is the MovieLens 20M Dataset. This is a stable benchmark dataset with 20 million ratings and 465,000 tag applications applied to 27,000 movies by 138,000 users. The dataset has last been updated 10/2016. The permalink for download is: http://grouplens.org/datasets/movielens/20m/

## Some initial data cleaning

In order to effectively analyze the dataset we do some initial cleaning of the data in Excel. The following instructions are applicable to the file: ``movies.csv`` from the original dataset. After cleaning we rename the file to ``movies_dataLens.csv`` to try to avoid confusion. Thus, instructions: 

  1) Use ``ctrl+H`` to remove all instances of ", " (note the whitespace!) this will remove all commas from the movie titles, this is          needed because the file format is ``.csv`` and the interpreter might otherwise get confused. 
  2) Use ``ctrl+H`` to remove all instances of """ (yes, we remove all apostrophes here). 

A file for which this has been done has been placed in the "Data" folder. Moreover, we need a list of trilogies. This list has been retrieved from Wikipedia at: https://en.wikipedia.org/wiki/List_of_feature_film_series_with_three_entries and saved as ``trilogies_wiki.csv`` along with the other data in the "Data" folder. 

## Cross-referencing trilogies

Currently, after successful execution of the ``get_trilogies.py`` script a file ``selected_trilogies.txt`` is made. This file contains the trilogies of which all movies are present in the MovieLens dataset. This information has been saved along with the corresponding MovieLens MovieIDs so we can later retrieve the ratings of these movies. Some additional notes on the ``selected_trilogies.txt`` file: it still contains some errors which could not be avoided by the way the ``get_trilogies.py`` script works. Hence, after some manual checking of the results we found the following mistakes: 

  1) 
