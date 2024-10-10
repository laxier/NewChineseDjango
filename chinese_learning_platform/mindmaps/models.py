from django.db import models
from chineseword.models import ChineseWord


class MindMap(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    mind_map = models.ForeignKey(MindMap, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.mind_map.title})"


class WordInMindMap(models.Model):
    word = models.ForeignKey(ChineseWord, related_name='mind_map_links', on_delete=models.CASCADE)
    mind_map = models.ForeignKey(MindMap, related_name='word_links', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category, related_name='words', blank=True)

    class Meta:
        unique_together = ('word', 'mind_map')

    def __str__(self):
        return f"{self.word} in {self.mind_map}"
