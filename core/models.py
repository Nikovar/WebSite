from django.utils.timezone import now as current_time
from django.db import models
from django.contrib.auth import get_user_model

from accounts.utils import dummy_deleted_user

from . import settings as app_settings

get_sentinel_user = dummy_deleted_user  # TODO: remove this shit after you done with temp


class Article(models.Model):
    title = models.CharField(max_length=app_settings.ARTICLE_TITLE_LEN)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET(dummy_deleted_user),
                               related_name='news_articles',
                               related_query_name='article')
    text = models.TextField()
    created_date = models.DateTimeField(default=current_time)
    published_date = models.DateTimeField(blank=True, null=True)

# TODO: create another models for core site app
