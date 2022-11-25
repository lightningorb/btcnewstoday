build:
	echo 'export const API_FQDN = "https://btcnews.today";' > src/svelte_site/src/lib/constants.js
	cd src/svelte_site && npm install && npm run build
	rm -rf src/api/venv
	cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt
	sudo supervisorctl reload

build_remote: sync
	ssh btcnewstoday 'bash -ic "cd dev/btcnewstoday && make build"'

sync:
	rsync -azv . btcnewstoday:~/dev/btcnewstoday/ --delete --exclude src/svelte_site/node_modules/ --exclude src/svelte_site/build/ --exclude src/api/venv/ --exclude src/api/database.db

front:
	cd src/svelte_site && npm run dev

back:
	cd src/api && ./venv/bin/uvicorn btcnewstoday_api:app --reload

get_db:
	rsync btcnewstoday:/home/ubuntu/dev/btcnewstoday/src/api/database.db src/api/

put_db:
	rsync src/api/database.db btcnewstoday:/home/ubuntu/dev/btcnewstoday/src/api/


# @task
# def revision(c, message, env=os.environ):
#     with c.cd("server"):
#         c.run(f'alembic revision -m "{message}" --autogenerate', env=env)


# @task
# def upgrade(c, env=os.environ):
#     with c.cd("server"):
#         c.run(f"alembic upgrade head", env=env)
