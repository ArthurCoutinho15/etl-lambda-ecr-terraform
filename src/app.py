from handler import ApiFootballHandler, S3Handler


def lambda_handler(event, context):
    api_football = ApiFootballHandler()
    s3_handler = S3Handler()

    df = api_football.run()
    s3_handler.upload_parquet(df)

    return {
        "statusCode": 200, 
        "body": "Upload realizado com sucesso"
    }
