from decimal import Decimal
from sqlalchemy import (
    create_engine,
    Integer,
    Column,
    String,
    Boolean,
    ForeignKey,
    Numeric,
    func
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

# Создание движка для SQLite в памяти
engine = create_engine("sqlite:///:memory:", echo=False)

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель Category
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

# Модель Product
class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer,
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
    
    # Связь с категорией
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

def main():
    # Создание сессии
    session = SessionLocal()
    
    try:
        # Задача 1: Наполнение данными
        
        # Добавление категорий
        electronics = Category(name="Электроника", description="Гаджеты и устройства.")
        books = Category(name="Книги", description="Печатные книги и электронные книги.")
        clothing = Category(name="Одежда", description="Одежда для мужчин и женщин.")
        
        session.add_all([electronics, books, clothing])
        session.commit()
        
        # Добавление продуктов
        smartphone = Product(
            name="Смартфон",
            price=Decimal("299.99"),
            in_stock=True,
            category=electronics
        )
        laptop = Product(
            name="Ноутбук",
            price=Decimal("499.99"),
            in_stock=True,
            category=electronics
        )
        scifi_book = Product(
            name="Научно-фантастический роман",
            price=Decimal("15.99"),
            in_stock=True,
            category=books
        )
        jeans = Product(
            name="Джинсы",
            price=Decimal("40.50"),
            in_stock=True,
            category=clothing
        )
        tshirt = Product(
            name="Футболка",
            price=Decimal("20.00"),
            in_stock=True,
            category=clothing
        )
        
        session.add_all([smartphone, laptop, scifi_book, jeans, tshirt])
        session.commit()
        
        print("=== Задача 1: Данные успешно добавлены ===")
        
        # Задача 2: Чтение данных
        print("\n=== Задача 2: Чтение данных ===")
        categories = session.query(Category).all()
        
        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(f"Описание: {category.description}")
            print("Продукты:")
            for product in category.products:
                print(f"  - {product.name}: ${product.price}")
        
        # Задача 3: Обновление данных
        print("\n=== Задача 3: Обновление данных ===")
        
        # Находим первый продукт с названием "Смартфон"
        smartphone = session.query(Product).filter(Product.name == "Смартфон").first()
        if smartphone:
            old_price = smartphone.price
            smartphone.price = Decimal("349.99")
            session.commit()
            print(f"Цена смартфона обновлена: ${old_price} -> ${smartphone.price}")
        else:
            print("Смартфон не найден")
        
        # Задача 4: Агрегация и группировка
        print("\n=== Задача 4: Количество продуктов в каждой категории ===")
        
        result = session.query(
            Category.name,
            func.count(Product.id).label('product_count')
        ).join(Product).group_by(Category.id).all()
        
        for category_name, count in result:
            print(f"{category_name}: {count} продуктов")
        
        # Задача 5: Группировка с фильтрацией
        print("\n=== Задача 5: Категории с более чем одним продуктом ===")
        
        filtered_result = session.query(
            Category.name,
            func.count(Product.id).label('product_count')
        ).join(Product).group_by(Category.id).having(func.count(Product.id) > 1).all()
        
        for category_name, count in filtered_result:
            print(f"{category_name}: {count} продуктов")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        # Закрытие сессии
        session.close()

if __name__ == "__main__":
    main()