import json
from typing import List
from scrapegraphai.graphs import SmartScraperGraph
from app.core.config import settings
from app.schemas.tender import ScrapedTenderList, TenderCreate
from loguru import logger

# Конфигурация ScrapeGraphAI
graph_config = {
    "llm": {
        "api_key": settings.GOOGLE_API_KEY,
        "model": "gemini-pro",
        "temperature": 0,
    },
    "verbose": True,
    "headless": True,
}

async def scrape_tenders(keyword: str) -> List[TenderCreate]:
    """
    Парсинг zakupki.gov.ru по ключевому слову через ScrapeGraphAI.
    """
    # URL поиска (упрощенный вариант)
    search_url = f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={keyword}&morphology=on"
    
    logger.info(f"Запуск парсинга: {keyword} -> {search_url}")

    prompt = """
    Extract a list of tenders from the search results page.
    For each tender, extract:
    - zakupki_id (The number starting with №)
    - title (The description text)
    - max_price (The price with currency)
    - publish_date (The date published)
    - customer_name (The generic name of the organization)
    - link (The full href link to the tender details)
    
    Return the result as a JSON object with a key 'tenders' which is a list of these objects.
    """

    try:
        # Запуск графа
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=search_url,
            config=graph_config,
            schema=ScrapedTenderList
        )

        result = smart_scraper_graph.run()
        
        # Проверка результата
        if not result or 'tenders' not in result:
             logger.warning(f"Тендеры не найдены: {keyword}")
             return []

        # Парсинг в Pydantic
        tenders_data = result.get('tenders', [])
        # Исправление относительных ссылок
        for tender in tenders_data:
            if tender.get('link') and tender['link'].startswith('/'):
                 tender['link'] = f"https://zakupki.gov.ru{tender['link']}"

        tender_objects = [TenderCreate(**t) for t in tenders_data]
        logger.info(f"Успешно получено {len(tender_objects)} тендеров.")
        return tender_objects

    except Exception as e:
        logger.error(f"Ошибка парсинга {keyword}: {e}")
        return []
