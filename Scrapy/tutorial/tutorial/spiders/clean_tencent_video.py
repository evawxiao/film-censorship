# This script takes the JSON file from scraping_tencent_video_movie_info.py, cleans it, and exports it into a CSV file.

import json
import re
import csv
import sys

with open("tencent_video.json") as json_file:
	data = json.load(json_file)

with open("tencent_video.csv","a", newline='') as csv_file:

	fieldnames = ["English Title", "China Runtime", "Converted Runtime", "China Release"]
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()

	for row in range(0, len(data)):

		#convert runtime from HH:MM:SS to minutes
		if ((data[row]["china_runtime"] != None) and (len(data[row]["china_runtime"])> 0)): #if not an empty string
			convert_list = re.split(":", data[row]["china_runtime"])
			for x in range(0,len(convert_list)):
				if (x == 0):
					hours = (int(convert_list[0])*60)
				elif (x == 1):
					minutes = int(convert_list[1])

			converted_runtime = hours + minutes
		else:
			converted_runtime = "null"
			data[row]["china_runtime"] = "null"


		if (data[row]["english_title"] == None):
			data[row]["english_title"] = "null"

		if (data[row]["china_release_date"] == None):
			data[row]["china_release_date"] = "null"

		writer.writerow({"English Title": data[row]["english_title"], 
			"China Runtime": data[row]["china_runtime"], 
			"Converted Runtime": str(converted_runtime), 
			"China Release": data[row]["china_release_date"]})


