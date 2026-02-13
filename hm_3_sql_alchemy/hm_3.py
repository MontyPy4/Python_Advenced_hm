from decimal import Decimal
from sqlalchemy import (
    create_engine,
    BigInteger,
    Column,
    String,
    SmallInteger,
    Boolean,
    ForeignKey,
    Numeric,
    Integer
)

from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

# Абстрактный базовый класс для всех моделей
class Base(DeclarativeBase):
    __abstract__ = True

# Задача 1: Создание движка для SQLite в памяти
engine = create_engine("sqlite:///:memory:", echo=True)

# Задача 2: Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Задача 4: Модель Category
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(255)
    )

    # Связь с продуктами
    products = relationship(
        'Product',
        back_populates='category'
    )

# Задача 3: Модель Product
class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    in_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    
    # Задача 5: Связь с категорией
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'),
        nullable=False
    )
    
    # Обратная связь
    category = relationship(
        'Category',
        back_populates='products'
    )

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Пример использования
if __name__ == "__main__":
    # Создание категории
    electronics = Category(
        name="Electronics",
        description="Electronic devices and gadgets"
    )
    
    # Создание продукта
    laptop = Product(
        name="Laptop",
        price=Decimal("999.99"),
        in_stock=True,
        category=electronics
    )
    
    # Добавление в сессию и коммит
    session.add(electronics)
    session.add(laptop)
    session.commit()
    
    # Проверка
    product = session.query(Product).first()
    print(f"Product: {product.name}, Category: {product.category.name}")
    
    # Закрытие сессии
    session.close()
