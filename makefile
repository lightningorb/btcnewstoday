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


install_back:
	rm -rf src/api/venv
	cd src/api && python3 -m virtualenv venv
	. src/api/venv/bin/activate && pip3 install -r requirements.txt

back:
	cd src/api && ./venv/bin/uvicorn btcnewstoday_api:app --reload

get_db:
	rsync --progress bndev-us-east-2:/home/ubuntu/database.db ~/
# 	cd src/api && . venv/bin/activate && alembic upgrade head

# put_db:
# 	rsync ~/database.db bndev-us-east-2:/home/ubuntu/

db_east_to_west:
	rsync --progress bndev-us-east-2:/home/ubuntu/database.db ~/
	rsync ~/database.db bndev-us-west-2:/home/ubuntu/

db_west_to_east:
	rsync --progress bndev-us-west-2:/home/ubuntu/database.db ~/
	rsync ~/database.db bndev-us-east-2:/home/ubuntu/

rev:
	. src/api/venv/bin/activate && cd src/api/ && alembic revision -m "meta" --autogenerate


upgrade:
	alembic upgrade head
