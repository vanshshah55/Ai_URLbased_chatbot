from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai



from dotenv import load_dotenv
import os
 
load_dotenv()
 
api_key = os.getenv('apikey')
url=os.getenv('your_url')
 





genai.configure(api_key=api_key)


def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = "\n".join([p.get_text() for p in paragraphs])
    return content


knowledge_base = scrape_content(url)

model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    prompt = f"User: {user_input}\nChatbot (limited to Microsoft Licensing Docs):"
    response = model.generate_content(f"{knowledge_base}\n\n{prompt}")
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)



