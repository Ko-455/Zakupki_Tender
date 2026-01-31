import asyncio
import sys
import os

# Добавляем корень проекта в путь
sys.path.append(os.getcwd())

from app.db.session import AsyncSessionLocal
from app.models.product import Product
from app.db.base import Base
from sqlalchemy import select

MOCK_PRODUCTS = [
    {"name": "Makita DF333D Drill", "price": 4500.0, "category": "Power Tools"},
    {"name": "Bosch GSB 180-LI", "price": 8500.0, "category": "Power Tools"},
    {"name": "Hammer Drill DeWalt", "price": 12000.0, "category": "Power Tools"},
    {"name": "Screwdriver Set 24pcs", "price": 1200.0, "category": "Hand Tools"},
    {"name": "Concrete Screws 10x100mm (Box 100)", "price": 800.0, "category": "Consumables"},
    {"name": "Wood Screws 3.5x35mm (Box 1000)", "price": 500.0, "category": "Consumables"},
    {"name": "Cutting Disc 125mm Metal", "price": 50.0, "category": "Consumables"},
    {"name": "Diamond Blade 230mm Concrete", "price": 1500.0, "category": "Consumables"},
    {"name": "Tape Measure 5m", "price": 450.0, "category": "Measuring"},
    {"name": "Level 60cm", "price": 900.0, "category": "Measuring"},
    {"name": "Safety Gloves (Pair)", "price": 150.0, "category": "Safety"},
    {"name": "Safety Goggles", "price": 300.0, "category": "Safety"},
    {"name": "Hammer 500g", "price": 600.0, "category": "Hand Tools"},
    {"name": "Pliers Combination", "price": 550.0, "category": "Hand Tools"},
    {"name": "Wrench Adjustable 250mm", "price": 750.0, "category": "Hand Tools"},
]

async def seed_products():
    async with AsyncSessionLocal() as session:
        # Проверка наличия товаров
        result = await session.execute(select(Product))
        if result.scalars().first():
            print("Товары уже добавлены.")
            return

        print("Заполнение базы товарами...")
        new_products = [Product(**p) for p in MOCK_PRODUCTS]
        session.add_all(new_products)
        await session.commit()
        print("Готово.")

if __name__ == "__main__":
    asyncio.run(seed_products())
