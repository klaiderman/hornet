from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

car_status = postgresql.ENUM(
    "available", "in_use", "under_maintenance", name="car_status", create_type=False
)

def upgrade() -> None:
    car_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "cars",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("model", sa.String, nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("status", car_status, nullable=False),
    )

    op.create_table(
        "rentals",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("car_id", sa.Integer, sa.ForeignKey("cars.id"), nullable=False),
        sa.Column("customer_name", sa.String, nullable=False),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=True),
    )

    op.create_index(
        "uq_open_rental_per_car",
        "rentals",
        ["car_id"],
        unique=True,
        postgresql_where=sa.text("end_date IS NULL"),
    )

def downgrade() -> None:
    op.drop_index("uq_open_rental_per_car", table_name="rentals")
    op.drop_table("rentals")
    op.drop_table("cars")
    car_status.drop(op.get_bind(), checkfirst=True)
