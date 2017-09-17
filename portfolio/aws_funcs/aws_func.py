import os
import traceback

import boto3

bucket_name = os.environ['S3_BUCKET']


def _conn_to_s3():
    print('Making connection to S3')
    try:
        return boto3.resource('s3')
    except Exception as err:
        print(err)
        traceback.print_exc()


def upload_to_s3(title, content):
    try:
        s3 = _conn_to_s3()

        print('bucket name: ', bucket_name)

        print('Uploading a post')
        s3.Object(bucket_name, title + '.md').put(Body=content)

    except Exception as e:
        print(e)


def delete_from_s3(bucket_name, file_path):
    try:
        s3 = _conn_to_s3()
        fixed_path = file_path.replace('\\', '/')
        s3.delete_object(Bucket=bucket_name, Key=fixed_path)
    except Exception as e:
        print(e)


def get_all_posts():
    p = []
    s3 = _conn_to_s3()
    b_name = s3.Bucket(bucket_name)
    for s3_file in b_name.objects.all():
        p.append(s3_file)
    return p
