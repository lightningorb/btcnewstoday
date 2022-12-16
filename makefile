build_a:
	echo 'export const API_FQDN = "https://btcnews.today";' > src/svelte_site/src/lib/constants.js
	cd src/svelte_site && npm install && npm run build
	rm -rf src/api/venv
	cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt
	sudo supervisorctl reload

build_b:
	echo "present working directory is"
	echo 'export const API_FQDN = "https://btcnews.today";' > src/svelte_site/src/lib/constants.js
	cd src/svelte_site && npm install && npm run build
	rm -rf src/api/venv
	cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt
# 	sudo supervisorctl reload


build_remote_b: sync_b
	ssh btcnewstoday 'bash -ic "cd dev/btcnewstoday_b && make build_b"'

sync_b:
	rsync -azv . btcnewstoday:~/dev/btcnewstoday_b/ --delete --exclude src/svelte_site/node_modules/ --exclude src/svelte_site/build/ --exclude src/api/venv/ --exclude src/api/database.db

front:
# 	nvm use 16.14
	. ~/.bash_profile && nvm use 16.14 && cd src/svelte_site && npm run dev

build_static:
# 	nvm use 16.14
	rm -rf build
	cd src/svelte_site && cp svelte.config.static.js src/svelte.config.js 
	cd src/svelte_site && npm run build #&& cd build && python3 -m http.server 8888

build_node:
# 	nvm use 16.14
	rm -rf build
	cd src/svelte_site && cp svelte.config.node.js src/svelte.config.js
	cd src/svelte_site && npm run build #&& cd build && python3 -m http.server 8888

install_front:
	rm -rf src/svelte_site/node_modules
	cd src/svelte_site && npm install
# 	nvm use 16.14
#	src/svelte_site/node_modules/@popperjs/core/package.json

back:
	cd src/api && ./venv/bin/uvicorn btcnewstoday_api:app --reload

get_db:
	rsync --progress bndev-us-west-2:/home/ubuntu/database.db ~/
# 	cd src/api && . venv/bin/activate && alembic upgrade head

put_db:
	rsync ~/database.db bndev-us-west-2:/home/ubuntu/


# @task
# def revision(c, message, env=os.environ):
#     with c.cd("server"):
#         c.run(f'alembic revision -m "{message}" --autogenerate', env=env)


# @task
# def upgrade(c, env=os.environ):
#     with c.cd("server"):
#         c.run(f"alembic upgrade head", env=env)
