from sqlalchemy import String, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class CampusLocation(Base):
    __tablename__ = "campus_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50)) # academic, facility, hostel, mess, medic
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
