from datetime import datetime
from enum import Enum

from sqlalchemy import (
    ForeignKey,
    String,
    BigInteger,
    Enum as SAEnum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

from config import DB_URL

engine = create_async_engine(
    url=DB_URL,
    echo=True,
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class SubscriptionStatus(str, Enum):
    trial = "trial"
    active = "active"
    expired = "expired"

class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    ai_limit: Mapped[int] = mapped_column(nullable=False)
    download_limit: Mapped[int] = mapped_column(nullable=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="tariff",
        cascade="all, delete-orphan",
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )
    username: Mapped[str | None] = mapped_column(String(50))

    status: Mapped[SubscriptionStatus] = mapped_column(
        SAEnum(SubscriptionStatus),
        default=SubscriptionStatus.trial,
        nullable=False,
    )

    expires_at: Mapped[datetime | None]

    ai_used: Mapped[int] = mapped_column(default=0)
    downloads_used: Mapped[int] = mapped_column(default=0)

    tariff_id: Mapped[int | None] = mapped_column(
        ForeignKey("tariffs.id", ondelete="SET NULL")
    )
    tariff: Mapped[Tariff | None] = relationship(
        back_populates="users"
    )

async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
