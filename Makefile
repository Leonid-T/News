build:
	docker-compose -f docker-compose.yml build $(c)
rebuild:
	docker-compose -f docker-compose.yml down --rmi all -v $(c)
	docker-compose -f docker-compose.yml up -d $(c)
up:
	docker-compose -f docker-compose.yml up -d $(c)
start:
	docker-compose -f docker-compose.yml start $(c)
down:
	docker-compose -f docker-compose.yml down $(c)
destroy:
	docker-compose -f docker-compose.yml down --rmi all -v $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
logs:
	docker-compose -f docker-compose.yml logs --tail=100 -f $(c)
ps:
	docker-compose -f docker-compose.yml ps
start-server:
	docker-compose -f docker-compose.yml start server $(c)
stop-server:
	docker-compose -f docker-compose.yml stop server $(c)
start-postgres:
	docker-compose -f docker-compose.yml start postgres $(c)
stop-postgres:
	docker-compose -f docker-compose.yml stop postgres $(c)