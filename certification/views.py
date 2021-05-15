from django.shortcuts import render



# Organic Certificate.
def organic_certificate(request):
    return render(request, 'certification/organic_certificate.html')
