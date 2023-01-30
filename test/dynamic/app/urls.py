from django.urls import include, path
from app.modules.category.view import CategoryDeleteView, CategoryFormView, CategoryListView, CategoryNestedListView
from app.modules.article.view import ArticleDeleteView, ArticleFormView, ArticleListView
from .modules.auth.view import *
from .modules.dynamic.view import *
from .modules.user.view import *
from .modules.contact.view import *
from .modules.document.view import *
from .modules.question.view import *


urlpatterns = [
    # Dynamic
    path('dynamic/', DynamicListView.as_view(), name='dynamic'),
    path('dynamic/page-<int:page>', DynamicListView.as_view(), name='dynamic.page'),
    path('dynamic/form/', DynamicFormView.as_view(), name='dynamic.add'),
    path('dynamic/form/<id>', DynamicFormView.as_view(), name='dynamic.change'),
    path('dynamic/delete/', DynamicDeleteView.as_view(), name='dynamic.delete'),

    # Question
    path('question/', QuestionListView.as_view(), name='question'),
    path('question/page-<int:page>', QuestionListView.as_view(), name='question.page'),
    path('question/form/', QuestionFormView.as_view(), name='question.add'),
    path('question/form/<id>', QuestionFormView.as_view(), name='question.change'),
    path('question/delete/', QuestionDeleteView.as_view(), name='question.delete'),

    # Auth
    path('login/', AuthLoginView.as_view(), name='login'),
    path('logout/', AuthLogoutView.as_view(), name='logout'),

    # User
    path('user/', UserListView.as_view(), name='user'),
    path('user/page-<int:page>', UserListView.as_view(), name='user.page'),
    path('user/form/', UserFormView.as_view(), name='user.add'),
    path('user/form/<id>', UserFormView.as_view(), name='user.change'),
    path('user/delete/', UserDeleteView.as_view(), name='user.delete'),

    # Contact
    path('contact/', ContactListView.as_view(), name='contact'),
    path('contact/page-<int:page>', ContactListView.as_view(), name='contact.page'),
    path('contact/form/', ContactFormView.as_view(), name='contact.add'),
    path('contact/form/<id>', ContactFormView.as_view(), name='contact.change'),
    path('contact/delete/', ContactDeleteView.as_view(), name='contact.delete'),

    # Document
    path('document/', DocumentListView.as_view(), name='document'),
    path('document/page-<int:page>', DocumentListView.as_view(), name='document.page'),
    path('document/form/', DocumentFormView.as_view(), name='document.add'),
    path('document/form/<id>', DocumentFormView.as_view(), name='document.change'),
    path('document/delete/', DocumentDeleteView.as_view(), name='document.delete'),

    # Category
    path('category/nested', CategoryNestedListView.as_view(), name='category'),
    path('category/list', CategoryListView.as_view(), name='category.list'),
    path('category/form', CategoryFormView.as_view(), name='category.add'),
    path('category/form/<id>', CategoryFormView.as_view(), name='category.change'),
    path('category/delete/', CategoryDeleteView.as_view(), name='category.delete'),

    # Article
    path('article', ArticleListView.as_view(), name='article'),
    path('article/page-<int:page>', ArticleListView.as_view(), name='article.page'),
    path('article/form', ArticleFormView.as_view(), name='article.add'),
    path('article/form/<id>', ArticleFormView.as_view(), name='article.change'),
    path('article/delete/', ArticleDeleteView.as_view(), name='article.delete'),
]