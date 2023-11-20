from django.shortcuts import render

# view ----- INDEX
def index(request):
    return render(
        request,
        'contact/index.html',
    )
# view ----- INDEX