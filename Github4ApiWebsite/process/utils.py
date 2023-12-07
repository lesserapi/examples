import requests


def checkUser(username: str) -> bool:
    status: requests.Response = requests.get(url=f'https://github.com/{username}')
    if (status.status_code == 200):
        return True
    return False


def checkBranch(username: str, repo_name: str, branch_name: str) -> bool:
    status: requests.Response = requests.get(url=f'https://github.com/{username}/{repo_name}/tree/{branch_name}')
    if (status.status_code == 200):
        return True
    return False