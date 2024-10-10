from django.db import models
from chineseword.models import ChineseWord


class MindMap(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WordInMindMap(models.Model):
    word = models.ForeignKey(ChineseWord, related_name='mind_map_links', on_delete=models.CASCADE)
    mind_map = models.ForeignKey(MindMap, related_name='word_links', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('word', 'mind_map')

    def __str__(self):
        return f"{self.word} in {self.mind_map}"
