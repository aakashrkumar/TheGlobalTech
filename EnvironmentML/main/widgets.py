from django_select2 import forms as s2forms


class AuthorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]
