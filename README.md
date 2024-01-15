# gitipynbcrawl

The provided Python script is designed to crawl a GitHub repository, find all Jupyter Notebook (.ipynb) files, convert them to Python (.py) files, and save the converted files to a specified output directory. Here's a step-by-step breakdown:

1. It reads a default configuration from a JSON file, which includes a GitHub URL and a token for API access.

2. It sets up an argument parser to allow command-line arguments for the GitHub URL, token, and output directory.

3. It parses the GitHub URL to extract the owner, repository name, and path.

4. It constructs the GitHub API URL for the repository contents.

5. It sends a GET request to the GitHub API to retrieve the repository contents.

6. If the request is successful, it filters the response data for .ipynb files.

7. For each .ipynb file, it downloads the file, loads it as a notebook, and filters out cells that contain 'get_ipython().system'.

8. It then converts the notebook to a .py file, excluding input and output prompts.

9. It saves the .py file to the output directory, creating the directory if it doesn't exist.

10. If the script hits the rate limit for the GitHub API, it sleeps for 60 seconds before retrying.

This script uses the `requests`, `json`, `os`, `time`, `nbconvert`, `nbformat`, and `argparse` libraries. It also requires a GitHub token for authenticated API requests.
