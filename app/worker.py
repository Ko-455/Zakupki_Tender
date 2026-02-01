import asyncio
from app.core.celery_app import celery_app
from app.services.scraper import scrape_tenders
from app.db.session import AsyncSessionLocal
from app.models.tender import Tender
from sqlalchemy.future import select
from loguru import logger
from app.bot.main import send_telegram_notification

@celery_app.task(name="app.worker.scrape_task")
def scrape_task():
    """
    Обертка для запуска асинхронного парсинга.
    """
    asyncio.run(run_scrape_cycle())

async def run_scrape_cycle():
    logger.info("Запуск цикла парсинга...")
    
    # 1. Глобальные ключевые слова
    keywords = ["инструмент строительный", "метизы", "крепеж"]
    
    async with AsyncSessionLocal() as session:
        for keyword in keywords:
            tenders = await scrape_tenders(keyword)
            
            for tender_data in tenders:
                # Проверка дублей
                stmt = select(Tender).where(Tender.zakupki_id == tender_data.zakupki_id)
                existing = await session.execute(stmt)
                if not existing.scalars().first():
                    # Сохранение нового тендера
                    new_tender = Tender(
                        zakupki_id=tender_data.zakupki_id,
                        title=tender_data.title,
                        max_price=tender_data.max_price,
                        publish_date=tender_data.publish_date,
                        customer_name=tender_data.customer_name,
                        link=tender_data.link
                    )
                    session.add(new_tender)
                    await session.commit()
                    await session.refresh(new_tender)
                    logger.info(f"Новый тендер: {new_tender.zakupki_id}")
                    
                    # Уведомление в Telegram (если настроено)
                    await send_telegram_notification(new_tender)
                else:
                    logger.info(f"Тендер существует: {tender_data.zakupki_id}")
