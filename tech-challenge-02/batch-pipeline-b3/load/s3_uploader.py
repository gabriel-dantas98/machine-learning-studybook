#!/bin/python3

import boto3
import os
import logging
from datetime import datetime
import pandas as pd
from botocore.exceptions import NoCredentialsError, ClientError


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def remove_second_line(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        if "Tipo" in line or "Redutor" in line or "Total" in line or "IBOV" in line:
            lines.pop(index)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)


def upload_file_to_s3(file_name, bucket_name, object_name=None, region="us-east-1"):
  aws_access_key_id = ""
  aws_secret_access_key = ""
  aws_session_token = ""

  if object_name is None:
      object_name = file_name

  s3_client = boto3.client(
      "s3",
      region_name=region,
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      aws_session_token=aws_session_token,
  )

  try:
    s3_client.head_bucket(Bucket=bucket_name)
  except ClientError:
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
    except ClientError as e:
        logging.error(e)
        return False

  print(f"Removendo a segunda linha do arquivo {file_name}.")
  remove_second_line(file_name)

  print(f"Transformando o {file_name} em parquet...")

  df = pd.read_csv(file_name, encoding="utf-8", delimiter=";")
  df.columns = ["cod", "acao", "tipo", "quantidade", "part", "other"]
  df["quantidade"].str.replace(".", "").astype("int64")
  df["part"] = df["part"].str.replace(",", ".").astype("float")
  df["data_extracao"] = datetime.now()

  parquet_file = f"./raw/b3-{get_current_date()}.parquet"

  print("primeira coluna")
  primeira_coluna = df.iloc[:, 0]
  print(primeira_coluna.head())

  print("ultima coluna")
  ultima_coluna = df.iloc[:, -2]
  print(ultima_coluna.head())

  print("top 10")
  print(df.head(10))

  if not os.path.exists(parquet_file):
      open(parquet_file, "w").close()

  parquet_df = df.to_parquet(parquet_file)
  print(parquet_df)

  s3_client.upload_file(parquet_file, bucket_name, f'raw/b3-{get_current_date()}.parquet')

  print(
      f"Arquivo {parquet_file} enviado para o bucket {bucket_name} com sucesso."
  )
  return True


upload_file_to_s3("../extract/IBOVDia_29-07-24.csv", "gd-ibov-data")
