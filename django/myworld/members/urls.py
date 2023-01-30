from django.urls import path
from .views.website import category,home,singleblog,hoidap,contact
from .views.admin.auth import login,admin,category_admin,article_admin,question_admin

urlpatterns = [
    path('', home.index, name='home_index'),
    path('category', category.index, name='category_index'),
    path('category/<str:slug>', category.index, name='category_index'),
    path('bai-viet/<str:slug>-<int:id>', singleblog.index, name='singleblog_index'),
    path('hoidap', hoidap.index, name='hoidap_index'),
    path('contact', contact.index, name='contact_index'),
    path('login', login.login, name='login_index'),
    path('register', login.regis, name='register_index'),
    path('adduser', login.adduser, name='adduser_index'),
    path('forgot-password', login.forgot, name='forgot-password_index'),
    path('reset-password-confirm/<int:id>/<token>/<token_date>', login.reset_password_confirm, name='reset_password_done_index'),
    path('home-admin', admin.index, name='home-admin_index'),
    path('contact-admin', admin.contact, name='contact_admin_index'),
    path('profile', admin.profile, name='profile_index'),
    path('edit_profile', admin.edit_profile, name='edit_profile_index'),
    path('update_profile', admin.update_profile, name='update_profile_index'),


    path('category-admin', category_admin.category, name='category-admin_index'),
    path('category-admin/form_cate', category_admin.form_cate, name='form_cate_index'),
    path('category-admin/form_cate/<str:alias>', category_admin.form_cate, name='form_cate_index'),
    path('category-admin/delete/<str:alias>', category_admin.delete_cate, name='delete_cate_index'),


    path('article-admin', article_admin.article, name='article-admin_index'),
    path('article-admin/form_art', article_admin.form_art, name='update_article_index'),
    path('article-admin/form_art/<str:alias>', article_admin.form_art, name='update_article_index'),
    path('article-admin/delete/<str:alias>', article_admin.delete_article, name='delete_article_index'),


    path('question-admin', question_admin.question, name='question-admin_index'),
    path('question-add', question_admin.add_question, name='add_ques_index'),
    path('question-admin/update/<str:id>', question_admin.update_question, name='update_ques_index'),
    path('question-admin/delete/<int:id>', question_admin.delete_ques, name='delete_ques_index'),


    path('logout', admin.log_out, name='logout_index'),
    path('change_password', admin.change_password, name='change_password_index'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='admin/password/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="admin/password/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='admin/password/password_reset_complete.html'), name='password_reset_complete'), 
]