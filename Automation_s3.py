import os
import glob
import boto3


def main():
    data_path = "data/*.csv"
    csv_files_path = glob.glob(data_path)
    print(csv_files_path)

    session = boto3.Session(profile_name="Carlos")

    s3 = session.resource("s3")

    for csv_path in csv_files_path:
        file_name = os.path.basename(csv_path)

        s3_key = f"csv_uploads/{file_name}"
        s3.Bucket("tradedata-imat-68-aaa-automation-testing").upload_file(
            csv_path, s3_key
        )


if __name__ == "__main__":
    main()
