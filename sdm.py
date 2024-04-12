'''
Script for managing safeack backend docker compose deployment
'''

from argparse import ArgumentParser
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


def run_command(cmd: list[str], failed_msg: str, graceful_failed_msg: bool = True):
    '''
    pulls required images
    '''
    try:
        run(cmd, check=True)
    except CalledProcessError:
        if graceful_failed_msg:
            print(f'[!] {failed_msg}')
            exit(-1)


def get_backend_shell():
    '''
    Spawns shell for backend container
    '''
    print('[*] Spawning Backend Service Container Shell Access. Make sure containers are running')
    run_command(
        ["docker", "compose", "exec", "-it", "backend", "/bin/sh"],
        "",
        False,
    )


def pull_images():
    '''
    pulls required images
    '''
    print('[*] Pulling images')
    run_command(["docker", "compose", "pull"], 'Failed to pull images')


def stop_docker_compose():
    '''
    Stops safeack backend
    '''
    print('[*] Stopping containers')
    run_command(["docker", "compose", "down"], "Failed to stop backend docker compose")


def start_docker_compose():
    '''
    Stops safeack backend
    '''
    print('[*] Starting containers')
    run_command(["docker", "compose", "up", "-d"], "Failed to stop backend docker compose")


def migrate_db():
    '''
    migrates db
    '''
    print('[*] Migrating DB')
    run_command(
        ["docker", "compose", "run", "backend", "alembic", "upgrade", "head"],
        "Failed to migrate db",
    )


def upgrade_infra():
    '''
    upgrades
    '''
    print('[*] Upgrading SafeAck Backend')
    stop_docker_compose()
    pull_images()
    start_docker_compose()
    migrate_db()


def deploy():
    '''
    deploys safeack backend infra using docker compose
    '''
    generate_env()
    pull_images()
    start_docker_compose()
    migrate_db()


if __name__ == "__main__":
    cmd_choices = ['deploy', 'start', 'stop', 'upgrade', 'migrate', 'shell']
    parser = ArgumentParser('sdm')
    parser.add_argument(choices=cmd_choices, dest='action')

    args = parser.parse_args()

    match args.action:
        case 'start':
            start_docker_compose()
        case 'stop':
            stop_docker_compose()
        case 'upgrade':
            upgrade_infra()
        case 'migrate':
            migrate_db()
        case 'shell':
            get_backend_shell()
        case 'deploy':
            deploy()
