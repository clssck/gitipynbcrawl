import requests
import json
import os
import time
from nbconvert import PythonExporter, filters
from urllib.parse import urlparse
import nbformat
import argparse

# Load default configuration from JSON file
with open('config.json') as f:
    default_config = json.load(f)

# Create the parser
parser = argparse.ArgumentParser(description='Process GitHub URL and token.')

# Add the arguments
parser.add_argument('--url', metavar='url', type=str, default=default_config['url'], help='the GitHub URL to crawl')
parser.add_argument('--token', metavar='token', type=str, default=default_config['token'], help='the GitHub token')
parser.add_argument('--output_dir', metavar='output_dir', type=str, default='output', help='the output directory for the converted Python files')

# Parse the arguments
args = parser.parse_args()

# Parse the GitHub URL
parsed_url = urlparse(args.url)
path_parts = parsed_url.path.split('/')
owner = path_parts[1]
repo = path_parts[2]
path = '/'.join(path_parts[5:])  # Changed from 4 to 5 to exclude 'tree'

# Convert web URL to API URL
api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

# GitHub API URL for repo contents
repo_api_url = api_url  # Use the provided API URL directly

# Headers for authenticated requests
headers = {'Authorization': f"token {args.token}"}

# Make a GET request to the GitHub API
r = requests.get(repo_api_url, headers=headers)

# If the GET request is successful, the status code will be 200
if r.status_code == 200:
    # Get the JSON data from the response
    data = json.loads(r.text)

    # Filter the data for .ipynb files
    ipynb_files = [file for file in data if file['name'].endswith('.ipynb')]

    print(f"Found {len(ipynb_files)} .ipynb files.")

    # For each .ipynb file
    for file in ipynb_files:
        # Download the file
        r = requests.get(file['download_url'], headers=headers)

        # Load the notebook
        notebook = nbformat.reads(r.text, as_version=4)

        # Filter out cells that contain 'get_ipython().system'
        notebook.cells = [cell for cell in notebook.cells if 'get_ipython().system' not in cell.source]

        # Convert the .ipynb file to a .py file
        exporter = PythonExporter()
        exporter.exclude_input_prompt = True
        exporter.exclude_output_prompt = True
        code, _ = exporter.from_notebook_node(notebook)

        # Create output directory if it doesn't exist
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

        # Save the .py file
        output_file = os.path.join(args.output_dir, os.path.splitext(file['name'])[0] + '.py')
        with open(output_file, 'w', encoding='utf-8') as f:  # Specify the encoding here
            f.write(code)

        print(f"Saved {output_file}.")
elif r.status_code == 429:
    # Too many requests, sleep for a while
    print("Rate limit reached. Sleeping for a while...")
    time.sleep(60)
else:
    print(f"Failed to get data from GitHub API. Status code: {r.status_code}")