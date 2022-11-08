build:
	cd src/svelte_site && npm install && npm run build
	sudo supervisorctl reload

build_remote: sync
	ssh btcnewstoday 'bash -ic "cd dev/btcnewstoday && make build"'

sync:
	rsync -azv . btcnewstoday:~/dev/btcnewstoday/ --delete --exclude src/svelte_site/node_modules/ --exclude src/svelte_site/build/

run:
	cd src/svelte_site && npm run dev
