import math
import numpy as np
from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db_models.User import User
from db_models.News import News
from core.database import get_database
from core.bert_embeddings import cosine_similarity
from core.logging import log

router = APIRouter()


@router.get("/similar/{user_id}")
def recommend_similar(
    user_id: int, limit: int = 5, db: Session = Depends(get_database)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.embedding is None:
        raise HTTPException(status_code=400, detail="User has no reading history")

    user_emb = db_user.embedding
    query = db.query(News)

    query = query.order_by(News.embedding.op("<=>")(user_emb)).limit(limit)
    results = query.all()

    return [{"id": n.id, "title": n.title, "url": n.url} for n in results]


@router.get("/trending/{user_id}")
def recommend_trending(
    user_id: int, limit: int = 5, db: Session = Depends(get_database)
):
    log.info(f"Requesting trending recommendations for user_id={user_id}")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        log.warning(f"User with id={user_id} not found")

    # Handle cold-start: user embedding might be None for new users without reading history
    user_emb = None
    if db_user is not None and db_user.embedding is not None:
        user_emb = np.array(db_user.embedding, dtype=np.float32)
        log.info(f"User {user_id} has embedding data - personalization will be applied")
    else:
        log.info(
            f"Cold-start scenario detected: User {user_id} has no embedding data or user not found - using popularity and recency only"
        )

    # Get all news candidates from the database
    query = db.query(News)
    candidates = query.all()
    log.info(f"Found {len(candidates)} news candidates for recommendation")

    now = datetime.utcnow()
    scored = []

    # Score each news item based on multiple factors
    log.info("Calculating scores for news items")
    for i, news in enumerate(candidates):
        if i % 100 == 0 and i > 0:
            log.debug(f"Processed {i}/{len(candidates)} news items...")

        # Extract news embedding for similarity calculation
        news_emb = np.array(news.embedding, dtype=np.float32)

        # Calculate similarity score only if user has embedding (non-cold-start)
        sim_score = 0.0
        if user_emb is not None:
            sim_score = cosine_similarity(user_emb, news_emb)

        # Popularity score (log scale to dampen extreme values)
        pop_score = math.log10(news.popularity + 1)

        # Recency score (linear decay over 30 days)
        age_days = (now - news.published_at).total_seconds() / 86400.0
        recency_score = max(0, (30 - age_days) / 30) if age_days < 30 else 0.0

        # Adjust weights based on cold-start scenario
        if user_emb is None:
            # Cold-start: rely more on popularity and recency since we don't have user preferences
            total_score = 0.7 * pop_score + 0.3 * recency_score
            if i < 5:  # Log only a few examples to avoid flooding
                log.debug(
                    f"Cold-start scoring for news {news.id}: pop={pop_score:.2f}, recency={recency_score:.2f}, total={total_score:.2f}"
                )
        else:
            # Normal case: consider user preferences along with popularity and recency
            total_score = 0.5 * sim_score + 0.3 * pop_score + 0.2 * recency_score
            if i < 5:  # Log only a few examples to avoid flooding
                log.debug(
                    f"Regular scoring for news {news.id}: sim={sim_score:.2f}, pop={pop_score:.2f}, recency={recency_score:.2f}, total={total_score:.2f}"
                )

        scored.append((total_score, news))

    # Sort by score (descending) and take top results
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:limit]

    # Return the recommended items
    log.info(f"Returning {len(top)} trending recommendations for user {user_id}")
    if user_emb is None:
        log.info(
            "Recommendations based on popularity and recency (cold-start strategy)"
        )
    else:
        log.info("Recommendations based on user similarity, popularity, and recency")

    return [{"id": n.id, "title": n.title, "url": n.url} for (score, n) in top]
