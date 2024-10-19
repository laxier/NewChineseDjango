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
