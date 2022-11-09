build:
	echo 'export const API_FQDN = "https://btcnews.today";' > src/svelte_site/src/lib/constants.js
	cd src/svelte_site && npm install && npm run build
	rm -rf src/api/venv
	cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt
	sudo supervisorctl reload

build_remote: sync
	ssh btcnewstoday 'bash -ic "cd dev/btcnewstoday && make build"'

sync:
	rsync -azv . btcnewstoday:~/dev/btcnewstoday/ --delete --exclude src/svelte_site/node_modules/ --exclude src/svelte_site/build/

run:
	cd src/svelte_site && npm run dev
