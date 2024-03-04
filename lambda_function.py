import json
import boto3
import platform
import hashlib

s3c = boto3.client("s3")

def print_log(*arg: tuple):
    '''ログ出力
    '''
    print(*arg)

def lambda_handler(event, context):

    print_log('start')

    # 動作環境確認
    print_log("python_version : ", platform.python_version())
    print_log("boto3.version : ", boto3.__version__)

    # S3バケット名
    src_bucket_name = 'sun-ada-bucket-tokyo'

    # S3オブジェクト名
    cpy_object_name = 'bigfile_001mb'
    #cpy_object_name = 'bigfile_010mb'
    #cpy_object_name = 'bigfile_100mb'
    #cpy_object_name = 'bigfile_500mb'
    #cpy_object_name = 'bigfile_01gb'
    #cpy_object_name = 'bigfile_02gb'
    #cpy_object_name = 'bigfile_05gb'
    #cpy_object_name = 'bigfile_08gb'
    #cpy_object_name = 'bigfile_10gb'
    #cpy_object_name = 'bigfile_20gb'

    print_log("cpy_object_name: ", cpy_object_name)

    try:
        # 方式1：S3から少しずつダウンロードしながら計算する方式（使用済みデータは捨てる）
        s3_object1 = s3c.get_object(Bucket=src_bucket_name, Key=cpy_object_name)
        md5 = hashlib.md5()
        for chunk in s3_object1["Body"].iter_chunks(chunk_size=10240):
            md5.update(chunk)
        md5_hash_value1 = md5.hexdigest().upper()
        print_log("MD5 hash value 1: ", md5_hash_value1)

        # 方式2：S3から一気に全てダウンロードして計算する方式（メモリ不足の懸念あり）
        s3_object2 = s3c.get_object(Bucket=src_bucket_name, Key=cpy_object_name)
        all_body = s3_object2["Body"].read()
        md5_hash_value2 = hashlib.md5(all_body).hexdigest().upper()
        print_log("MD5 hash value 2: ", md5_hash_value2)

        print_log('success')
        
    except Exception as e:
        print_log('error: ', e)

    finally:
        print_log('finally')
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
