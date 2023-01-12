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
	cd src/api && ./venv/bin/uvicorn btcnewstoday_api:app --reload --workers 3

rev:
	. src/api/venv/bin/activate && cd src/api/ && alembic revision -m "withdrawals" --autogenerate

upgrade:
	. src/api/venv/bin/activate && cd src/api/ && alembic upgrade head && python3 migrate.py

test:
	. src/api/venv/bin/activate && cd src/api/ && ./bn init-db && ./bn drop && ./bn fix-db-keys
	pytest src/build_system/tests/test_bounties.py -s --full-trace -vv

test_bounties:
	pytest src/build_system/tests/test_bounties.py -s --full-trace -vv