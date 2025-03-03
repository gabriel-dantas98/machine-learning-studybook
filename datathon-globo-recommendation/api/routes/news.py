import asyncio
from fastapi import APIRouter
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_database
from core.bert_embeddings import get_text_embedding
from core.logging import log

from db_models.News import News
from db_models.RawData import RawNews
from schemas.News import NewsIn

router = APIRouter()


@router.post("/charge")
async def charge_data(db: Session = Depends(get_database)):
    raw_news = db.query(RawNews).filter(RawNews.issued_year > 2020).limit(50).all()
    print(f"Found {len(raw_news)} raw news entries to process")

    async def process_news(raw_news_item):
        try:
            combined_text = raw_news_item.title + " " + raw_news_item.body

            # Run the CPU-bound operation in a thread to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None, get_text_embedding, combined_text
            )
            log.info(f"Generated embedding for news {raw_news_item.id}")

            return {
                "title": raw_news_item.title,
                "new_hash": raw_news_item.page.strip(),
                "text": raw_news_item.body,
                "url": raw_news_item.url,
                "published_at": datetime.utcnow(),
                "popularity": 0,
                "embedding": embedding.tolist(),
                "success": True,
            }
        except Exception as e:
            print(f"Error processing news {raw_news_item.id}: {str(e)}")
            return {"success": False, "id": raw_news_item.id, "error": str(e)}

    tasks = [process_news(item) for item in raw_news]
    results = await asyncio.gather(*tasks)

    processed_items = []
    error_count = 0
    for result in results:
        if result["success"]:
            processed_items.append(result)
        else:
            error_count += 1

    if processed_items:
        news_objects = [
            News(
                title=item["title"],
                text=item["text"],
                new_hash=item["new_hash"],
                url=item["url"],
                published_at=item["published_at"],
                popularity=item["popularity"],
                embedding=item["embedding"],
            )
            for item in processed_items
        ]

        print(f"Bulk inserting {len(news_objects)} news items...")
        db.bulk_save_objects(news_objects)
        db.commit()

    return {
        "message": "Data loading completed",
        "total_processed": len(processed_items),
        "total_errors": error_count,
        "total_found": len(raw_news),
    }


@router.post("")
def add_news(item: NewsIn, db: Session = Depends(get_database)):
    try:
        print(f"Processing news article: '{item.title[:30]}...'")

        new_input = item.title + " " + item.text

        emb = get_text_embedding(new_input)

        news = News(
            title=item.title,
            text=item.text,
            published_at=datetime.utcnow(),
            popularity=0,
            embedding=emb.tolist(),  # pgvector accepts lists of floats
        )

        print("Saving news to database...")
        db.add(news)
        db.commit()
        db.refresh(news)

        print(f"Successfully added news with ID: {news.id}")

        return {"id": news.id, "title": news.title}
    except Exception as e:
        print(f"Error adding news article: {str(e)}")
        db.rollback()
        raise
