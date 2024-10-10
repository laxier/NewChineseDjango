from django.db import models

class ChineseWord(models.Model):
    simplified = models.CharField(max_length=50)
    traditional = models.CharField(max_length=50, blank=True)
    pinyin = models.CharField(max_length=100)
    meaning = models.TextField()

    def __str__(self):
        return f"{self.simplified} ({self.pinyin})"