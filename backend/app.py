# Flask backend entry

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import mysql.connector
import json
import fitz  # PyMuPDF for PDF parsing
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
CORS(app)

# Configurations
VECTOR_API_URL = "http://test.2brain.ai:9700/v1/emb"
SHUSHENG_API_URL = "http://test.2brain.ai:23333/v1"
ES_SEARCH_URL = "http://test.2brain.ai:9200/bee_beta_b_jobs_index/_search"
ES_AUTH = ("elastic", "O43eFzDVxf7qfwND4liMjzEq")

MYSQL_CONFIG = {
    'host': 'test.2brain.ai',
    'user': 'Track_B_2',
    'password': 'mfsd123_B_2',
    'database': 'bee_beta2'
}

def search_jobs_by_vector(vector, top_k=3):
    es_query = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": vector}
                }
            }
        }
    }
    es_response = requests.post(ES_SEARCH_URL, auth=ES_AUTH, json=es_query)
    es_data = es_response.json()

    if 'hits' not in es_data:
        return []

    job_hits = es_data['hits']['hits']
    job_results = [
        {
            "title": hit['_source']['title'],
            "location": hit['_source']['location'],
            "skills": hit['_source']['skills']
        } for hit in job_hits
    ]
    return job_results

# Upload and analyze resume
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # If PDF, extract text using PyMuPDF
    if file.filename.endswith('.pdf'):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            resume_text = "\n".join(page.get_text() for page in doc)
    else:
        resume_text = file.read().decode('utf-8')


    # Step 0. Inject category prompt
    category = request.form.get("category", "").strip()
    if category:
        resume_text += f"\n\n我对{category}方向感兴趣，请从该方向推荐相关岗位，并结合此方向分析我的简历。"

    # Step 1: Vector embedding
    vector_response = requests.post(VECTOR_API_URL, json={"texts": [resume_text]})
    try:
        vector_json = vector_response.json()
        vector_data = vector_json.get("data", {})
        text_vectors = vector_data.get("text_vectors", [])
    except Exception as e:
        return jsonify({"error": f"Failed to parse vector response: {str(e)}"}), 500

    if not isinstance(text_vectors, list) or len(text_vectors) == 0:
        return jsonify({"error": "Vector model did not return valid embedding"}), 500

    vector = text_vectors[0]
    job_results = search_jobs_by_vector(vector, top_k=4)

    # Step 3: Shusheng and chatgpt suggestion
#    prompt = f"请你扮演一位职业简历顾问。以下是用户上传简历，用户的兴趣是{category}, 请帮我诊断以下简历的优缺点并提供修改建议：\n{resume_text}"
#  shusheng_response = requests.post(
#        f"{SHUSHENG_API_URL}/chat/completions",
#        headers={"Content-Type": "application/json"},
#        json={
#            "model": "internvl-internlm2",
#            "messages": [{"role": "user", "content": prompt}]
#        }
#    )
    # suggestion = shusheng_response.json().get("response", "暂无建议")
#    suggestion = shusheng_response.json()["choices"][0]["message"]["content"]
    suggestion = get_suggestions_from_both_models(resume_text, category)
    openai_suggestion = suggestion["openai"]
    shusheng_suggestion = suggestion["shusheng"]
    # 合并成一个 markdown-friendly 字符串
    suggestion_combined = (
        "[ ✅ OpenAI 建议]\n"
        f"{openai_suggestion.strip()}\n"
        "[ 🧠 书生模型建议]\n"
        f"{shusheng_suggestion.strip()}"
    )
    #suggestion = call_shusheng_model(prompt)
    # Step 4: Save to MySQL
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    #cursor.execute(
    #    "INSERT INTO resumes (resume_text, suggestion, job_matches) VALUES (%s, %s, %s)",
    #    (resume_text, suggestion, json.dumps(job_results))
    #)
    cursor.execute(
        "INSERT INTO resumes (resume_text, suggestion, job_matches) VALUES (%s, %s, %s)",
        (resume_text, suggestion_combined, json.dumps(job_results))
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "score": round(len(resume_text) / 1000 * 5, 2),
        "suggestion": suggestion["openai"],
        "suggestion_shusheng": suggestion["shusheng"],
        "jobs": job_results
    })



def get_suggestions_from_both_models(resume_text, category):
    prompt = f"请你扮演一位职业简历顾问。以下是用户上传简历，用户的兴趣是{category}请帮我诊断简历的优缺点并提供修改建议:\n{resume_text}"

    # ---- Call OpenAI ----
    openai_suggestion = None
    if OPENAI_API_KEY:
        try:
            openai_response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
            openai_response.raise_for_status()
            openai_suggestion = openai_response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            openai_suggestion = f"[OpenAI Error] {str(e)}"

    # ---- Call Shusheng ----
    try:
        shusheng_response = requests.post(
            f"{SHUSHENG_API_URL}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "internvl-internlm2",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        shusheng_response.raise_for_status()
        shusheng_suggestion = shusheng_response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        shusheng_suggestion = f"[Shusheng Error] {str(e)}"

    return {
        "openai": openai_suggestion,
        "shusheng": shusheng_suggestion
    }





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
