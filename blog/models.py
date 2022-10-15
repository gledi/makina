import mistune
from django.db import models

# create table posts (
#     id int ,
#     title varchar(2222),
#     body text,
#     published_on datetime,
#     author,
#     status,
#     tags
# )


class Post(models.Model):  # default table name: blog_post
    # id = models.BigAutoField(primary_key=True, null=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    published_on = models.DateTimeField(null=True, blank=True)
    author = models.CharField(max_length=128, null=False, blank=False)
    is_published = models.BooleanField(default=False)
    tags = models.CharField(max_length=255)

    class Meta:
        db_table = "posts"

    def __str__(self) -> str:
        return self.title

    @property
    def body_html(self) -> str:
        return mistune.markdown(self.body)
