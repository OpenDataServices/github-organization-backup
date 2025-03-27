# GitHub Organization Backup

Creates a GitHub Organization Backup using the Migrations API. 

Backups all repositories in that organisation.

## To setup

Setup a Python virtual environment:

    pip install -r requirements.in 

Create a classic access token with the following scopes: 
* repo 
* admin:org

## Assumptions

This will get any backup that is there - but backups are deleted after 7 days. So don't run it more than once every 7 days :-)

Does not lock repositories, so others can carry on working on them.

## To use

To start the backup run:

    python start.py --access-token TOKEN ORG_NAME

Then when you think it will be ready, run:

    python get.py --access-token TOKEN ORG_NAME

If the backup is not ready, this will wait and keep checking.

You'll then have a backup.tar.gz file.

Extract this file:

    gzip -d backup.tar.gz

Then save the backup.tar file as appropriate.

## Trouble shooting

### requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://api.github.com/orgs/xxxxxxx/repos?per_page=100&page=1

The organisation may restrict Classic Access tokens. 

Go to organisation settings, "Personal Access tokens" then "settings" in Sidebar, "Tokens (classic)" in tab, and make sure they are allowed

