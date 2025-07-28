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

    def record_user_visit(self, article_id, user_id):
        """记录用户访问，返回该用户对这篇文章的阅读次数"""
        try:
            # 记录用户到访客集合
            visitor_key = f"article:{article_id}:visitors"
            self.client.sadd(visitor_key, user_id)
            
            # 记录用户阅读次数
            user_views_key = f"article:{article_id}:user:{user_id}:views"
            user_views = self.client.incr(user_views_key)
            
            return user_views
        except Exception as e:
            print(f"Record user visit error: {e}")
            return 1

    def get_visitor_count(self, article_id):
        """获取访客数"""
        try:
            visitor_key = f"article:{article_id}:visitors"
            return self.client.scard(visitor_key)
        except Exception as e:
            print(f"Get visitor count error: {e}")
            return 0

    def get_user_views(self, article_id, user_id):
        """获取某用户对某文章的阅读次数"""
        try:
            user_views_key = f"article:{article_id}:user:{user_id}:views"
            views = self.client.get(user_views_key)
            return int(views) if views else 0
        except Exception as e:
            print(f"Get user views error: {e}")
            return 0

    def sync_views_to_db(self, article_id):
        """同步阅读量和访客数据到数据库"""
        # 同步阅读量
        cache_key = f"article:{article_id}:views"
        views = self.get(cache_key)
        if views is not None:
            try:
                article = Article.objects.get(id=article_id)
                stat, _ = ArticleReadStat.objects.get_or_create(article=article)
                stat.total_views = int(views)
                # 同时同步访客数
                stat.unique_visitors = self.get_visitor_count(article_id)
                stat.save()
            except Exception as e:
                print(f"DB sync error: {e}")

    def sync_visitors_to_db(self, article_id):
        """同步访客数据到数据库"""
        try:
            visitor_count = self.get_visitor_count(article_id)
            article = Article.objects.get(id=article_id)
            stat, _ = ArticleReadStat.objects.get_or_create(article=article)
            stat.unique_visitors = visitor_count
            stat.save()
        except Exception as e:
            print(f"Sync visitors to DB error: {e}")