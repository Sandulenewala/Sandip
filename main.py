from flask import Flask, request, render_template, send_file, flash, redirect
import os
import re
import webtoword_1 as single_crawler
import webtoword_multi as multi_crawler
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'supersecretkey'
OUTPUT_DIR = os.path.join(os.getcwd(), "crawled_links_docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_filename(filename):
    filename = filename.strip()
    filename = filename.replace(".docx", "")
    filename = re.sub(r'[^A-Za-z0-9_-]', '', filename)
    if not filename:
        filename = "output"
    return filename

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/single-page", methods=["POST"])
def single_page():
    url = sanitize_url(request.form.get("username"))
    filename = sanitize_filename(request.form.get("filename"))

    if not is_valid_url(url):
        flash("❌ Invalid URL format. Please enter a complete domain like 'example.com'.")
        return redirect("/")

    try:
        single_crawler.main(url, filename)
        filepath = os.path.join(OUTPUT_DIR, f"{filename}.docx")
        print(f"Sending file: {filepath}")
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f"❌ Error crawling the page: {str(e)}")
        return redirect("/")

@app.route("/multi-page", methods=["POST"])
def multi_page():
    url = sanitize_url(request.form.get("username"))
    filename = sanitize_filename(request.form.get("filename"))

    if not is_valid_url(url):
        flash("❌ Invalid URL format. Please enter a complete domain like 'example.com'.")
        return redirect("/")

    try:
        multi_crawler.main(url, filename)
        filepath = os.path.join(OUTPUT_DIR, f"{filename}.docx")
        print(f"Sending file: {filepath}")
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f"❌ Error crawling the page: {str(e)}")
        return redirect("/")

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.run(host="0.0.0.0", port=5000, debug=True)
