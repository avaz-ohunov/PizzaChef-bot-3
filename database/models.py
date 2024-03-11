# models.py

# Сторонние модули
from sqlalchemy import (
    Float, String, Text,
    DateTime, ForeignKey, func
)

from sqlalchemy.orm import (
    DeclarativeBase, Mapped,
    mapped_column, relationship
)


# Столбцы таблицы, которые создаются автоматически
class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(
                                DateTime,
                                default = func.now()
                            )
    
    updated: Mapped[DateTime] = mapped_column(
                                DateTime,
                                default = func.now(),
                                onupdate = func.now()
                            )


class Banner(Base):
    __tablename__ = "banner"

    banner_id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(15), unique = True)
    image: Mapped[str] = mapped_column(String(None), nullable = True)
    description: Mapped[str] = mapped_column(Text, nullable = True)


class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(150), nullable = False)


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(150), nullable = False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float(asdecimal = True), nullable = False)
    image: Mapped[str] = mapped_column(String(150))
    category_id: Mapped[int] = mapped_column(
        ForeignKey(Category.category_id, ondelete = "CASCADE"),
        nullable = False
    )

    category: Mapped["Category"] = relationship(backref = "product")


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    telegram_id: Mapped[int] = mapped_column(unique = True)
    first_name: Mapped[str] = mapped_column(String(150), nullable = False)
    last_name: Mapped[str] = mapped_column(String(150), nullable = True)
    phone: Mapped[int] = mapped_column(String(13), nullable = True)


class Cart(Base):
    __tablename__ = "cart"

    cart_id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id, ondelete = "CASCADE"),
        nullable = False
    )
    
    product_id: Mapped[int] = mapped_column(
        ForeignKey(Product.product_id, ondelete = "CASCADE"),
        nullable = False
    )
    
    quantity: Mapped[int]


    user: Mapped["User"] = relationship(backref = "cart")
    product: Mapped["Product"] = relationship(backref = "cart")
