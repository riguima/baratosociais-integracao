from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from baratosociais_integracao.database import db


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int]


Base.metadata.create_all(db)
