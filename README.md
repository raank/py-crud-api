## Python Crud news with user and AUTH JWT.

Install:

```shell
make install
```

- Server exposed on address: `http://0.0.0.0:5000`
- MySQL server exposed on `0.0.0.0:3306` with user `root` and pass `root`.

Manually instalation:

- Copy environment file: `cp .env.example .env;`
- Runner the docker compose: `docker-compose up -d`
- Configure database and migrations: `docker exec -it crud-backend python run.py db init;`
- Run migrations: `docker exec -it crud-backend python run.py db migrate;`
- Upgrade: `docker exec -it crud-backend python run.py db upgrade;`
- Seed admin first user: `docker exec -it crud-backend python run.py seed;`

Thanks.
