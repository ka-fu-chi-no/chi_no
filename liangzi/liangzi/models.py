from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .cache import RedisClient
import logging

logger = logging.getLogger(__name__)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ArticleReadStat(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='read_stat')
    total_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.article.title} - {self.total_views} views"

@receiver(post_save, sender=Article)
def sync_article_cache(sender, instance, created, **kwargs):
    """当文章保存时，同步缓存数据"""
    if not created:  # 只在更新时同步
        redis_client = RedisClient()
        redis_client.sync_views_to_db(instance.id)