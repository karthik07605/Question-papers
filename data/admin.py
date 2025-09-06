from django.contrib import admin
from django import forms
from .models import Regulation, Department, Paper
from .gdrive import upload_to_drive  # ✅ Import your Drive uploader


class PaperAdminForm(forms.ModelForm):
    file = forms.FileField(required=False, help_text="Upload a file to store in Google Drive")

    class Meta:
        model = Paper
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get("file")

        if file:
            # Upload to Google Drive
            drive_link = upload_to_drive(file, file.name)
            instance.file_url = drive_link  # Save URL in DB

        if commit:
            instance.save()
        return instance


class PaperAdmin(admin.ModelAdmin):
    form = PaperAdminForm
    list_display = ("question_paper_name", "department", "year", "semester", "paper_type", "file_url")
    list_filter = ("department", "year", "semester", "paper_type", "regulation")
    search_fields = ("question_paper_name",)


# ✅ Register all models
admin.site.register(Paper, PaperAdmin)
admin.site.register(Regulation)
admin.site.register(Department)
