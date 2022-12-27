# Auth0 Report

This sample app demonstrates how to show a report of applications or actions under an Auth0 tenant.

## Features

- Show a list of applications under a tenant
- Show a list of actions under a tenant
- Show a trigger of each action
- Show an applicable application of each action
- Require Auth0 login
- Require logged-in user to have "Managers" role for ACL

 
# Running the App

## Preparation on Auth0 Dashboard

- Open Auth0 Dashboad and navigate to Applications > Applications > Create Application to create a Regular Web application.
- Copy the values of Client ID, Domain, Client Secret under settings section of the application.
- Register `http://localhost:3000/callback` as `Allowed Callback URLs` and `http://localhost:3000` as `Allowed Logout URLs` in your client settings.
- Navigate to Applications > APIs > "Auth0 Management API" and open "Machine to Machine Applications" tab, then Authorize the application and assign permissions of `read:clients` and `read:actions`.
- Build a Custom Action with Post Login trigger, to add user roles to ID and Access tokens. For more details, please follow the [document](https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow#add-user-roles-to-id-and-access-tokens).
- After deploying the Action, attach it to a Login Flow.
- If you don't have `Managers` role, navigate to User Management > Roles > Create to create it and assign the role to users. Role name is case insensitive for this app.

## Running the App without Docker

- To run the sample, make sure you have `python3` and `pip` installed.
- Rename `.env.example` to `.env` and populate it with the client ID, domain, secret, callback URL and audience for your Auth0 app. If you are not implementing any API you can use `https://YOUR_DOMAIN.auth0.com/userinfo` as the audience.
- Run `pip install -r requirements.txt` to install the dependencies and run `python server.py`.
- The app will be served at [http://localhost:3000/](http://localhost:3000/).

## Running the App with Docker

- To run the sample with [Docker](https://www.docker.com/), make sure you have `docker` installed.
- Rename the `.env.example` file to `.env`, change the environment variables, and register the URLs as explained [previously](#running-the-app).
- Run `sh exec.sh` to build and run the docker image in Linux or run `.\exec.ps1` to build and run the docker image on Windows.

# Issue Reporting

If you have found a bug or if you have a feature request, please report them at this repository issues section.
Please do not report security vulnerabilities on the public GitHub issue tracker.
The [Responsible Disclosure Program](https://auth0.com/whitehat) details the procedure for disclosing security issues.

# Author

[Auth0](https://auth0.com)

# License

This project is licensed under the MIT license. See the [LICENSE](../LICENSE) file for more info.
