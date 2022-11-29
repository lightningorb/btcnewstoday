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

## Installing node, npm and python

Currently, recommended versions are:

- node >= v12.18.3
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

