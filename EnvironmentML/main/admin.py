from django.contrib import admin
from .models import Project
from tinymce.widgets import TinyMCE
from django.db import models
from django.contrib.auth.models import User


class UsersInline(admin.StackedInline):
    model = Project.project_authors.through


# Register your models here
class ProjectAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "project_users":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        models.ManyToManyField: {'widget': admin.widgets.FilteredSelectMultiple('authors', False)},
    }
    # set "project_authors" to use formfield_for_manytomany
    inlines = [UsersInline]
    list_display = ('project_name', 'project_description', 'project_authors', 'project_date_created', 'project_date_modified')


admin.site.register(Project, ProjectAdmin)
