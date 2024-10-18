from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import MindMap, WordInMindMap
from .forms import MindMapForm

class MindMapListView(ListView):
    model = MindMap
    template_name = 'mindmaps/mindmap_list.html'
    context_object_name = 'mindmaps'


class MindMapDetailView(DetailView):
    model = MindMap
    template_name = 'mindmaps/mindmap_detail.html'

    def get_queryset(self):
        return MindMap.objects.prefetch_related('word_links__word')


class MindMapCreateView(CreateView):
    model = MindMap
    form_class = MindMapForm
    template_name = 'mindmaps/mindmap_form.html'
    success_url = reverse_lazy('mindmap-list')
