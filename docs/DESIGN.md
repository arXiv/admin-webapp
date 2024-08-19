# Overview

## Two Cookies

* **AUTH_SESSION_COOKIE_NAME**: Arxiv NG cookie uses JWT token.  
* **CLASSIC_COOKIE_NAME**: This is the original Tapir cookie

## AUTH_SESSION_COOKIE_NAME - "ARXIVNG_SESSION_ID"
This is based on JWT but the tags are not following the standard.

The cookie is encryipted and we shooud def move to this.

## CLASSIC_COOKIE_NAME - "tapir_session"

We need to ditch this ASAP.


## Storage

REDIS and database both contains the session.

### Shoud we get rid of REDIS?

tot.
