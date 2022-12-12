# BTCNews.Today
"Come for the news, stay for the low time-preference.™" 🌟

## Cloning

First you'll need to generate a token in Github:

Settings > Developer Settings > Personal Access Token > Tokens (classic)

Then generate a token with all access.

Then use this token in the URL to clone:

```
git clone https://[YOUR_TOKEN]@github.com/lightningorb/btcnewstoday.git
cd btcnewstoday
repo_root=`pwd`
```

## Provisioning a new host

```
src/admin/deploy_fresh.sh
```

## Installing node, npm and python

Currently, recommended versions are:

- node >=16.14
- npm >= 6.14.6
- python >= 3.8


## Installing frontend dependencies

```
cd ${repo_root}/src/svelte_site
npm install
```

## Installing backend dependencies

```
cd ${repo_root}/src/api
python3 -m virtualenv venv
. venv/bin/activate
```

## Running locally

```
cd ${repo_root}
make front
```

In a new terminal:

```
cd ${repo_root}
make back
```

### Setting up a reverse proxy

Since we're using both node and fastapi / uvicorn, we use a reverse proxy to serve the site, which also avoids the incredible amount of pain associated with CORS. `brew install nginx` / `sudo apt-get install nginx` then set up the following server:

```
server {
 proxy_read_timeout 5m;

 listen 80;
 location / {
  proxy_pass http://127.0.0.1:5173;
   proxy_http_version 1.1;
     proxy_set_header Upgrade $http_upgrade;
     proxy_set_header Connection "upgrade";
 }
 location /api/ {
  proxy_pass http://127.0.0.1:8000;
 }
 location /docs/ {
  proxy_pass http://127.0.0.1:8000/docs/;
 }
 location /token/ {
  proxy_pass http://127.0.0.1:8000/api/token;
 }
 location /openapi.json {
  proxy_pass http://127.0.0.1:8000;
 }
}
```

### Secrets

The site uses a bunch of secrets, currently for the Twitter API, but there may be more to come. Just ask another dev for the secrets.py file, and save it in `src/api`.


### SSH access to the server

Add the following to your `~/.ssh/config`

```
Host btcnewstoday
    Hostname 52.15.149.220
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/btcnewstoday.cer
```

Then ask for dev for `btcnewstoday.cer` and save it in `~/.ssh/btcnewstoday.cer` then `chmod 400 ~/.ssh/btcnewstoday.cer`.

### Getting the production database

Currently we're using a simple sqlite database. This reduces time spent on DB admin, makes backups super easy, as well as upgrades, restoring etc.

sqlite is fine for sites with less than 100k requests per day. Once the site grows, we'll need to move to something more production oriented like postgres.

```
cd ${repo_root}
make get_db
```

The db lives in:

```
src/api/database.db
```

Take a look at it with something like: https://sqlitebrowser.org/

### Modifying the DB schema

Make the changes you need in `src/api/models.py` then run:

```
cd ${repo_root}/src/api
python3 -m virtualenv venv
. venv/bin/activate
alembic revision -m "my message here" --autogenerate
```

Check the newly generated migration script in `src/api/alembic/versions/` and try the upgrade with:

```
alembic upgrade head
```

### Deploying the DB

If the migration was successful, you can push the db back to the server:

```
cd ${repo_root}
make put_db
```

### Deploying

Once you're ready to deploy our changes:

```
cd ${repo_root}
make build_remote
```

Or check your changes into a branch, and ask another dev to review and deploy.