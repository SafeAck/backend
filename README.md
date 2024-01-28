# SafeAck Backend

APIs for SafeAck Applications

## Config

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
