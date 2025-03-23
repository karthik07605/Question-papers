from django.shortcuts import render
from .models import Paper
from .gdrive import upload_to_drive  # Import Google Drive function

def home(request):
    details = []
    selected_regulation = ""
    selected_department = ""
    selected_year = ""
    selected_semester = ""
    selected_paper_type = ""

    if request.method == "POST":
        selected_regulation = request.POST.get("regulation", "")
        selected_department = request.POST.get("department", "")
        selected_year = request.POST.get("year", "")
        selected_semester = request.POST.get("semester", "")  
        selected_paper_type = request.POST.get("paper_type", "")  
        file = request.FILES.get("file")  # Get uploaded file

        if selected_regulation and selected_department and selected_year and selected_semester and selected_paper_type:
            details = Paper.objects.filter(
                regulation=selected_regulation,
                department=selected_department,
                year=selected_year,
                semester=selected_semester,
                paper_type=selected_paper_type,
            )

        if file:  # ✅ Direct Upload to Google Drive
            drive_link = upload_to_drive(file, file.name)  

            # Save uploaded file link in database
            Paper.objects.create(
                regulation=selected_regulation,
                department=selected_department,
                year=selected_year,
                semester=selected_semester,
                paper_type=selected_paper_type, 
                question_paper_name=file.name,
                file_url=drive_link
            )

    # ✅ Add selected values to context
    context = {
        "details": details,
        "selected_regulation": selected_regulation,
        "selected_department": selected_department,
        "selected_year": selected_year,
        "selected_semester": selected_semester,
        "selected_paper_type": selected_paper_type,
    }

    return render(request, "home.html", context)
