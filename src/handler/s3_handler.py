import os
from datetime import datetime
import io

import boto3
import pandas as pd


class S3Handler:
    def __init__(self):
        self.bucket = os.getenv("BUCKET_NAME")
        self.s3 = boto3.client("s3")

    def _build_key(self) -> str:
        now = datetime.utcnow()

        return (
            f"raw/football/corinthians/"
            f"year={now.year}/month={now.month:02d}/day={now.day:02d}/data.parquet"
        )

    def upload_parquet(self, df: pd.DataFrame):
        buffer = io.BytesIO()
        print(self.bucket)
        df.to_parquet(buffer, index=False)
        buffer.seek(0)

        key = self._build_key()

        self.s3.put_object(Bucket=self.bucket, Key=key, Body=buffer.getvalue())

        print(f"Upload realizado em: s3://{self.bucket}/{key}")
