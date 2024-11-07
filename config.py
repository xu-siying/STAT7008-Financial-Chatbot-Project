# 数据库配置 (config.py)
from pymongo import MongoClient


# MongoDB连接
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["financial_chatbot"]


