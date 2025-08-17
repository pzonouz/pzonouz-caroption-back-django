start-postgres:
	docker run --name postgres --network caroption --detach --rm -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=secret	-e PGDATA=/var/lib/postgresql/data/pgdata -v "$(pwd)/database:/var/lib/postgresql/data" postgres:17.5


stop-postgres:
	docker stop postgres

start-caroption-django:
	docker run --name caroption-django --network caroption --rm -p 8000:8000 -v "./":/app django5.2-python3.13.3
stop-caroption-django:
	docker stop caroption-django



