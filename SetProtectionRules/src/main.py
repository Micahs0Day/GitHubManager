import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")

# Set headers for API Request(s)
Headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Retrieve List of Private/Public Repos for GITHUB_USER
response_get = requests.get(f"https://api.github.com/search/repositories?q=user:{GITHUB_USER}", headers=Headers)

# Convert response to JSON
http_response = response_get.json()

## --- Protection Rules --- ##
#[1]Restrict deletions
#[2]Require a pull request before merging (Required approvals = 1)
#[3]Block force pushes

protection_rules = {
    "allow_deletions": False,
    "required_pull_request_reviews": {
        "required_approving_review_count": 0
    },
    "allow_force_pushes": False,
    "restrictions": None,
    "required_status_checks": None,
    "enforce_admins": True
    }

# For each repo's JSON obect in the "items" list, print the repo's name, then set protection rules on repo
for element in http_response["items"]:
    print(element["name"])
    repo_name = element["name"]
    response_put = requests.put(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/branches/main/protection", headers=Headers, data=json.dumps(protection_rules))
    print(response_put.status_code)
    print(response_put.reason)

