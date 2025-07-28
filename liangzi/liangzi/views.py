from django.shortcuts import render, get_object_or_404
from .models import Article, ArticleReadStat

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 获取或创建统计对象
    stat, created = ArticleReadStat.objects.get_or_create(article=article)
    # 增加总阅读量
    stat.total_views += 1
    stat.save()
    return render(request, 'article_detail.html', {
        'article': article,
        'stat': stat,
    })
