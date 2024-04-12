from argparse import ArgumentParser
from . import db, close_session
from ..auth.crud import create_user
from ..auth.schemas import UserCreateSchema


if __name__ == '__main__':
    parser = ArgumentParser('create_superuser')
    parser.add_argument(
        '-e', '--email', dest='email', help='email of superuser', required=True, type=str
    )
    parser.add_argument(
        '-p', '--password', dest='password', help='password for superuser', required=True, type=str
    )
    parser.add_argument(
        '-n', '--name', dest='full_name', help='Full name of superuser', required=True, type=str
    )

    args = parser.parse_args()

    full_name = args.full_name
    name_tokens = full_name.split(' ')
    first_name = name_tokens[0]
    last_name = name_tokens[1] if len(name_tokens) > 1 else 'User'

    try:
        user_data = UserCreateSchema(
            email=args.email,
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            password=args.password,
        )

        user = create_user(db, user_data, is_active=True, is_superuser=True)
        if user:
            print(f'[*] User created successfully: {user.email}')
        else:
            print(f'[!] Failed to create user: {user.email}')
    except Exception as e:
        print(f"[!] Failed to create user due to error: {e}")
    finally:
        close_session()
