from github import Github
from github import Auth
import requests
import os
from dotenv import load_dotenv
import pandas as pd

# Load token var from .env file
load_dotenv()
personal_access_token = os.getenv('personal_access_token')

# Create Github obj
g = Github(personal_access_token)
repo = g.get_repo("DonneyF/ubc-pair-grade-data")

# Get the contents of the UBCO and UBCV directories
ubco_contents = repo.get_contents("tableau-dashboard-v2/UBCO")
ubcv_contents = repo.get_contents("tableau-dashboard-v2/UBCV")

cols_to_keep = ['Year', 'Session', 'Subject', 'Course', 'Title', 'Professor']  # The columns I need data from

ubco_json_path = 'ubco_data.json'
ubcv_json_path = 'ubcv_data.json'

# Iterate through the tableau-dashboard-v2 directory, get the links to the raw CSV data for each class, convert the data to JSON, and write it to a JSON file
index = 0
while index < len(ubco_contents):
    ubco_file_content = ubco_contents[index]
    if ubco_file_content.type == "file":
        # read the CSV data from the current CSV file
        df = pd.read_csv(ubco_file_content.download_url)
        df_subset = df[cols_to_keep]
        df_subset.to_json(ubco_json_path, orient='records', lines=True, mode='a')
    elif ubco_file_content.type == "dir":
        ubco_contents.extend(repo.get_contents(ubco_file_content.path))
    index += 1

index = 0
while index < len(ubcv_contents):
    ubcv_file_content = ubcv_contents[index]
    if ubcv_file_content.type == "file":
        # read the CSV data from the current CSV file
        df = pd.read_csv(ubcv_file_content.download_url)
        df_subset = df[cols_to_keep]
        df_subset.to_json(ubcv_json_path, orient='records', lines=True, mode='a')
    elif ubcv_file_content.type == "dir":
        ubcv_contents.extend(repo.get_contents(ubcv_file_content.path))
    index += 1