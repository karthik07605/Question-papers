from django.contrib import admin
from django import forms
from .models import Paper

class PaperAdminForm(forms.ModelForm):
    file = forms.FileField(required=False, help_text="Upload a file to store in Google Drive")

    class Meta:
        model = Paper
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get("file")

        if file:
            instance.save(file=file)  # Pass file to the model save() method

        if commit:
            instance.save()
        return instance

class PaperAdmin(admin.ModelAdmin):
    form = PaperAdminForm
    list_display = ("question_paper_name", "department", "year", "semester", "paper_type", "file_url")
    search_fields = ("question_paper_name", "department", "year", "semester", "paper_type")

admin.site.register(Paper, PaperAdmin)
