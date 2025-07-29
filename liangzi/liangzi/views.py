# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Article, ArticleReadStat
from .cache import RedisClient
from django.http import JsonResponse

redis_client = RedisClient()

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 生成用户ID
    user_id = request.user.username
    # 记录用户访问
    user_views = redis_client.record_user_visit(article_id, user_id)
    # 获取总阅读量
    cache_key = f"article:{article_id}:views"
    total_views = redis_client.get(cache_key)
    if total_views is None:
        # 缓存未命中，从数据库读并写入缓存
        stat, _ = ArticleReadStat.objects.get_or_create(article=article)
        total_views = stat.total_views
        redis_client.set(cache_key, total_views)
    else:
        # 缓存命中，自动加1
        total_views = redis_client.incr(cache_key)
    
    # 获取访客数
    visitor_count = redis_client.get_visitor_count(article_id)
    
    # 当阅读量达到一定阈值时，触发同步
    if total_views % 10 == 0:  # 每10次访问同步一次
        redis_client.sync_views_to_db(article_id)
    
    return render(request, 'article_detail.html', {
        'article': article,
        'stat': {
            'total_views': total_views,
            'unique_visitors': visitor_count,
            'user_views': user_views
        },
        'user_id': user_id,
    })

def sync_views(request, article_id):
    redis_client.sync_views_to_db(article_id)
    return JsonResponse({'status': 'ok'})

def cache_hit_rate(request):
    rate = redis_client.get_hit_rate()
    return JsonResponse({'cache_hit_rate': f"{rate}%"})

def sync_visitors(request, article_id):
    redis_client.sync_visitors_to_db(article_id)
    return JsonResponse({'status': 'visitors synced'})
