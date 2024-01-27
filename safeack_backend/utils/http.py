from fastapi import Request


def get_user_ip(request: Request):
    # Retrieve user's IP address from the X-Forwarded-For header
    user_ip: str | None = request.headers.get("X-Forwarded-For")

    if not user_ip:
        # If X-Forwarded-For header is not present, fallback to request.client.host
        user_ip: str = request.client.host

    return user_ip
