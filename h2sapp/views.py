from django.shortcuts import render
# from PyMuPDF import fitz
# Create your views here.
from django.http import JsonResponse
from django.urls import path
from . import views

def hello_api(request):
    return JsonResponse({'message': 'Hello from the backend!'})

def base(request):
    return render(request,'h2sapp/base.html')


def result(request):
    return render(request,'h2sapp/result.html')

import pdfplumber
# import fitz
from bs4 import BeautifulSoup
import requests
from PIL import Image
import io
import google.generativeai as genai
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import ModerationRequest

# Configure Gemini AI
genai.configure(api_key="AIzaSyA3hLtsWFRvJ5TAT4DciUWP-zJtKh8AIG8")
model = genai.GenerativeModel("gemini-1.5-pro")

def extract_text_from_url(url):
    """Extracts text from a given URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "lxml")
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.extract()
    return " ".join(soup.stripped_strings)[:5000]

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extract_text = page.extract_text()
            if extract_text:
                text += extract_text + "\n"
    return text

def analyze_content(content):
    """Analyze text content using Gemini AI."""
    prompt = f"""
    Analyze the following content for sensitive material:
    - Identify vulgar language.
    - Detect illegal activity intentions.
    - Provide a percentage of sensitive content.

    Content:
    {content}
    """
    response = model.generate_content(prompt)
    return response.text

def moderate_url(request):
    """Handles URL moderation requests."""
    if request.method == "POST":
        url = request.POST["url"]
        extracted_text = extract_text_from_url(url)
        analysis = analyze_content(extracted_text) if extracted_text else "Failed to extract content."

        # ModerationRequest.objects.create(url=url, analysis_result=analysis)
        return render(request, "h2sapp/result.html", {"result": analysis})
    
    return render(request, "h2sapp/url_form.html")

def moderate_document(request):
    """Handles document moderation requests."""
    if request.method == "POST" and request.FILES["document"]:
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        extracted_text = extract_text_from_pdf(file_path)
        analysis = analyze_content(extracted_text)

        # ModerationRequest.objects.create(document=uploaded_file, analysis_result=analysis)
        return render(request, "h2sapp/result.html", {"result": analysis})
    
    return render(request, "h2sapp/document_form.html")


from .models import ModeratedText

def text(request):
    return render(request,"text.html")
HATEFUL_KEYWORDS = ["hate", "stupid", "idiot","bigotry", "biased", "bitch", "brutal", "bully", "cancer", "ch*nk",
    "clown", "cockroach", "criminal", "cunt", "damn", "deadbeat", "delusional",
    "demon", "disgusting", "disgrace", "dumb", "enemy", "evil", "extremist",
    "failure", "fake", "fraud", "garbage", "harass", "hate", "hatred", "hell",
    "horrible", "idiot", "ignorant", "illegal", "imbecile", "inferior", "insane",
    "insult", "jerk", "joke", "kill", "loser", "lunatic", "menace", "moron",
    "nasty", "nazi", "nonsense", "offensive", "oppressor", "parasite", "pathetic",
    "pervert", "pest", "pig", "psycho", "racist", "rapist", "reject", "repulsive",
    "rubbish", "scum", "shameful", "sick", "slavery", "slur", "stupid", "terrorist",
    "thief", "threat", "trash", "ugly", "unworthy", "useless", "villain", "violent",
    "vulgar", "weak", "worthless", "wretched"
]

#  find to given text hate or not hate
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def analyze_text(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        is_hateful = any(word in text.lower() for word in HATEFUL_KEYWORDS)

        return render(request, "h2sapp/text.html", {"result": "hateful" if is_hateful else "safe"})
    return render(request, "h2sapp/text.html", {"error": "Invalid request"}, status=400)