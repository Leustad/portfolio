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


def delete_from_s3(title):
    try:
        s3 = _conn_to_s3()
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().filter(Prefix=title + '.md').delete()
    except Exception as e:
        print(e)


def get_all_posts():
    p = []
    s3 = _conn_to_s3()
    b_name = s3.Bucket(bucket_name)

    for s3_file in sorted(b_name.objects.all(), key=lambda k: k.last_modified, reverse=True):
        p.append(s3_file)
    return p


def get_single_post(title):
    s3 = _conn_to_s3()
    bucket = s3.Bucket(bucket_name)
    obj = bucket.objects.all().filter(Prefix=title)
    for o in obj:
        return o.key, o.get()['Body'].read().decode('utf-8')
