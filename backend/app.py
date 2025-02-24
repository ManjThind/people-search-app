
from flask import Flask, request, jsonify, send_file
import requests
from bs4 import BeautifulSoup
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# API KEYS (Replace with your keys)
SERP_API_KEY = "your_serpapi_key"

# Google Search Function (SerpAPI)
def google_search(name):
    search_url = f"https://serpapi.com/search.json?q={name}&api_key={SERP_API_KEY}"
    response = requests.get(search_url)
    return response.json().get("organic_results", [])

# Generate PDF Report
def generate_pdf(name, search_results):
    pdf_path = f"{name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, f"Search Report for {name}")
    c.drawString(100, 730, "-" * 40)

    y = 700
    for result in search_results:
        c.drawString(100, y, f"{result.get('title')} - {result.get('link')}")
        y -= 20
        if y < 100:
            c.showPage()
            y = 750

    c.save()
    return pdf_path

@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Please provide a name"}), 400

    search_results = google_search(name)
    pdf_path = generate_pdf(name, search_results)

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    