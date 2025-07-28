import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.hit = 0
        self.miss = 0

    def get(self, key):
        try:
            value = self.client.get(key)
            if value is not None:
                self.hit += 1
            else:
                self.miss += 1
            return value
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    def get_hit_rate(self):
        total = self.hit + self.miss
        if total == 0:
            return 0
        return round(self.hit / total * 100, 2)

    def set(self, key, value, ex=None):
        try:
            self.client.set(key, value, ex=ex)
        except Exception as e:
            print(f"Redis set error: {e}")

    def incr(self, key):
        try:
            return self.client.incr(key)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return None
    def sync_views_to_db(self, article_id):
        cache_key = f"article:{article_id}:views"
        views = self.get(cache_key)
        if views is not None:
            try:
                article = Article.objects.get(id=article_id)
                stat, _ = ArticleReadStat.objects.get_or_create(article=article)
                stat.total_views = int(views)
                stat.save()
            except Exception as e:
                print(f"DB sync error: {e}")