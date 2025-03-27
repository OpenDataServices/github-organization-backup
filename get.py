import requests
import argparse
import time
import shutil
import zipfile

def _print_migrations(migrations):
    for migritation in migrations:
        print("ID: {} State: {} Created: {}".format(migritation["id"], migritation["state"], migritation["created_at"]))

def _get_exported_migration(migrations):
    for migritation in migrations:
        if migritation["state"] == "exported":
            return migritation
    return None

def _download_exported_migration(organization_name, exported_migration, access_token):
    print("Downloading exported migration")
    url = "https://api.github.com/orgs/{}/migrations/{}/archive".format(organization_name, exported_migration["id"])
    r = requests.get(url, headers={"Authorization": f"token {access_token}"}, stream=True)
    r.raise_for_status()
    with open("backup.tar.gz", "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)

def get_org_backup(organization_name, access_token):
    while True:
        print("Looking for Migrations")
        url = f"https://api.github.com/orgs/{organization_name}/migrations"
        data = {}
        r = requests.get(url, headers={"Authorization": f"token {access_token}"}, json=data)
        r.raise_for_status()
        
        migrations = r.json()

        _print_migrations(migrations)

        exported_migration = _get_exported_migration(migrations)
        if exported_migration:            
            _download_exported_migration(organization_name, exported_migration, access_token)
            return

        time.sleep(60*5)



if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("organization_name", help="")
    ap.add_argument("--access-token", help="Access Token from Organisation Owner")

    args = ap.parse_args()

    get_org_backup(args.organization_name, args.access_token)

