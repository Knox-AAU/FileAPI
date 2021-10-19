# Dependencies

You need the following dependencies to run the program: 
- flask
- psycopg2
- python-dotenv
- pytest (Only needed for running tests)

Install these using `pip install <dependency>`

# Environment
To run the program you need an environment file called ".env" containing the relevant information in the format seen below:
```
DB_HOST=""
DATABASE=""
DB_USER=""
DB_PASSWORD=""
```

## Environment variables
The values for the environment variables should match the credentials and information based on the running setup. 
If for example the program is run locally it should match the local database credentials or the credentials for the remote server that you might SSH to.
Typically when running locally DB_HOST will be "localhost". (The port is not needed if running on the default 5432 port).