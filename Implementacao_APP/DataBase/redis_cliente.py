import redis
import pickle

redis_host = 'localhost'
redis_port = 6379
redis_db = 0

r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

def set_year_data(year, data):
    r.set(f'year_data:{year}', pickle.dumps(data))

def get_year_data(year):
    data = r.get(f'year_data:{year}')
    if data:
        return pickle.loads(data)
    return None