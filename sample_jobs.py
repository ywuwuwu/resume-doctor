import json
import random
import requests

titles = [
    "Machine Learning Engineer", "Data Scientist", "Backend Developer",
    "Frontend Developer", "DevOps Engineer", "Cloud Architect",
    "AI Researcher", "Mobile App Developer", "NLP Engineer", "Computer Vision Scientist"
]

locations = ["San Francisco, CA", "New York, NY", "Remote", "Austin, TX", "Seattle, WA"]

skills_pool = [
    "Python", "PyTorch", "TensorFlow", "SQL", "JavaScript", "React",
    "Docker", "Kubernetes", "AWS", "GCP", "NLP", "Computer Vision",
    "C++", "Java", "Rust", "Node.js", "TypeScript", "Scikit-learn"
]

jobs = []

VECTOR_API = "http://test.2brain.ai:9700/v1/emb"

def get_embedding(text):
    payload = {"texts": [text]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(VECTOR_API, json=payload, headers=headers)
    response_json = response.json()
    
    if response.status_code == 200 and "data" in response_json and "text_vectors" in response_json["data"]:
        return response_json["data"]["text_vectors"][0]
    else:
        raise ValueError(f"Invalid vector response: {response_json}")


#  构造职位 + 向量字段
for i in range(10):
    job = {
        "title": titles[i],
        "description": f"We are looking for a {titles[i]} to join our team. Must have experience with modern tools and frameworks.",
        "location": random.choice(locations),
        "skills": random.sample(skills_pool, k=4)
    }
    job_text = job["title"] + " " + job["description"] + " " + " ".join(job["skills"])
    embedding = get_embedding(job_text)
    job["embedding"] = embedding
    jobs.append(job)

# 保存为 JSON 文件
with open("data/sample_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print(" Successfully saved 10 embedded job records.")
