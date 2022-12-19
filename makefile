front:
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
	rsync --progress bndev-us-east-2:/home/ubuntu/database.db ~/
# 	cd src/api && . venv/bin/activate && alembic upgrade head

put_db:
	rsync ~/database.db bndev-us-east-2:/home/ubuntu/

db_east_to_west:
	rsync --progress bndev-us-east-2:/home/ubuntu/database.db ~/
	rsync ~/database.db bndev-us-west-2:/home/ubuntu/

# @task
# def revision(c, message, env=os.environ):
#     with c.cd("server"):
#         c.run(f'alembic revision -m "{message}" --autogenerate', env=env)


# @task
# def upgrade(c, env=os.environ):
#     with c.cd("server"):
#         c.run(f"alembic upgrade head", env=env)
