import requests
from bs4 import BeautifulSoup
from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model

User = get_user_model()


class ChineseWord(models.Model):
    simplified = models.CharField(max_length=50)
    traditional = models.CharField(max_length=50, blank=True, null=True)
    pinyin = models.CharField(max_length=100, blank=True, null=True)
    meaning = models.TextField(blank=True, null=True)
    hsk_level = models.CharField(null=True, blank=True, max_length=10)
    favorites = models.ManyToManyField(
        User,
        related_name='favorite_words',
        blank=True,
        through='ChineseWordFavorite'  # Указываем кастомное промежуточное имя
    )

    class Meta:
        db_table = 'chinese_word'
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


class ChineseWordFavorite(models.Model):
    chinese_word = models.ForeignKey(ChineseWord, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['chinese_word', 'user'],
                name='chineseword_favorites_uniq'  # Устанавливаем короткое имя
            ),
        ]


def searchWord(word):
    url = f'https://www.trainchinese.com/v2/search.php?searchWord={word}&rAp=0&height=0&width=0&tcLanguage=ru'

    try:
        response = requests.get(url, timeout=10, verify='./certs/trainchinese.crt')
        # Дата выдачи	вторник, 19 ноября 2024г. в 03:00:00
        # Срок действия	вторник, 25 ноября 2025г. в 02:59:59
        response.raise_for_status()

        if response.status_code == 200:
            # Парсим контент страницы
            soup = BeautifulSoup(response.content, 'html.parser')

            # Ищем строки таблицы
            rows = soup.find_all('tr')
            if not rows or len(rows) == 0:
                print("No table rows found.")
                return None, None

            # Ищем нужные элементы в первой строке
            cells = rows[0].find_all('div')
            if cells and len(cells) > 2:
                pinyin = cells[1].text.strip()
                meaning = cells[2].text.replace("\"", "").strip()
                return pinyin, meaning
            else:
                print("Expected data not found in the table cells.")
                return None, None
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching word details: {e}")
        return None, None
