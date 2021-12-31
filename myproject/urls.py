from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views
from myapp.views import (
    DocumentDetailView,
    DocumentViewList,
    author_detail,
    document_upload,
    full_detail,
    keyword_detail,
    lesson_detail,
    logout_view,
    project_detail,
    register_view,
    term_detail,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("", views.index, name="index"),
    path("docs/", DocumentViewList.as_view(), name="list"),
    path("docs/<int:pk>", DocumentDetailView.as_view(), name="document_detail"),
    path("docs/upload", document_upload, name="document_upload"),
    path("keyword/<keyword>", keyword_detail, name="keyword_detail"),
    path("author/<author>", author_detail, name="author_detail"),
    path("lesson/<lesson>", lesson_detail, name="lesson_detail"),
    path("project/<project>", project_detail, name="project_detail"),        
    path("term/<term>", term_detail, name="term_detail"),
    path("join/<lesson>/<term>",full_detail,name="full_detail")



]

# Serve static files during development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
