from django.shortcuts import render
from .models import Paper, Regulation, Department
from .gdrive import upload_to_drive  # Import Google Drive function

def home(request):
    details = []
    selected_regulation = ""
    selected_department = ""
    selected_year = ""
    selected_semester = ""
    selected_paper_type = ""

    # Fetch dynamic dropdown data
    regulations = Regulation.objects.all()
    departments = Department.objects.all()

    if request.method == "POST":
        selected_regulation = request.POST.get("regulation", "")
        selected_department = request.POST.get("department", "")
        selected_year = request.POST.get("year", "")
        selected_semester = request.POST.get("semester", "")
        selected_paper_type = request.POST.get("paper_type", "")
        file = request.FILES.get("file")

        # Filter papers dynamically
        if selected_regulation and selected_department and selected_year and selected_semester and selected_paper_type:
            details = Paper.objects.filter(
                regulation__name=selected_regulation,
                department__name=selected_department,
                year=selected_year,
                semester=selected_semester,
                paper_type=selected_paper_type,
            )

        # Upload file to Google Drive + save in DB
        if file:
            drive_link = upload_to_drive(file, file.name)
            Paper.objects.create(
                regulation=Regulation.objects.get(name=selected_regulation),
                department=Department.objects.get(name=selected_department),
                year=selected_year,
                semester=selected_semester,
                paper_type=selected_paper_type,
                question_paper_name=file.name,
                file_url=drive_link
            )

    context = {
        "details": details,
        "selected_regulation": selected_regulation,
        "selected_department": selected_department,
        "selected_year": selected_year,
        "selected_semester": selected_semester,
        "selected_paper_type": selected_paper_type,
        "regulations": regulations,
        "departments": departments,
    }
    return render(request, "home.html", context)
