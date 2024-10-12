import requests
from bs4 import BeautifulSoup
from django.db import models
from django.db.models import UniqueConstraint

class ChineseWord(models.Model):
    simplified = models.CharField(max_length=50)
    traditional = models.CharField(max_length=50, blank=True, null=True)
    pinyin = models.CharField(max_length=100, blank=True, null=True)
    meaning = models.TextField(blank=True, null=True)
    hsk_level = models.CharField(null=True, blank=True, max_length=10)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['simplified', 'pinyin', 'meaning'], name='unique_simplified_pinyin_meaning')
        ]

    def __str__(self):
        return f"{self.simplified} ({self.pinyin})"

    def save(self, *args, **kwargs):
        # If pinyin or meaning are not provided, fetch them from the external source
        if not self.pinyin or not self.meaning:
            pinyin, meaning = searchWord(self.simplified)
            if pinyin:
                self.pinyin = pinyin
            if meaning:
                self.meaning = meaning
        super().save(*args, **kwargs)

def searchWord(word):
    url = f'https://www.trainchinese.com/v2/search.php?searchWord={word}&rAp=0&height=0&width=0&tcLanguage=ru'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        rows = soup.find_all('tr')
        cells = rows[0].find_all('div')  # Assuming the text is in divs within the table rows
        if cells and len(cells) > 2:
            pinyin = cells[1].text.strip()
            meaning = cells[2].text.replace("\"", "").strip()
            return pinyin, meaning
    return None, None
