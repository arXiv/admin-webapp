# Development

## Set up

                                        User interface
                                    +-- http://localhost:4042
                                    |
            nginx                   |   backend
Browser --  http://localhost:5000 --+-- http://localhost:4041
                                    |
                                    |   oauth2 cookie maker 
                                    +-- http://localhost:20241

* nginx
 sets up the reverse proxy for the 3 endpoints to have single entry point.
 See `admin-webapp/local-setup/nginx/admin-console`

 - /admin-console  --> http://localhost:4042
 - /admin-api      --> http://localhost:4041
 - /aaa            --> http://localhost:20241
 

* User interface

This is a react-admin app.

https://github.com/marmelab/react-admin


* Backend

This is a fastapi app that serves bits to react-admin. The shape of REST API
is derived from react-admin's data provider.

* oauth2 cookie maker

Talks to Keycloak and sets up the cookies


## User interface by react-admin

There is the open source part and "Pro" - the paid version. Since we don't need
anything fancy, we'll stick to the freebie.

Underlying UI is Material UI.

So far, I have not touched any CSS. If we want to make it look like "arXiv" look
which is provided by arxiv-base's Flask/Jinja template + CSS, we have some work
to incorporate.

## Backend by FastAPI

Rather than designing the API, follow the example and match it with the frontend
which is already hashed out the pagination and usage patterns so no philosophical
idea of REST API design needed.

Adding new endpoint for react-admin resouce is VERY simple. You can copy&paste
an existing route and you are good to go.

### Business logic separation

In Tapir, UI, DTO (data transfer object) and business logic was all in one. This
made adding new features, even if it's just adding a new field on the web page
may require changing SQL statement, forming data (DTO), and logic in one -
very awkward, slow and "not easy".

react-admin forces the separation of presentation for sure. Right how, the
endpoint's DTO (control logic) and business logic are not very well separated.

There are two camps - one for cotrol/business logic separation and other for
not distinguishing. I think the latter is fine as long as the business logic is
simple.
When you have need for reusing business logic elsewhere, it makes sense to do so.
OTOH, this is a API that provides the business logic so the value of doing so is
pretty small, and most of data manipulation is straigtforward.


## oauth2-authenticator aka cookie maker

Also a FastAPI, and not a lot of feature.

The most important endpoint is /callback where Keycloak calls back for authorized
user.
