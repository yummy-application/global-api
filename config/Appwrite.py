import os
from dotenv import load_dotenv
from appwrite.client import Client

load_dotenv()
APW_client = Client()
APW_client.set_endpoint('https://cloud.appwrite.io/v1')
APW_client.set_project('66ca28ea003c2ddf0db8')
APW_client.set_key(os.environ.get("APPWRITE_KEY"))