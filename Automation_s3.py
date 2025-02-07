import os
import glob
import boto3


def main():
    data_path = "data/*.csv"
    csv_files_path = glob.glob(data_path)

    session = boto3.Session(profile_name="Carlos")

    s3 = session.resource("s3")

    for csv_path in csv_files_path:
        file_name = os.path.basename(csv_path)
        bucket_name = f"tradedata-imat68-{file_name.rstrip('.csv')}".lower()

        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "eu-south-2"  # Region for the bucket
            },
        )

        s3_key = f"csv_uploads/{file_name}"
        s3.Bucket(bucket_name).upload_file(csv_path, s3_key)


if __name__ == "__main__":
    main()
