from django.shortcuts import render

def home(request):
    context = {
        "name": "Ermiyas",
        "profession": "Software Developer",
        "numbers": [1, 2, 3, 4, 5]
    }
    return render(request, "home.html", context)
