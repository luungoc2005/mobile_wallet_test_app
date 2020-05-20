1. Steps to run (on local):

Simplest: Modifying `/mobile_wallet_test/settings.py` to use SQLite database backend. Then create a new python environment, `pip install -r requirements.txt` to install dependencies then `python manage.py runserver`

Advanced: Running on minikube/microk8s
Prerequisites: Docker, minikube (microk8s), kubectl installed

  - Build the main Django app
  `docker build . -t luungoc2005/mobile-wallet-test`

  - Deploy onto minikube
  `kubectl apply -f ./k8s/local/django`
  `kubectl apply -f ./k8s/local/postgres`

2. Description

Following the requirements:

- __User access the service through an HTTP based API, with authentication.__

Users can log in through `POST http://localhost:8000/login`
```json
{
  "username": "<username here>",
  "password": "<password here>"
}
```
Subsequent requests require the `sessionid` cookies to authenticate

To register a new admin (staff role) use `python manage.py createsuperuser` (No API)
To register a normal user use `POST http://localhost:8000/users`
```json
{
  "username": "<username here>",
  "email": "<email here>",
  "password": "<password here>"
}
```

B. __User should be able to retrieve their balance.__

Users can use `POST http://localhost:8000/accounts/` to see individual account balances
```json
{
  "username": "<username here>",
  "password": "<password here>"
}
```

Additionally staff users can see `GET http://localhost:8000/users/` which offers a quick overview of user total balances (a quick sum without accounting for currencies)

C. __User should be able to send money to other users.__

Users can use `POST http://localhost:8000/transactions/` to send money from one of own accounts to another (own or other user's account).

```json
{
  "from_account": "<account id (guid string) here>",
  "to_account": "<account id (guid string) here>",
  "amount": 20
}
```

Restrictions:
- Cannot transfer more than available balance (in `from_account`)
- `from_account` must belong to the user
- `to_account` must be different from `from_account`

As a quick utility admin (staff) users can deposit money into accounts using
`POST http://localhost:8000/deposit`

```json
{
  "account_id": "<account id (guid string) here>",
  "amount": 20,
  "currency": "SGD"
}
```

As a bonus both transfer and deposit APIs supports multiple currencies by querying `exchangeratesapi.io`

D. __User should be able to retrieve the transactions that affects through the API__
Users can see own transactions (either to or from own accounts) using `GET http://localhost:8000/transactions/`

E. __The management of MobileWallet2020 would like to get regular report about the usage of the service__

The app has a crontab job that runs every (for the sake of debugging) 2 minutes or every day at 09:10 (UTC time) that generates a report (into `mobile_wallet_test/report.txt`) and upload to a Google Cloud Storage bucket

F. __MobileWallet2020 is deploying all their services with container, and are standardizing their development to utilize Python, your API needs to follow__

G. __Usually MobileWallet2020 stores their data on relational Database, but other means of storage are fine__
The app uses SQLite in development and Postgres in production (albeit using k8s persistent volume as storage). Configurable to use a cloud RDS service.

H. __You have the luxury of adding one killer feature in your app, to impress the management of the company__

- Partial support for multiple currencies (mainly during transfers)
- Web interface for API navigation

3. TODO:
- Use Celery, deployed on a separate service instead of crontab for reporting cron job
- Real support for currencies
- Use gunnicorn instead of `manage.py runserver`