from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from .models import BlogPost, Comment
from .forms import BlogPostForm, UpdateBlogPostForm, BlogPostCommentForm

# Create your views here.

@login_required
def LikeView(request, slug):
    post = get_object_or_404(BlogPost, slug=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:detail', args=[slug] ))


class BlogPostHomeView(ListView):
    model = BlogPost
    # context_object_name = 
    template_name='blog.html'
    paginate_by = 10
    

class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "create_post.html"
    # fields = '__all__'
    # fields = ('title', 'content')

    def get_form_kwargs(self):
        kwargs = super(BlogPostCreateView, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = BlogPost()
        kwargs['instance'].user = self.request.user
        return kwargs
    
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        post = self.object
        return reverse_lazy('blog:detail', kwargs={'slug': post.slug})


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = UpdateBlogPostForm
    template_name = "update_post.html"
    # fields = ['title', 'content']
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BlogPostUpdateView, self).post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context
    
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        post = self.object
        return reverse_lazy('blog:detail', kwargs={'slug': post.slug})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "delete_post.html"
    success_url = reverse_lazy('blog:blogs')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BlogPostDeleteView, self).post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name='single-blog.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        get_post = get_object_or_404(BlogPost, slug=self.kwargs['slug'])
        total_likes = get_post.total_likes()
        
        liked = False
        
        if get_post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context['total_likes'] = total_likes
        context['liked'] = liked
        
        context['object_list'] = BlogPost.objects.all()
        
        context['comments'] = Comment.objects.filter(blog_post_id=self.object.id).all()
        context['form'] = BlogPostCommentForm
        return context
    
    def post(self, request, slug):
       post = get_object_or_404(BlogPost, slug=slug)
       form = BlogPostCommentForm(request.POST)

       if form.is_valid():
           obj  = form.save(commit=False)
           obj.blog_post = post
           obj.user = self.request.user
           obj.save()
           return redirect('blog:detail', post.slug)


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "delete_comment.html"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CommentDeleteView, self).post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context
    
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        post = self.object.blog_post
        return reverse_lazy('blog:detail', kwargs={'slug': post.slug})


class CommentEditView(UpdateView):
    model = Comment
    form_class = BlogPostCommentForm
    template_name = "edit_comment.html"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CommentEditView, self).post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context
    
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        post = self.object.blog_post
        return reverse_lazy('blog:detail', kwargs={'slug': post.slug})

# NOTE THIS IS JUST IF I WANTED TO CREATE THE COMMENT IN OTHER PAGE(AND OTHER STUFFS)
# class CommentCreateView(CreateView):
#     model = Comment
#     form_class = BlogPostCommentForm
    
#     def form_valid(self, form):
#         form.instance.blog_post_id = self.kwargs['pk']
#         return super().form_valid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super(CommentCreate, self).get_context_data(**kwargs)
#         context['post'] = get_object_or_404(Post, pk = self.kwargs['pk'])
#         return context

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.post=get_object_or_404(Post, pk = self.kwargs['pk'])
#         return super(CommentCreate, self).form_valid(form)

#     def get_success_url(self):
#         return reverse('post-detail', kwargs={'pk': self.kwargs['pk'],})


def CategoryView(request, cat):
    category_posts = BlogPost.objects.filter(category=cat.replace('-', ' '))
    object_list = BlogPost.objects.all()
    if category_posts:
        for categories in category_posts:
            category = categories
    else:
        category = None
    paginator = Paginator(category_posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'object_list': object_list,
        'category':category,
        'category_name':cat.replace('-', ' '),
        'category_posts':category_posts
    }
    return render(request, 'category.html', context)
