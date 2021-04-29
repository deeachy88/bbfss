from django.shortcuts import render


# Create your views here.
def inspection_and_monitoring(request):
    return render(request, 'food/inspection_and_monitoring.html')
