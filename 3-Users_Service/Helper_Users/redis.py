from dotenv import load_dotenv
import redis
import os


load_dotenv('.env')

redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, decode_responses=True)


