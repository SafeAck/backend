# SafeAck Backend

APIs for SafeAck Applications

-   Tests Status [![Run SafeAck API App Tests](https://github.com/SafeAck/backend/actions/workflows/python-package.yml/badge.svg)](https://github.com/SafeAck/backend/actions/workflows/python-package.yml)

## Usage 🐦‍🔥

-   Install and configure [Docker 🐋](https://docs.docker.com/get-docker/)

-   Install [python 🐍](https://www.python.org/downloads/)

-   Clone repo

    ```bash
    git clone https://github.com/SafeAck/backend.git
    ```

-   Usage SafeAck Deployment Manager script for managing deployment

    ```bash
    python sdm.py -h
    ```

-   Deploy Backend

    ```bash
    python sdm.py deploy
    ```

    > Note: use `python3` instead of `python`

-   Stop Backend

    ```bash
    python sdm.py stop
    ```

-   Start Backend. Below command needs to be used once backend has been deployed and you need to start it again.

    ```bash
    python sdm.py start
    ```

-   Upgrade Infra

    ```bash
    python sdm.py upgrade
    ```

-   Migrate Manually

    ```bash
    python sdm.py migrate
    ```

-   Get backend container shell access

    ```bash
    python sdm.py shell
    ```

## Dev

Hi 👋, If you'd like to contribute to SafeAck project then below sections are for you 😎

### Config

Update env and alembic.ini file when making changes to db

-   import newly generated model in `safeack-backend/models.py`

-   create migrations

    ```bash
    alembic revision --autogenerate -m "init"
    ```

-   apply migrations

    ```bash
    alembic upgrade head
    ```

## Shell Usage

-   Trigger shell

```bash
python -m safeack_backend.scripts.shell
```

-   Enter python or db queries

```python
from ..models import User
db.query(User).all()
```
