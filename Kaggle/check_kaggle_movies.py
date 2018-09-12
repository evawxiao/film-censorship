# This Python script merges Kaggle and Tencent Video movie data. Because movies sometimes go by different titles, especially on 
# Tencent Video, I've only included films that appear by the same name in both datasets. This cuts out about 800 movies.

# Kaggle data (movies_metadata.csv) important headers by row number: 
# 0 budget
# 1 genres
# 2 original_title
# 3 production_companies	
# 4 production_countries	
# 5 release_date	
# 6 revenue	
# 7 runtime	

import csv
import re
import codecs
import json

tencent_movies = {}

# store tencent movie data into a dictionary
with open("tencent_video.csv", "r") as csv_tencent_info:
	tencent_csv_reader = csv.reader(csv_tencent_info)
	for row in tencent_csv_reader:
		tencent_value = row[0:len(row)] #row should be a list of comma separated values <-- string?
		tencent_key = row[0] # key should be name of movie
		tencent_movies[tencent_key] = tencent_value

kaggle_movies = {}

# store Kaggle data into dictionary
with open("movies_metadata.csv", "r", errors='replace') as kaggle_info:
	kaggle_reader = csv.reader(kaggle_info)
	for row in kaggle_reader:

		try:
			production_country = re.search(r"United States of America", row[4]) # check US movies only for now
				
			if(production_country != None):
				kaggle_value = [] 

				# add budget info
				kaggle_value.append(row[0])

				# add genre tags
				genre_list = re.findall(r'[A-Z]{1}[a-z]+', row[1])
				joined_genres = ""

				for genre in genre_list:
					joined_genres = joined_genres + str(genre) + " ;" # CSV file splits columns by commas...

				kaggle_value.append(joined_genres)

				# add production companies
				companies = re.findall(r'[A-Z]{1}[A-Za-z ]+', row[3])
				joined_companies = ""

				for company in companies:
					joined_companies = joined_companies + str(company) + " ;" # CSV file splits columns by commas...

				kaggle_value.append(joined_companies)

				# add release date
				kaggle_value.append(row[5])

				# add revenue
				kaggle_value.append(row[6])

				# add runtime
				kaggle_value.append(row[7])

				kaggle_key = row[2] # should be 'original_title' field
				kaggle_movies[kaggle_key] = kaggle_value
		except IndexError:
			pass

problematic_movies = [] # use this to track movies that aren't in both Tencent and Kaggle datasets

# merge entries
for movie in tencent_movies:
	if (movie in kaggle_movies):
		tencent_movies[movie] = tencent_movies[movie] + kaggle_movies[movie] 
	else:
		problematic_movies.append(movie)

for movie in problematic_movies:
	del(tencent_movies[movie])

final_writer = csv.writer(open("tencent_kaggle_min_subset.csv", "w", newline=''))

# write to new CSV file
for movie in tencent_movies:
	final_writer.writerow(tencent_movies[movie])

# output list of problematic films
problem_writer = open("tencent_kaggle_problems.txt", "a")

with problem_writer:
	for movie in problematic_movies:
		bad_movie = movie + '\n'
		problem_writer.write(bad_movie)