from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


MAX_NAME_LEN = 128


class Author(models.Model):
    
    student_id = models.CharField("öğrenci numarası", max_length=9, primary_key=True)
    name = models.CharField("ad", max_length=MAX_NAME_LEN)
    surname = models.CharField("soyad", max_length=MAX_NAME_LEN)

    class EducationType(models.IntegerChoices):
        D = 1, "1. öğretim"
        E = 2, "2. öğretim"

    education_time = models.IntegerField("öğretim türü", choices=EducationType.choices)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Keyword(models.Model):
    name = models.CharField("anahtar kelimesi", max_length=MAX_NAME_LEN, unique=True)

    def clean(self):
        self.name = self.name.lower()
    def __str__(self):
        return f"{self.name}"


# class Teacher(models.Model):
#     name = models.CharField("ad", max_length=MAX_NAME_LEN)
#     surname = models.CharField("soyad", max_length=MAX_NAME_LEN)
#     title = models.CharField("unvan", max_length=MAX_NAME_LEN)


def document_upload_path(doc, filename):
    return f"docs/{filename}"


class Document(models.Model):
    uploader = models.ForeignKey(to=User, on_delete=models.CASCADE)
    authors = models.ManyToManyField(to=Author)
    lesson = models.TextField("Dersin adı")
    project = models.TextField("Proje Adı")
    summary = models.TextField("proje özeti")
    date = models.TextField("teslim tarihi")
    title = models.TextField("proje başlığı")
    keywords = models.ManyToManyField(to=Keyword)
    # supervisor = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)
    # jury = models.ManyToManyField(to=Teacher, related_name="document_juries")
    jury = models.TextField("Jüriler")
    file = models.FileField("Tez dokümanı", upload_to=document_upload_path)
    term = models.TextField("Dönem")
    def __str__(self):
        return f"{self.title}"