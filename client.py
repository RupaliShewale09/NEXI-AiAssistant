import google.generativeai as genai
import os

Geminiapi = os.getenv("Geminiapi") 

genai.configure(api_key=Geminiapi)
model = genai.GenerativeModel("gemini-pro")

def aiProcess(command):
    response = model.generate_content(command)
    return response.text


command = "Tell me about Python Langauge"
print(aiProcess(command))

