from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView

from blogs.forms import BlogsCommentModelForm
from blogs.models import BlogModel, BlogCategoryModel, BlogTagModel, BlogCommentModel
from users.models import TeamModel


class BlogListView(ListView):
    template_name = 'blogs/blog-list.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_queryset(self):
        qs = BlogModel.objects.all().order_by('-pk')
        cat = self.request.GET.get('cat')
        tag = self.request.GET.get('tag')
        q = self.request.GET.get('q')

        if cat:
            qs = qs.filter(category__in=cat)
        if tag:
            qs = qs.filter(tags__in=tag)
        if q:
            qs = qs.filter(title__icontains=q)

        return qs



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategoryModel.objects.all()
        context['tags'] = BlogTagModel.objects.all()
        context['famous_blogs'] = BlogModel.objects.all().order_by('-created_at')[:3]
        context["related_blogs"] = BlogModel.objects.all().order_by('-created_at')

        return context


class BlogDetailView(DetailView):
    template_name = 'blogs/blog-detail.html'
    context_object_name = 'blogs'
    model = BlogModel

    def get_object(self, *args, **kwargs):
        return BlogModel.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        blogs = BlogModel.objects.get(id=self.kwargs['pk'])
        content = super().get_context_data(**kwargs)
        context = {
            "author": TeamModel.objects.all(),
            "blog": BlogModel.objects.get(pk=self.kwargs['pk']),
            "category": BlogCategoryModel.objects.all(),
            "tags": BlogTagModel.objects.all(),
            "famous_blogs": BlogModel.objects.all().order_by('-created_at')[:3],
            "related_blogs": BlogModel.objects.filter(category__in=self.object.category.all())[:3],
            'comments': BlogCommentModel.objects.filter(blogs=blogs),

        }
        return context

class BlogCommentView(LoginRequiredMixin, CreateView):
    template_name = 'blogs/blogs-detail.html'
    form_class = BlogsCommentModelForm
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        blog_id = self.kwargs['pk']
        blog = BlogModel.objects.get(pk=blog_id)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.blogs = blog  # comment.product dan comment.blogs ga o'zgartirish
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('blogs:list'))

    def form_invalid(self, form):
        return self.get_success_url()