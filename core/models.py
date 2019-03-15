from django.utils.timezone import now as current_time
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


from . import settings as app_settings


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Article(models.Model):
    title = models.CharField(max_length=app_settings.ARTICLE_TITLE_LEN)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user),
                               related_name='news_articles',
                               related_query_name='article')
    text = models.TextField()
    created_date = models.DateTimeField(default=current_time)
    published_date = models.DateTimeField(blank=True, null=True)

# TODO: create following models for core site app:
#