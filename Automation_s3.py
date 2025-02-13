import os
import glob
import boto3
import pandas as pd


def main():
    data_path = "data/*.csv"
    csv_files_path = glob.glob(data_path)

    session = boto3.Session(profile_name="Carlos")

    s3 = session.resource("s3")

    os.makedirs("tmp", exist_ok=True)

    for csv_path in csv_files_path:
        coin_name = os.path.basename(csv_path)
        bucket_name = f"tradedata-imat68-{coin_name.rstrip('.csv')}".lower()

        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "eu-south-2"  # Region for the bucket
            },
        )

        df = pd.read_csv(csv_path, parse_dates=["datetime"])
        df["year"] = df["datetime"].dt.year

        for year, year_df in df.groupby("year"):
            year_file_path = f"tmp/{coin_name}_{year}.csv"
            year_df.drop(columns=["year"]).to_csv(year_file_path, index=False)

            s3_key = f"csv_uploads/{year}/{coin_name}"
            s3.Bucket(bucket_name).upload_file(year_file_path, s3_key)

        print("Bucket created and csv uploades correctly")


if __name__ == "__main__":
    main()
