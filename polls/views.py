from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "teacher/teacher_index.html", {})
