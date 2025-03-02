import numpy as np
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.Users import UserIn
from db_models.User import User
from db_models.News import News
from db_models.RawData import RawNews, RawUsers
from core.database import get_database
from core.logging import log
from core.bert_embeddings import get_text_embedding

router = APIRouter()


@router.post("")
def create_user(user: UserIn, db: Session = Depends(get_database)):
    db_user = User(name=user.name, read_count=0, embedding=None)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "name": db_user.name}


@router.post("/charge")
def charge_data(db: Session = Depends(get_database)):
    raw_users = db.query(RawUsers).limit(50).all()
    log.info(f"Processing {len(raw_users)} users with reading history")

    processed_users = 0
    processed_interactions = 0

    for user in raw_users:
        user_interactions = 0
        news_ids = user.history.split(",")
        for news_id in news_ids:
            try:
                user_read_news(user.id, news_id, db)
                user_interactions += 1
                processed_interactions += 1
            except Exception as e:
                log.error(
                    f"Failed to process user {user.id} reading news {news_id}: {str(e)}"
                )

        log.debug(f"User {user.id}: processed {user_interactions} reading interactions")
        processed_users += 1

    log.info(
        f"Successfully processed {processed_interactions} reading interactions for {processed_users} users"
    )

    return {
        "status": "success",
        "processed_users": processed_users,
        "processed_interactions": processed_interactions,
        "message": "User reading history successfully loaded and processed",
    }


@router.post("/{user_id}/read/{news_hash}")
def user_read_news(user_id: int, news_hash: str, db: Session = Depends(get_database)):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            log.info(
                f"User {user_id} not found, first interaction, creating new user..."
            )
            db_user = User(id=user_id, read_count=0)
            db.add(db_user)

        db_news = db.query(News).filter(News.new_hash == news_hash).first()

        if not db_news:
            db_raw_news = db.query(RawNews).filter(RawNews.page == news_hash).first()

            if db_raw_news:
                log.info(f"Processing raw news {news_hash}...")
                combined_text = db_raw_news.title + " " + db_raw_news.body
                embedding = get_text_embedding(combined_text)
                db_news = News(
                    title=db_raw_news.title,
                    text=db_raw_news.body,
                    new_hash=db_raw_news.page.strip(),
                    published_at=db_raw_news.issued,
                    embedding=embedding.tolist(),
                )

        # Log the popularity update for the news
        log.debug(
            f"Increasing popularity for news {news_hash} from {db_news.popularity} to {db_news.popularity + 1}"
        )
        db_news.popularity += 1

        # Log the embedding extraction process
        log.debug(f"Getting embedding for news {news_hash}")
        current_new_embedding = (
            np.array(db_news.embedding, dtype=np.float32)
            if db_news.embedding
            else embedding
        )

        if db_user.embedding is None:
            log.info(f"First reading for user {user_id}, initializing user embedding")
            updated_user_embedding = current_new_embedding
            incremented_news_counter = 1
        else:
            log.debug(
                f"User {user_id} has read {db_user.read_count} news before, updating embedding"
            )
            user_embedding_array = np.array(db_user.embedding, dtype=np.float32)
            incremented_news_counter = db_user.read_count + 1

            log.debug(
                f"Calculating weighted average for user {user_id}'s profile, now with {incremented_news_counter} readings"
            )
            updated_user_embedding = (
                user_embedding_array * db_user.read_count + current_new_embedding
            ) / incremented_news_counter

        log.info(
            f"Updating user {user_id} profile: read count from {db_user.read_count} to {incremented_news_counter}"
        )
        db_user.embedding = updated_user_embedding.tolist()
        db_user.read_count = incremented_news_counter

        db.commit()
        log.debug(
            f"Successfully committed user {user_id} reading news {news_hash} to database"
        )

        return {"message": f"User {user_id} read news {news_hash} - profile updated."}
    except Exception as e:
        db.rollback()

        log.error(f"Error processing user {user_id} reading news {news_hash}: {str(e)}")

        raise HTTPException(
            status_code=500, detail=f"Failed to process reading interaction: {str(e)}"
        )
