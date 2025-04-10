from django.views import generic
from .models import RelatedWord, Sentence
from chineseword.models import ChineseWord
from frontend.views import CurrentUserMixin


class ChineseWordDetailView(CurrentUserMixin, generic.DetailView):
    model = ChineseWord
    context_object_name = 'chinese_word'

    def get_template_names(self):
        is_mindmap = self.request.GET.get('is_mindmap', 'false') == 'true'
        if is_mindmap:
            return ['wordpages/chinese_word_detail_no_header.html']
        return ['wordpages/chinese_word_detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sentences'] = Sentence.objects.filter(chinese_word=self.object)
        context['related_words'] = RelatedWord.objects.filter(word=self.object)
        context['is_favorite'] = self.request.user in self.object.favorites.all()

        return context


import os
import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

import openpyxl
from openpyxl.styles import PatternFill, Font

from users.models import WordPerformance
from chineseword.models import ChineseWord


class HSK4ProgressDownloadView(LoginRequiredMixin, View):
    """
    Пример вью:
    1) Загружаем progress_template_hsk4.xlsx
    2) Собираем слова из столбца E и примеры из столбца M
    3) Одним запросом получаем ChineseWord
    4) Одним запросом получаем WordPerformance для текущего юзера
    7) Сохраняем и отдаём пользователю Excel
    """

    def get(self, request, *args, **kwargs):
        # 1) Путь к шаблону
        input_path = os.path.join(settings.BASE_DIR, "progress_template_hsk4.xlsx")
        wb = openpyxl.load_workbook(input_path)
        ws = wb.active  # Или wb["Sheet"] — смотрите, как у вас называется лист

        # ---------------------------------------------------
        # 2) Собираем иероглифы из столбцов E (слово) и M (пример)
        # ---------------------------------------------------
        characters = set()

        # Для слов: E = 5
        for row in ws.iter_rows(min_row=2, max_col=15):
            word_cell = row[4]  # index 4 = колонка E
            if word_cell.value:
                characters.add(word_cell.value)

        # Для примеров: L = 12
        for row in ws.iter_rows(min_row=2, max_col=15):
            example_cell = row[11]  # index 11 = колонка L
            if example_cell.value:
                characters.add(example_cell.value)

        # ---------------------------------------------------
        # 3) Одним запросом все ChineseWord, у которых simplified в нашем наборе
        # ---------------------------------------------------
        words_qs = ChineseWord.objects.filter(simplified__in=characters)
        # Превращаем в словарь { "你": <ChineseWord>, "爱": <ChineseWord>, ... }
        word_dict = {w.simplified: w for w in words_qs}

        # ---------------------------------------------------
        # 4) Одним запросом все WordPerformance для этих слов
        # ---------------------------------------------------
        user_id = request.user.id
        word_ids = [w.id for w in words_qs]  # список ID найденных слов
        perf_qs = WordPerformance.objects.filter(user_id=user_id, word_id__in=word_ids)
        # Словарь { word_id: <WordPerformance>, ... }
        perf_dict = {p.word_id: p for p in perf_qs}

        # ---------------------------------------------------
        # Пример несложной логики раскраски ячеек со словами/примерами
        # ---------------------------------------------------
        no_progress_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        no_progress_font = Font(color="000000")  # для слабого прогресса
        low_progress_font = Font(color="FF9900")  # прогресс 30-80
        good_progress_font = Font(color="008000")  # >80

        def color_cell_if_needed(cell, prog):
            """
            Раскрашивает ячейку (cell) в зависимости от прогресса prog.
            prog может быть None, либо целым числом 0..100
            """
            if prog is None:
                cell.fill = no_progress_fill
            elif prog < 30:
                cell.font = no_progress_font
            elif 30 <= prog <= 80:
                cell.font = low_progress_font
            else:
                cell.font = good_progress_font

        # ---------------------------------------------------
        # 5) Заполняем A,B,C для слова из E и I,J,K, для примера из L
        # ---------------------------------------------------
        for row in ws.iter_rows(min_row=2, max_col=15):
            # Ячейки для слов (E=5 → index=4)
            word_cell = row[4]
            # Ячейки для примеров (L=13 → index=12)
            example_cell = row[11]
            print(example_cell.value)

            # 5.1) Если есть "слово" в E (упрощённый иероглиф)
            if word_cell.value:
                word_obj = word_dict.get(word_cell.value)
                perf = perf_dict.get(word_obj.id) if word_obj else None

                # Берём нужные поля
                wrong_count = perf.wrong if perf else 0
                right_count = perf.right if perf else 0
                prog = perf.accuracy_percentage_display if (
                            perf and perf.accuracy_percentage_display is not None) else None

                # Записываем в A,B,C (index=0,1,2)
                row_num = word_cell.row
                a_cell = ws.cell(row=row_num, column=1)  # A
                b_cell = ws.cell(row=row_num, column=2)  # B
                c_cell = ws.cell(row=row_num, column=3)  # C

                a_cell.value = wrong_count
                b_cell.value = right_count
                c_cell.value = prog if prog is not None else ""

                # Раскрасим саму ячейку со словом (E) по прогрессу
                color_cell_if_needed(word_cell, prog)

            # 5.2) Если есть "пример" в L (упрощённый иероглиф)
            if example_cell.value:
                word_obj = word_dict.get(example_cell.value)
                perf = perf_dict.get(word_obj.id) if word_obj else None

                wrong_count = perf.wrong if perf else 0
                right_count = perf.right if perf else 0
                prog = perf.accuracy_percentage_display if (
                            perf and perf.accuracy_percentage_display is not None) else None

                # Записываем в J,K,L (index=9,10,11)
                row_num = example_cell.row
                j_cell = ws.cell(row=row_num, column=9)  # I
                k_cell = ws.cell(row=row_num, column=10)  # J
                l_cell = ws.cell(row=row_num, column=11)  # K

                j_cell.value = wrong_count
                k_cell.value = right_count
                l_cell.value = prog if prog is not None else ""

                # Раскрасим саму ячейку с примером (M) по прогрессу
                color_cell_if_needed(example_cell, prog)

        # ---------------------------------------------------
        # 6) (Необязательно) создаём лист Statistics, если нужно
        #    — можно собрать суммарную статистику и вывести
        # ---------------------------------------------------
        # (Пропущено для краткости — по аналогии с предыдущими примерами.)

        # ---------------------------------------------------
        # 7) Возвращаем Excel с датой и временем в названии
        # ---------------------------------------------------
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"hsk4_progress_{timestamp}.xlsx"

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response
