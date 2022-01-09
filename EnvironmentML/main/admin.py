from django.contrib import admin
from .models import Project
from tinymce.widgets import TinyMCE
from django.db import models
from django.contrib.auth.models import User


class UsersInline(admin.StackedInline):
    model = Project.project_authors.through


# Register your models here
class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    filter_horizontal = ('project_authors',)


admin.site.register(Project, ProjectAdmin)
