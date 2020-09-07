from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView
from blog.models import BlogPost

# Create your views here.


class SearchBlogView(ListView):
    template_name = "search/blog_view.html"
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(SearchBlogView, self).get_context_data(
            *args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)  # method_dict['q']
        if query is not None:
            return BlogPost.objects.search(query)
        queryset_list = BlogPost.objects.none()
        return queryset_list
        '''
        __icontains = field contains this
        __iexact = fields is exactly this
        '''
