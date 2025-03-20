import requests
import argparse


def _get_all_repos(organization_name, access_token):
    repo_list = []
    page = 1
    keep_going = True
    while keep_going:
        url = f"https://api.github.com/orgs/{organization_name}/repos?per_page=100&page={page}"
        r = requests.get(url, headers={"Authorization": f"token {access_token}"})
        r.raise_for_status()
        data = r.json()
        if data:
            for d in data:
                repo_list.append(d["full_name"])
        else:
            keep_going = False
        page += 1
    return repo_list


def _start_migration(organization_name, repo_list, access_token):
    url = f"https://api.github.com/orgs/{organization_name}/migrations"
    data = {
        "repositories": repo_list,
        "lock_repositories": False
    }
    r = requests.post(url, headers={"Authorization": f"token {access_token}"}, json=data)
    r.raise_for_status()
    return r.json()

def start_org_backup(organization_name, access_token):

    # The migrations API wants you to pass it a list of repos, but we just want all of them!
    # So we'll use the API to get a list of all repos, and then pass that list to the migration API
    repo_list = _get_all_repos(organization_name, access_token)

    # Now start Migration
    print(_start_migration(organization_name, repo_list, access_token))



if __name__ == "__main__":


    ap = argparse.ArgumentParser()
    ap.add_argument("organization_name", help="")
    ap.add_argument("--access-token", help="Access Token from Organisation Owner")

    args = ap.parse_args()

    start_org_backup(args.organization_name, args.access_token)

