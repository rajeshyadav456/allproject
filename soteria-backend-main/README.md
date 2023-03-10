# Soteria Backend

### Requirements
1. Python 3.8+ (Recommended 3.8.10 or later)
1. [Poetry](https://github.com/python-poetry/poetry#installation)
1. [Postgresql 12+](https://www.postgresql.org/download/)
1. [Pyenv](https://stackoverflow.com/a/62743443)
1. [Django Tenants](https://django-tenants.readthedocs.io/en/latest/)


## Setup PostgreSQL Database
1. Login into the `psql` shell
    ```bash
    $ sudo -u postgres psql
    ```
2. Create user and database on PostgreSQL
    ```
    postgres=# CREATE DATABASE db_name;
    postgres=# CREATE USER user_name WITH PASSWORD 'password';
    postgres=# GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;
    ```

3. Create following postgres extensions
    ```
    postgres=# CREATE EXTENSION IF NOT EXISTS postgis;
    postgres=# CREATE EXTENSION IF NOT EXISTS btree_gist;
    ```

## Instructions
1. Create a virtual environment of name `.venv` in project root directory
    ```bash
    $ virtualenv --python=python3.8 .venv
    ```
2. Activate virtual environment
    ```bash
   $ source .venv/bin/activate
   ```
3. Install project dependencies. 
    ```bash
    $ poetry install
    ```
4. Create environment variables file copy of `.env.example`  for an environment 
    * `.env.development` - for development
    * `.env.staging` - for staging
    * `.env.production` - for production
5. Apply database migrations
    ```bash
    $ python manage.py migrate
    ```
6. To collect static files of django project
    ```bash
    $ python manage.py collectstatic
    ```
7. Run application
    ```bash
    $ python manage.py runserver

## Setup Tenants

1. Firstly create a public `Tenant` (Fresh Setup Only)
    ```bash
    $ python manage.py create_tenant 

2. Create your own `Tenant` 
   ```bash
   $ python manage.py create_tenant

3. To migrate changes
   ```bash
   $ python manage.py migrate_schemas
