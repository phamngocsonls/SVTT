import boto
import boto.s3.connection
access_key = 'CKHF33D2EGWIRNJPEPO3'
secret_key = 'kiDbAMjuDBEGbQD8ckH63B943zRLXLKB3qDy8IPT'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 'rgw1',
        port = 80,
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

bucket = conn.create_bucket('my-new-bucket')
for bucket in conn.get_all_buckets():
    print "{name}  {created}".format(name=bucket.name, created=bucket.creation_date)
