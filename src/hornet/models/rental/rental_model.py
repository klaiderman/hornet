from datetime import date

from sqlalchemy import ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from hornet.core.database import Base

class RentalModel(Base):
    __tablename__ = "rentals"
    __table_args__ = (
        Index(
            "uq_open_rental_per_car",
            "car_id",
            unique=True,
            postgresql_where=text("end_date IS NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date | None] = mapped_column(nullable=True)
