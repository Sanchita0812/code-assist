import requests
from app.utils.auth import get_github_token

def create_pull_request(owner, repo, head, base="main", title="AI Agent Code Changes", body="Changes proposed by AI agent"):
    token = get_github_token()
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code >= 300:
        raise Exception(f"Failed to create PR: {response.text}")

    return response.json()["html_url"]
