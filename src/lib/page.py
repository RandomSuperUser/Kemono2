def get_cached_page(key):
    redis = get_conn()
    page = redis.get(key)
    if page is None:
        return None
    return page.decode('utf-8')

def cache_page(key, data):
    redis = get_conn()
    page = redis.set(key, data, ex = 600)
