import requests

# Tests the Resume Context retrieval capability of the server

url = "http://localhost:8000/resumes/upload/"
file_path = r"C:\Users\ayann\Downloads\Simple_CSE_Resume.pdf"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

print(response.json())  # Check the stored data
