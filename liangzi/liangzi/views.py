from django.shortcuts import render, get_object_or_404
from .models import Article, ArticleReadStat
from .cache import RedisClient

redis_client = RedisClient()

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    cache_key = f"article:{article_id}:views"
    # 优先从缓存读取
    views = redis_client.get(cache_key)
    if views is None:
        # 缓存未命中，从数据库读并写入缓存
        stat, _ = ArticleReadStat.objects.get_or_create(article=article)
        views = stat.total_views
        redis_client.set(cache_key, views)
    else:
        # 缓存命中，自动加1
        views = redis_client.incr(cache_key)
    # 这里只是演示，后续我们会用异步任务定期将缓存写回数据库
    return render(request, 'article_detail.html', {
        'article': article,
        'stat': {'total_views': views, 'unique_visitors': 0},  # 访客数后续实现
    })
