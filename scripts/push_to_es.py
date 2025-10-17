# scripts/push_to_es.py

import pandas as pd
from elasticsearch import Elasticsearch, helpers
import warnings
import numpy as np
import json

# --- CẤU HÌNH ---
ES_HOST = "http://localhost:9200"
CSV_FILE_PATH = 'data/final_logs_with_anomalies.csv'
INDEX_NAME = 'nginx-anomalies'

# --- ĐỌC DỮ LIỆU CSV VÀ CHUYỂN ĐỔI KIỂU DỮ LIỆU ---
print(f"Reading data from '{CSV_FILE_PATH}'...")
try:
    # parse_dates=['@timestamp'] sẽ bảo Pandas tự động chuyển đổi cột này thành datetime
    df = pd.read_csv(CSV_FILE_PATH, parse_dates=['@timestamp'])
    
    # Thay thế các giá trị NaN bằng None (tương đương null trong JSON)
    df = df.replace({np.nan: None})
    print(f"Successfully read {len(df)} rows.")
except FileNotFoundError:
    print(f"Error: File not found at '{CSV_FILE_PATH}'. Please run the notebooks first.")
    exit()

# --- ĐỊNH NGHĨA MAPPING CHO INDEX MỚI ---
INDEX_MAPPING = {
    "properties": {
        "@timestamp": {"type": "date"},
        "geoip": {"type": "object", "enabled": False},
        "useragent": {"type": "object", "enabled": False},
        "status": {"type": "integer"},
        "body_bytes_sent": {"type": "integer"},
        "is_anomaly": {"type": "boolean"}
    }
}

# --- HÀM CHUẨN BỊ DỮ LIỆU ---
def generate_actions(dataframe, index_name):
    if 'is_anomaly' in dataframe.columns and dataframe['is_anomaly'].dtype == 'object':
         dataframe['is_anomaly'] = dataframe['is_anomaly'].apply(lambda x: x.lower() == 'true' if isinstance(x, str) else bool(x))
            
    for index, row in dataframe.iterrows():
        record = row.to_dict()
        for field in ['geoip', 'useragent', 'log']:
            if field in record and isinstance(record[field], str):
                try:
                    record[field] = json.loads(record[field].replace("'", "\""))
                except json.JSONDecodeError:
                    record[field] = None
        if '@timestamp' in record and pd.notna(record['@timestamp']):
            record['@timestamp'] = record['@timestamp'].isoformat()
        yield {
            "_index": index_name,
            "_source": record
        }

# --- KẾT NỐI VÀ ĐẨY DỮ LIỆU LÊN ---
try:
    # 1. Kết nối Elasticsearch
    print(f"Connecting to Elasticsearch at {ES_HOST}...")
    es = Elasticsearch(ES_HOST, request_timeout=30)
    if not es.ping():
        raise ConnectionError("Connection failed!")
    print("Connection successful.")

    # 2. Xóa index cũ nếu tồn tại
    if es.indices.exists(index=INDEX_NAME):
        print(f"Deleting old index '{INDEX_NAME}'...")
        es.indices.delete(index=INDEX_NAME)
    
    # 3. Tạo index mới với mapping
    print(f"Creating new index '{INDEX_NAME}' with explicit mapping...")
    es.indices.create(index=INDEX_NAME, mappings=INDEX_MAPPING)
    
    # 4. Đẩy dữ liệu
    print("Pushing data using bulk API...")
    helpers.bulk(es, generate_actions(df, INDEX_NAME))
    print("Successfully pushed all data to Elasticsearch.")

except Exception as e:
    print(f"An error occurred: {e}")
