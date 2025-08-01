import requests
from app.utils.auth import get_github_token

def create_pull_request(owner, repo, head, base="main", title="AI Agent Code Changes", body="Changes proposed by AI agent"):
    token = get_github_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    base_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Optional: Check if a PR from this branch already exists
    existing_prs = requests.get(f"{base_url}/pulls?head={owner}:{head}&base={base}&state=open", headers=headers)
    if existing_prs.status_code == 200:
        prs = existing_prs.json()
        if prs:
            return prs[0]["html_url"]  # Return existing PR URL

    # Attempt to create a new PR
    pr_data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }

    response = requests.post(f"{base_url}/pulls", json=pr_data, headers=headers)

    if response.status_code == 404:
        raise Exception(f"[GitHub PR Error] 404 Not Found — check if '{head}' or '{base}' branch exists and your token has repo access.")
    elif response.status_code == 422:
        raise Exception(f"[GitHub PR Error] 422 Unprocessable Entity — this often means the branch was already merged or PR exists.\n{response.text}")
    elif response.status_code >= 300:
        raise Exception(f"[GitHub PR Error] {response.status_code}: {response.text}")

    return response.json()["html_url"]
