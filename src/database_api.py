from sqlalchemy import (
    FLOAT,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from .conf import get_settings

SQLALCHEMY_DATABASE_URL = get_settings("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
scoped_Session = scoped_session(SessionLocal)
Base = declarative_base()


class Assetbtc(Base):
    __tablename__ = "btc"
    __table_args__ = (
        UniqueConstraint(
            "time_period_start",
            "time_period_end",
            "symbol_id",
            name="unique_timedeltas",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(String(30), nullable=False)
    time_period_start = Column(DateTime, nullable=False)
    time_period_end = Column(DateTime, nullable=False)
    time_open = Column(DateTime, nullable=False)
    time_close = Column(DateTime, nullable=False)
    price_open = Column(FLOAT, nullable=False)
    price_high = Column(FLOAT, nullable=False)
    price_low = Column(FLOAT, nullable=False)
    price_close = Column(FLOAT, nullable=False)
    volume_traded = Column(FLOAT, nullable=False)
    trades_count = Column(Integer, nullable=False)


class Asseteth(Base):
    __tablename__ = "eth"
    __table_args__ = (
        UniqueConstraint(
            "time_period_start",
            "time_period_end",
            "symbol_id",
            name="unique_timedeltas",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(String(30), nullable=False)
    time_period_start = Column(DateTime, nullable=False)
    time_period_end = Column(DateTime, nullable=False)
    time_open = Column(DateTime, nullable=False)
    time_close = Column(DateTime, nullable=False)
    price_open = Column(FLOAT, nullable=False)
    price_high = Column(FLOAT, nullable=False)
    price_low = Column(FLOAT, nullable=False)
    price_close = Column(FLOAT, nullable=False)
    volume_traded = Column(FLOAT, nullable=False)
    trades_count = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)
