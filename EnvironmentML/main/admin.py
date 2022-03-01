from django.contrib import admin
from .models import Project, UserProfile, Volunteers
from tinymce.widgets import TinyMCE
from django.db import models
from django.contrib.auth.models import User


# Register your models here
class ProjectAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "project_users":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(UserProfile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Volunteers)