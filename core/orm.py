from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
class Base(DeclarativeBase):
    pass

class Regulation(Base):
    __tablename__ = "regulations"
    id: Mapped[int] = mapped_column(primary_key=True)
    cfr: Mapped[str] = mapped_column(String, nullable=False)
    product_codes: Mapped[list["ProductCode"]] = relationship(back_populates="regulation")

class ProductCode(Base):
    __tablename__ = "product_codes"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    regulation_id: Mapped[int | None] = mapped_column(ForeignKey("regulations.id"))
    regulation: Mapped["Regulation"] = relationship(back_populates="product_codes")
    devices: Mapped[list["Device"]] = relationship(back_populates="product_code")

class Device(Base):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    product_code_id: Mapped[int | None] = mapped_column(ForeignKey("product_codes.id"))
    product_code: Mapped["ProductCode"] = relationship(back_populates="devices")
    indications: Mapped[list["Indication"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )

class Indication(Base):
    __tablename__ = "indications"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    device: Mapped["Device"] = relationship(back_populates="indications")
