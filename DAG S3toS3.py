from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from airflow.operators import S3KeySensor
from airflow.hooks import S3Hook

from datetime import datetime
from io import StringIO

s3_bucket_name = 'airflow-dag-bucket'
s3_inkey = 'input.csv'
s3_outkey = 'output.csv'

def transform_file_fn():
  hook = S3Hook()
  s3c = hook.get_conn()
  obj = s3c.get_Object(Bucket=s3_bucket_name,Key=s3_inkey)
  infileStr = obj['Body'].read().decode('utf-8')
  outfileStr=infileStr.replace('"',' ')
  outfile = StringIO(outfileStr)
  s3c.put_object(Bucket=s3_bucket_name,Key=s3_outkey,Body=outfile.getvalue())
  
with DAG(dag_id='copy-s3-file',
         schedule_interval='@once',
         start_date=datetime(2021,11,29),
         catchup=False) as dag:
  
         wait_for_file = S3KeySensor(
           task_id='wait_for_file',
           bucket_key=s3_inkey,
           bucket_name=s3_bucket_name
         )
    
         transform_file = PythonOperator(
           task_id='transform_file',
           python_callable=transform_file_fn
         )
      
         wait_for_file >> transform_file 
          
