# scripts/fetch_logs.py

from elasticsearch import Elasticsearch
import pandas as pd
import warnings
import os

# Bỏ qua các cảnh báo không cần thiết
warnings.filterwarnings("ignore")

print("Connecting to Elasticsearch at http://localhost:9200...")
try:
    # Kết nối tới Elasticsearch service đang chạy trong Docker
    es = Elasticsearch("http://localhost:9200", request_timeout=30)

    # Kiểm tra kết nối
    if not es.ping():
        raise ConnectionError("Connection to Elasticsearch failed!")
    print("Connection successful.")

except Exception as e:
    print(f"Error connecting to Elasticsearch: {e}")
    exit()

# Query để lấy tất cả log từ các index có tiền tố "nginx-"
# Tăng size để lấy được nhiều log hơn (tối đa 10000 cho một request)
query = {
    "size": 10000,
    "query": {
        "match_all": {}
    }
}

print("Fetching logs from indices 'nginx-*'...")
try:
    response = es.search(index="nginx-*", body=query)
    
    # Lấy dữ liệu từ trường _source của mỗi hit
    all_hits = [hit['_source'] for hit in response['hits']['hits']]
    
    if not all_hits:
        print("\nWarning: No logs found!")
        print("Please run 'scripts/log_generator.py' for a few minutes and try again.")
    else:
        print(f"Successfully fetched {len(all_hits)} log entries.")

        # Chuyển đổi list các dictionary thành DataFrame của Pandas
        df = pd.DataFrame(all_hits)
        
        output_dir = 'data'
        os.makedirs(output_dir, exist_ok=True)
        
        # Lưu DataFrame ra file CSV
        output_path = os.path.join(output_dir, 'logs.csv')
        df.to_csv(output_path, index=False)
        print(f"Logs have been saved to '{output_path}'")

except Exception as e:
    print(f"\nAn error occurred during search: {e}")
    print("Please ensure the ELK stack is running and contains data.")
