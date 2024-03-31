from subprocess import run, CalledProcessError
from secrets import token_urlsafe
from textwrap import dedent


def generate_env():
    '''
    generates env file for docker deployment
    '''
    jwt_secret = token_urlsafe(64)
    jwt_algo = "HS256"
    env = "PRODUCTION"

    env_str = dedent(
        f'''
    JWT_SECRET={jwt_secret}
    JWT_ALGORITHM={jwt_algo}
    ENV={env}'''
    )

    with open("docker.env", "w", encoding="utf-8") as f:
        f.write(env_str)


def pull_images():
    '''
    pulls required images
    '''
    try:
        run(["docker", "compose", "pull"], check=True)
    except CalledProcessError:
        print('[!] Failed to pull images')
        exit(-1)


if __name__ == "__main__":
    generate_env()
