
clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	@if [ -d "migrations" ]; then \
		docker-compose up -d; \
	else \
		cp .env.example .env; \
		docker-compose up -d; \
		docker exec -it crud-backend python run.py db init; \
		docker exec -it crud-backend python run.py db migrate; \
		docker exec -it crud-backend python run.py db upgrade; \
		docker exec -it crud-backend python run.py seed; \
	fi

build:
	@docker-compose up -d
	@docker exec -it crud-backend python run.py db migrate
	@docker exec -it crud-backend python run.py db upgrade
