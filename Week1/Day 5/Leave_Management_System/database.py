from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./leaves.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Leave(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee = Column(String)
    start_date = Column(Date)
    days = Column(Integer)
    reason = Column(String)
    status = Column(String, default="Pending")
    approved_by = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
