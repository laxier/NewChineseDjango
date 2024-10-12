from django.views import generic
from .models import RelatedWord, Sentence
from chineseword.models import ChineseWord
from frontend.views import CurrentUserMixin

class ChineseWordDetailView(CurrentUserMixin, generic.DetailView):
    model = ChineseWord
    template_name = 'wordpages/chinese_word_detail.html'  # Adjust the template path
    context_object_name = 'chinese_word'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sentences'] = Sentence.objects.filter(chinese_word=self.object)
        context['related_words'] = RelatedWord.objects.filter(word=self.object)
        return context
