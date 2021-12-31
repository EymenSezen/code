from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Author, Document, Keyword

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    list_filter = ['authors',"term","lesson"]
    search_fields = ['title', 'lesson']
    class Meta:
        model = Document


admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Document,DocumentAdmin)
admin.site.register(Keyword)

# admin.site.register(Teacher)

