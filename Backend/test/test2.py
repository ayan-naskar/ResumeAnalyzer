import requests

def get_job_recommendations(email: str):
    """Fetch job recommendations for a given email"""
    url = f"http://localhost:8000/resumes/recommend-jobs/{email}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Example Usage
email = "john.doe@example.com"
recommendations = get_job_recommendations(email)

print("Job Recommendations:", recommendations)
