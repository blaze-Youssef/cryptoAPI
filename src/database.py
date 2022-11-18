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

from .conf import get_settings

SQLALCHEMY_DATABASE_URL: str = get_settings("SQLALCHEMY_DATABASE_URL")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  #
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
)
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
            "frequency",
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
    frequency = Column(Integer, nullable=False)


class Asseteth(Base):
    __tablename__ = "eth"
    __table_args__ = (
        UniqueConstraint(
            "time_period_start",
            "time_period_end",
            "symbol_id",
            "frequency",
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
    frequency = Column(Integer, nullable=False)


class Assetsol(Base):
    __tablename__ = "sol"
    __table_args__ = (
        UniqueConstraint(
            "time_period_start",
            "time_period_end",
            "symbol_id",
            "frequency",
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
    frequency = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)
