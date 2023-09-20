# Import all the models, so that Base has them before being
# imported by Alembic
from src.database.postgres.database import Base
from src.models.user import User  # noqa
