from typing import List
from sqlalchemy.future import select
from app.db.session import AsyncSessionLocal
from app.models.product import Product
from app.models.tender import Tender
from app.schemas.quote import QuoteResponse, QuoteItem
from loguru import logger

async def generate_quote_for_tender(tender_id: int) -> QuoteResponse:
    """
    Генерация КП для тендера на основе совпадения товаров.
    """
    async with AsyncSessionLocal() as session:
        # 1. Получение тендера
        result = await session.execute(select(Tender).where(Tender.id == tender_id))
        tender = result.scalars().first()
        
        if not tender:
            return QuoteResponse(tender_id=tender_id, items=[], total_price=0.0)

        # 2. Получение всех товаров (в проде нужен векторный поиск)
        result_products = await session.execute(select(Product))
        all_products = result_products.scalars().all()

        # 3. Простая логика сопоставления по ключевым словам
        matched_items = []
        total_price = 0.0
        
        tender_text_lower = (tender.title + " " + (tender.link or "")).lower()

        for product in all_products:
            # Разбиваем название товара на слова (длиной > 3)
            product_words = [w.lower() for w in product.name.split() if w.isalpha() and len(w) > 3]
            match_score = 0
            for word in product_words:
                if word in tender_text_lower:
                    match_score += 1
            
            # Эвристика: если есть совпадения
            if match_score > 0:
                item = QuoteItem(
                    product_id=product.id,
                    product_name=product.name,
                    quantity=1,
                    unit_price=product.price,
                    total=product.price
                )
                matched_items.append(item)
                total_price += product.price

        return QuoteResponse(
            tender_id=tender_id,
            tender_title=tender.title,
            items=matched_items,
            total_price=total_price
        )
