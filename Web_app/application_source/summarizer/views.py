from django.shortcuts import render


def homepage_view(request):
    return render(request,"summarizer/index.html", {})

def summary_request_form_view(request):
    return render(request,"summarizer/summaryRequestForm.html", {})

def api_view(request):
    return render(request, "summarizer/api.html", {})




