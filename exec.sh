docker build -t auth0-report .
docker run --env-file .env -p 3000:3000 -it auth0-report
