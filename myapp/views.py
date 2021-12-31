import os
from django.contrib import auth

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.core.files import uploadhandler
from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from myapp import models
from myapp.forms import DocumentUploadForm, RegisterForm
from django.conf import settings
from django.http import HttpRequest

from myapp.models import Document, Author, Keyword
from myapp.pdf_reader import read_pdf


def index(request):
    return render(request, "index.html")


@login_required
def document_upload(request: HttpRequest):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
    else:
        form = DocumentUploadForm()
    if form.is_valid() and request.method == "POST":
        document: Document = form.save(commit=False)
        pdf_info = read_pdf(
            document.file.file.file
        )  # infoyu burada alıyoruz ÇOOOOK ÖNEMLİ
        print(pdf_info)

        document.uploader = request.user
        document.date = pdf_info.date
        document.lesson = pdf_info.lesson
        document.project = pdf_info.project_name
        document.title = pdf_info.project_title
        document.summary = pdf_info.summary
        document.jury = pdf_info.juries
        document.term = pdf_info.term
        document.save()
        for keyword in pdf_info.keywords:
            document.keywords.add(Keyword.objects.get_or_create(name=keyword)[0])
        for author_info in pdf_info.authors:
            student_id = author_info[0]
            full_name = author_info[1].split(maxsplit=1)
            if len(full_name) > 1:
                name, surname = full_name
            else:
                name = full_name[0]
                surname = ""
            education_time = (
                Author.EducationType.D
                if student_id[5] == "1"
                else Author.EducationType.E
            )
            author = Author.objects.get_or_create(
                student_id=student_id,
                name=name,
                surname=surname,
                education_time=education_time,
            )[0]
            document.authors.add(author)
        # document.save()

        return redirect("index")
    context = {
        "form": form,
    }
    return render(request, "document_upload.html", context)


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("index")
    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")


# @login_required
class DocumentViewList(ListView):
    model = Document

    def get_queryset(self):
        return Document.objects.filter(uploader=self.request.user)


class DocumentDetailView(DetailView):
    model = Document


def keyword_detail(request, keyword: str):
    docs = get_object_or_404(Keyword, name__icontains=keyword).document_set.filter(uploader=request.user)
    context = {
        "keyword": keyword,
        "document_list": docs,
    }

    return render(
        request, template_name="myapp/keyword_documents.html", context=context
    )


def author_detail(request, author: str):
    docs = get_object_or_404(Author, name__icontains=author).document_set.filter(uploader=request.user)
    context = {
        "author": author,
        "document_list": docs,
    }

    return render(request, template_name="myapp/author_documents.html", context=context)


def lesson_detail(request, lesson: str):
    docs = get_list_or_404(Document, lesson__icontains=lesson,uploader=request.user)
    print(docs)
    print("-----------------------------")
    print(lesson)
    context = {
        "lesson": lesson,
        "document_list": docs,
    }
    return render(request, template_name="myapp/lesson_documents.html", context=context)


def project_detail(request, project: str):
    docs = get_list_or_404(Document, project__icontains=project,uploader=request.user)  # list kullanıldı
    context = {
        "project": project,
        "document_list": docs,
    }
    return render(
        request, template_name="myapp/project_documents.html", context=context
    )


def term_detail(request, term: str):
    docs = get_list_or_404(Document, term__icontains=term,uploader=request.user)  # list kullanıldı
    context = {
        "term": term,
        "document_list": docs,
    }
    return render(request, template_name="myapp/term_documents.html", context=context)


def full_detail(request, term: str, lesson: str):
    docs = get_list_or_404(
        Document, term__icontains=term, lesson__icontains=lesson,uploader=request.user
    )  # list kullanıldı
    context = {
        "term": term,
        "lesson": lesson,
        "document_list": docs,
    }
    return render(request, template_name="myapp/join_documents.html", context=context)
