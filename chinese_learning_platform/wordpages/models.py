from django.db import models
from django.db.models import UniqueConstraint
from chineseword.models import ChineseWord

# Create your models here.
class RelatedWord(models.Model):
    word = models.ForeignKey(ChineseWord, related_name='related_words', on_delete=models.CASCADE)
    related_word = models.ForeignKey(ChineseWord, related_name='related_to', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['word', 'related_word'], name='unique_related_word_pair')
        ]

    def __str__(self):
        return f"{self.word} is related to {self.related_word}"

class Sentence(models.Model):
    content = models.TextField()
    meaning = models.TextField(null=True, blank=True)
    chinese_word = models.ForeignKey(ChineseWord, on_delete=models.CASCADE, related_name='sentences')

    def __str__(self):
        return self.content
