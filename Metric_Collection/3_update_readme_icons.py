import os 
import re

from datetime import datetime

# Create function to get the number of views for a given repository
def get_number_of_views(repo_name):

	# Open the input file with the number of CloudFormation download for each repo
	with open("./Aggregated_Metric_Data/agg_views.csv") as file:
		agg_views = [line.rstrip() for line in file]
	file.close()

	# Match the name of the yaml file with a regex
	for line in agg_views:
 
		if re.match(repo_name + ".*", line):
			split_line = line.split(",")
			number_of_agg_views = split_line[1]

	print("Number of views for " + repo_name + ": " + str(number_of_agg_views))

	return number_of_agg_views

# Create function to get the number of unique visits for a given repository
def get_number_of_unique_visits(repo_name):

	# Open the input file with the number of CloudFormation download for each repo
	with open("./Aggregated_Metric_Data/agg_unique_visits.csv") as file:
		agg_unique_visits = [line.rstrip() for line in file]
	file.close()

	# Match the name of the yaml file with a regex
	for line in agg_unique_visits:
 
		if re.match(repo_name + ".*", line):
			split_line = line.split(",")
			number_of_agg_unique_visits = split_line[1]

	print("Number of unique visits for " + repo_name + ": " + str(number_of_agg_unique_visits))

	return number_of_agg_unique_visits

# Create function to get the icon in the read me
def update_readme_icon (repo_path, icon_type, number_to_update):

	# Git pull
	os.system("git -C " + repo_path + " pull")

	# Open the README
	with open(repo_path + "\\README.md") as README_file:
		README_lines = [line.rstrip() for line in README_file]
	README_file.close()

	new_README_lines = []

	for line in README_lines:

		# Views
		if icon_type == 'views':
			regex = r'.*<img width="\d{1,5}" alt="map-user" src="https://img.shields.io/badge/views-.*-green">.*'

			if re.match(regex, line):
				new_line = re.sub(r'(https://img.shields.io/badge/views-)\d+(-green)', r'\g<1>' + str(number_to_update) + r'\2', line)
				
				new_README_lines.append(new_line)

			else:
				new_README_lines.append(line)

		# Unique Vists
		elif icon_type == 'unique-visits':
			regex = r'.*<img width="\d{1,5}" alt="map-user" src="https://img.shields.io/badge/unique visits-.*-green">.*'

			if re.match(regex, line):
				new_line = re.sub(r'(https://img.shields.io/badge/unique visits-)\d+(-green)', r'\g<1>' + str(number_to_update) + r'\2', line)
				
				new_README_lines.append(new_line)
			
			else:
				new_README_lines.append(line)

	new_README_file = open(repo_path + "\\README.md", "w")

	for line in new_README_lines:
		new_README_file.write(line + "\n")

	new_README_file.close()

	# Git push
	os.system("git -C " + repo_path + " add .")
	os.system('git -C ' + repo_path + ' commit -m "Updating downloads"')
	os.system("git -C " + repo_path + " push")

#
repos = [
    "github-stats",

]

for repo in repos:

	views = get_number_of_views(repo)
	unique_visits = get_number_of_unique_visits(repo)

	# Format views with leading zeros
	if len(views) == 1:
		views = "00" + str(views)
	elif len(views) == 2:
		views = "0" + str(views)

	# Format unique vists with leading zero
	if len(unique_visits) == 1:
		unique_visits = "00" + str(unique_visits)
	elif len(unique_visits) == 2:
		unique_visits = "0" + str(unique_visits)

	update_readme_icon("C:\\Users\\ev290\\OneDrive\\Desktop\\GitHub\\" + repo, "views", views)
	update_readme_icon("C:\\Users\\ev290\\OneDrive\\Desktop\\GitHub\\" + repo, "unique-visits", unique_visits)
