
import boto3, io, pandas as pd
from pandas import DataFrame
from io import StringIO


session = boto3.session.Session(profile_name="s", region_name = "us-east-1")

s3r = session.resource('s3', 'us-east-1')
bucket = "s4-bidl-dev"
prefix = 'Raw/Payments/TSYS/D256/Hold/'
bucket = s3r.Bucket(bucket)
Names = []
for object_summary in bucket.objects.filter(Prefix=prefix):
    print(object_summary.key)
    if 'TSYSO' in object_summary.key:
        Names.append(str(object_summary.key))
df = pd.DataFrame (Names)
print(df)
csv_buffer = StringIO()
df.to_csv(csv_buffer)
s3r.Object('s4-bidl-dev', 'raw/payments/payments_dev/gateway/transactions/archive/df.csv').put(Body=csv_buffer.getvalue())


'''
$ aws s3 ls s3://s4-bidl-dev/Raw/Payments/TSYS/D256/Hold/Old/ --recursive --profile s
 You need to setup an sts profile to run those commands, as well as having rbac access via IAM.
'''