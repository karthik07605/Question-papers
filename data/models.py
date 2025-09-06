from django.db import models

class Regulation(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Paper(models.Model):
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(max_length=10, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    semester = models.CharField(max_length=10, choices=[('1', '1'), ('2', '2')])
    paper_type = models.CharField(
        max_length=50,
        choices=[('mid', 'MID'), ('semester', 'SEMESTER'), ('questionbank', 'QUESTIONBANK')],
    )
    question_paper_name = models.CharField(max_length=100, default="newpaper")
    file_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.question_paper_name
