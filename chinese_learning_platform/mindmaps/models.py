from django.db import models

class MindMap(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    mind_map = models.ForeignKey(MindMap, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.mind_map.title})"

class ChineseWord(models.Model):
    simplified = models.CharField(max_length=50)
    traditional = models.CharField(max_length=50, blank=True)
    pinyin = models.CharField(max_length=100)
    meaning = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    mind_maps = models.ManyToManyField(MindMap, related_name='words')
    categories = models.ManyToManyField(Category, related_name='words', blank=True)

    def __str__(self):
        return f"{self.simplified} ({self.pinyin})"