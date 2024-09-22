#
# refresh_url AAA_TOKEN_REFRESH_URL
#
async def foo(refresh_url: str, original_url: str, cookies: dict, cookie, classic_cookie, logger):

    async with httpx.AsyncClient() as client:
        refresh_response = await client.post(
            refresh_url,
            data={
                "session": cookie,
                "classic": classic_cookie,
            },
            cookies=cookies)

    if refresh_response.status_code != 200:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Failed to refresh access token"}
        )
    # Extract the new token from the response
    refreshed_tokens = await refresh_response.json()
    new_session_cookie = refreshed_tokens.get("session")
    new_classic_cookie = refreshed_tokens.get("classic")
    max_age = refreshed_tokens.get("max_age")
    domain = refreshed_tokens.get("domain")
    secure = refreshed_tokens.get("secure")
    samesite = refreshed_tokens.get("samesite")
        response.set_cookie(cookie_name, new_session_cookie,
                            max_age=max_age, domain=domain, secure=secure, samesite=samesite)
        response.set_cookie(classic_cookie_name, new_classic_cookie,
                            max_age=max_age, domain=domain, secure=secure, samesite=samesite)
        return response

    except Exception as _exc:
        logger.warning("Failed to refresh access token: %s", _exc)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Failed to refresh access token"}
        )
