from datetime import datetime

from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import PostForm, CommentForm
from .models import *


def rating(post_pk):
    """
    Функция показа рейтинга
    :param post_pk:
    :return:
    """
    reviews = Reviews.objects.filter(post=post_pk)
    count_rating = sum([i.rating for i in reviews]) / reviews.count()
    return count_rating


def index(request):
    """
    Для вывода постов на главную
    :param request:
    :return:
    """
    posts = Post.objects.all().filter(published=True)
    categories = Category.objects.all()
    count_post = posts.count()
    context = {
        'posts': posts,
        'categories': categories,
        'count_post': count_post
    }
    return render(request, 'blog/index.html', context)


def get_category(request, category_pk):
    """
    Функция показа категорий
    :param request:
    :param category_pk:
    :return:
    """
    posts = Post.objects.filter(category=category_pk)
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)


def post_draft(request):
    """
    Вывод черновиков
    :param request:
    :return:
    """
    posts = Post.objects.all().filter(published=False)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)


def published_post(request, post_pk):
    """
    Страница для публикации не опубликованных статей
    :param request:
    :param post_pk:
    :return:
    """
    post = Post.objects.get(pk=post_pk)
    post.published = True
    post.save()
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)


def post_detail(request, post_pk):
    """
    Вывод статей детально
    Вывод коментариев
    Вывод чисел коментариев

    :param request:
    :param post_pk:
    :return:
    """
    post = Post.objects.get(pk=post_pk)
    comments = Comments.objects.filter(post=post_pk)
    count = comments.count()
    count_rating = rating(post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        comment_form = CommentForm
    context = {
        'post': post,
        'comments': comments,
        'count': count,
        'comment_form': comment_form,
        'rating': count_rating
    }
    return render(request, 'blog/post_detail.html', context)


class AddPost(CreateView):
    """
    Создание поста
    """
    form_class = PostForm
    template_name = 'blog/new_post.html'

    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def post_edit(request, post_pk):
    """
    Редактирование поста
    :param request:
    :param post_pk:
    :return:
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'form': form})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = datetime.now()
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)


def delete_post(request, post_pk):
    """
    Удаление поста
    :param request:
    :param post_pk:
    :return:
    """
    post = get_object_or_404(Post, pk=post_pk).delete()
    return redirect('index')


def delete_comment(request, post_pk, comment_pk):
    """
    Удаление Коментария
    :param request:
    :param post_pk:
    :param comment_pk:
    :return:
    Не работает ссылка
    """
    post = Post.objects.get(pk=post_pk)
    comment = get_object_or_404(Comments, pk=comment_pk).delete()
    return redirect('post_detail', post_pk=post.pk)


# def comment_post(request, post_pk):
#     post = get_object_or_404(Post, pk=post_pk)
#     if request.method == 'GET':
#         form = CommentForm(instance=post)
#         return render(request, 'blog/post_detail.html', {'form': form})


def reviews_views(request, post_pk):
    """
    Функция траница отзывов
    :param request:
    :param post_pk:
    :return:
    """
    post = Post.objects.get(pk=post_pk)
    reviews = Reviews.objects.filter(post=post_pk)
    context = {
        'post': post,
        'reviews': reviews,
    }
    return render(request, 'blog/reviews.html', context)


def recommended_posts(request):
    posts = Post.objects.filter(reviews__rating__gt=3).order_by('-reviews__rating')[0:5]
    categories = Category.objects.all()
    count_post = posts.count()
    context = {
        'posts': posts,
        'categories': categories,
        'count_post': count_post,
    }
    return render(request, 'blog/recommended.html', context)


