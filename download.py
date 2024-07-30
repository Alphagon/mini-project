import s3fs
import dotenv
import os

dotenv.load_dotenv()
KEY = os.environ["KEY"]
SECRET = os.environ["SECRET"]

fs = s3fs.S3FileSystem(key=KEY, secret=SECRET)
bucket = "s3://sentiment-classification-fastapi"

#files references the entire bucket.
files = fs.ls(bucket)

for file in files:
    fs.download(file,'sentiment-model.h5')