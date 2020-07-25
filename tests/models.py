from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from snakeoil.models import SEOModel


User = get_user_model()


class Article(SEOModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=500)
    main_image = models.ImageField(
        null=True,
        blank=True,
        width_field="main_image_width",
        height_field="main_image_height",
    )
    main_image_width = models.PositiveSmallIntegerField(null=True, blank=True)
    main_image_height = models.PositiveSmallIntegerField(null=True, blank=True)
    secondary_image = models.ImageField(null=True, blank=True)
    content = models.TextField()

    @property
    def author_name(self):
        return self.author.get_full_name()

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.slug])
