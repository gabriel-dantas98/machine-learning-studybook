import os
import pandas as pd
from glob import glob
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.logging import log
from core.database import get_database

from db_models.RawData import RawUsers, RawNews

router = APIRouter()


@router.get("")
def loader(db: Session = Depends(get_database)) -> str:
    log.info("Loading raw data into database...")
    # df_train_data = get_df_cleaned_train_data()
    df_news_data = get_df_cleaned_news_data()
    log.info("Done raw data into database...")

    # train_original_count = len(df_train_data)
    news_original_count = len(df_news_data)

    # log.info(df_train_data.head())
    log.info(df_news_data.head())

    try:
        log.info(
            f"Clearing existing data from {RawUsers.__tablename__} and {RawNews.__tablename__}..."
        )
        # db.query(RawUsers).delete()
        db.query(RawNews).delete()
        db.commit()

        # log.info(
        #     f"Bulk inserting {len(df_train_data)} user records to database table {RawUsers.__tablename__}..."
        # )
        chunk_size = 5000
        # total_records = 0

        # for i in range(0, len(df_train_data), chunk_size):
        #     chunk = df_train_data.iloc[i : i + chunk_size]
        #     records = chunk.to_dict(orient="records")
        #     db.bulk_insert_mappings(RawUsers, records)
        #     db.commit()

        #     total_records += len(records)
        #     log.info(f"Committed {total_records} user records so far")

        # log.info(
        #     f"Successfully loaded {total_records} user records into {RawUsers.__tablename__}"
        # )

        log.info(
            f"Bulk inserting {len(df_news_data)} news records to database table {RawNews.__tablename__}..."
        )
        total_news_records = 0

        for i in range(0, len(df_news_data), chunk_size):
            chunk = df_news_data.iloc[i : i + chunk_size]
            records = chunk.to_dict(orient="records")
            db.bulk_insert_mappings(RawNews, records)
            db.commit()

            total_news_records += len(records)
            log.info(f"Committed {total_news_records} news records so far")

        log.info(
            f"Successfully loaded {total_news_records} news records into {RawNews.__tablename__}"
        )

        users_db_count = db.query(RawUsers).count()
        news_db_count = db.query(RawNews).count()

        log.info("Data loading summary:")
        # log.info(
        #     f"Users: Original dataset had {train_original_count} rows, {users_db_count} rows inserted into database"
        # )
        log.info(
            f"News: Original dataset had {news_original_count} rows, {news_db_count} rows inserted into database"
        )

    except Exception as e:
        db.rollback()
        log.error(f"Error uploading data to database: {str(e)}")
        raise

    return "OK Everything is loaded"


def get_df_cleaned_train_data():
    log.info("Getting training data...")

    log.info(f"Current working directory: {os.getcwd()}")

    train_files = glob(os.path.join("./datasources/train/", "treino_*.csv"))
    log.info(f"Found {len(train_files)} training files: {train_files}")

    dfs_train = []
    for file in train_files:
        df_train_part = pd.read_csv(file)
        dfs_train.append(df_train_part)
        log.info(f"Read {file}, shape: {df_train_part.shape}")

    df_train = pd.concat(dfs_train, ignore_index=True)
    log.info(f"Combined training dataframe shape: {df_train.shape}")
    log.info(df_train.head())

    dup_train = df_train.duplicated().sum()
    log.info(f"Duplicate rows in training data: {dup_train}")

    log.info("Training data info:")
    log.info(df_train.info())

    # Summary statistics
    log.info("Training data summary statistics:")
    log.info(df_train.describe())

    log.info("Null values in training data:")
    log.info(df_train.isnull().sum())

    log.info(
        f"Training data (df_train): {df_train.shape} rows, {df_train.columns.tolist()}"
    )

    return df_train


def get_df_cleaned_news_data():
    log.info("Getting news data...")
    news_files = glob(os.path.join("./datasources/news", "itens-*.csv"))
    log.info(f"Found {len(news_files)} news files: {news_files}")

    dfs_news = []
    for file in news_files:
        df_news_part = pd.read_csv(file)
        dfs_news.append(df_news_part)
        log.info(f"Read {file}, shape: {df_news_part.shape}")

    df_news = pd.concat(dfs_news, ignore_index=True)
    log.info(f"Combined news dataframe shape: {df_news.shape}")
    log.info(df_news.head())

    log.info("Summary of dataframes:")
    log.info(
        f"News data (df_news): {df_news.shape} rows, {df_news.columns.tolist() if 'df_news' in locals() else 'not loaded'}"
    )

    log.info("Performing news data cleaning and preparation...")
    df_news_clean = df_news.copy()

    log.info("Number of null values per column:")
    log.info(df_news_clean.isnull().sum())

    # Convert timestamp columns to datetime
    df_news_clean["issued"] = pd.to_datetime(df_news_clean["issued"])
    df_news_clean["modified"] = pd.to_datetime(df_news_clean["modified"])

    # Getting more features

    df_news_clean["title_length"] = df_news_clean["title"].apply(
        lambda x: len(x) if isinstance(x, str) else 0
    )
    df_news_clean["body_length"] = df_news_clean["body"].apply(
        lambda x: len(x) if isinstance(x, str) else 0
    )

    df_news_clean["issued_year"] = df_news_clean["issued"].dt.year.astype("int32")
    df_news_clean["issued_month"] = df_news_clean["issued"].dt.month.astype("int32")

    # Text body processing (remove extra line breaks)
    df_news_clean["body"] = df_news_clean["body"].str.replace("\n", " ", regex=False)

    log.info("Dataframe information after cleaning:")
    log.info(df_news_clean.info())

    log.info("Statistics after cleaning:")
    log.info(df_news_clean.describe())

    log.info("First rows of the cleaned dataframe:")
    log.info(df_news_clean.head())

    log.info(f"Final dimensions of the cleaned dataframe: {df_news_clean.shape}")

    log.info(
        f"News data (df_news_clean): {df_news_clean.shape} rows, {df_news_clean.columns.tolist() if 'df_news_clean' in locals() else 'not loaded'}"
    )

    return df_news_clean
