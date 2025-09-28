import json
from elasticsearch import Elasticsearch, helpers, exceptions

# ES 配置信息
ES_HOST = "http://test.2brain.ai:9200"
ES_USERNAME = "elastic"
ES_PASSWORD = "O43eFzDVxf7qfwND4liMjzEq"
INDEX_NAME = "bee_beta_b_jobs_index"

# 初始化 Elasticsearch 客户端
es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    verify_certs=False
)
# es.indices.delete(index=INDEX_NAME)
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(
        index=INDEX_NAME,
        body={
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "location": {"type": "keyword"},
                    "skills": {"type": "keyword"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 1024
                    }
                }
            }
        }
    )
    print(f"Created index with mapping: {INDEX_NAME}")
else:
    print(f"Index {INDEX_NAME} already exists")


# 加载本地 JSON 数据
with open("sample_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# 构建上传的批量数据
actions = [
    {
        "_index": INDEX_NAME,
        "_source": job
    }
    for job in jobs
]

# 创建索引（如果不存在）
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)
    print(f"Created index: {INDEX_NAME}")

# 执行批量上传
helpers.bulk(es, actions)
print(f"Successfully uploaded {len(actions)} job records to index: {INDEX_NAME}")
