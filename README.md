# Giám sát Log và Phát hiện Bất thường bằng ELK Stack và Machine Learning

Dự án này trình bày một giải pháp hoàn chỉnh để thu thập, giám sát và phân tích log hệ thống Nginx trong thời gian thực bằng cách sử dụng ELK Stack (Elasticsearch, Logstash, Kibana). Điểm nổi bật của dự án là việc tích hợp một mô hình Machine Learning (Isolation Forest) để tự động phát hiện các hành vi bất thường như tấn công Brute-force và quét lỗ hổng web.

![Kibana Anomaly Dashboard Demo]

---

## 🚀 Tính năng chính

- **Thu thập & Ghi log tập trung:** Sử dụng Nginx để tạo log và Logstash để thu thập, xử lý và làm giàu dữ liệu (GeoIP, User-Agent).
- **Lưu trữ & Tìm kiếm hiệu quả:** Dùng Elasticsearch để lưu trữ và lập chỉ mục hàng triệu dòng log, cho phép tìm kiếm và truy vấn gần như ngay lập tức.
- **Trực quan hóa mạnh mẽ:** Xây dựng hai dashboard trên Kibana:
    - **System Overview:** Giám sát tổng quan tình trạng hệ thống (lượng truy cập, mã trạng thái, vị trí địa lý...).
    - **Anomaly Detection:** Tập trung hiển thị các cảnh báo an ninh được phát hiện bởi mô hình AI.
- **Phát hiện Bất thường bằng AI:**
    - Sử dụng mô hình **Isolation Forest** (Học không giám sát) để học các mẫu hành vi bình thường.
    - Tự động phát hiện và gán nhãn các hoạt động đáng ngờ dựa trên các đặc trưng như tần suất request, số lượng URL duy nhất, tỷ lệ lỗi...

---

## 🛠️ Công nghệ sử dụng

- **Containerization:** Docker & Docker Compose
- **ELK Stack (v8.10.4):**
    - **Elasticsearch:** Lưu trữ, tìm kiếm và phân tích.
    - **Logstash:** Pipeline xử lý log.
    - **Kibana:** Trực quan hóa và tạo dashboard.
- **Web Server:** Nginx
- **AI & Data Science:**
    - **Python 3.12**
    - **Thư viện:** Pandas, Scikit-learn, Elasticsearch-py, Jupyter Notebook.
- **Mô hình:** Isolation Forest

---

## 📂 Cấu trúc thư mục

```
project-anomaly-detection/
│
├── docker-compose.yml         # File điều phối chính của Docker
├── requirements.txt           # Các thư viện Python cần thiết
├── .gitignore                 # Các file/thư mục cần bỏ qua
├── README.md                  # File bạn đang đọc
│
├── logstash/                  # Cấu hình cho Logstash
│   ├── Dockerfile
│   └── pipeline.conf
│
├── nginx/                     # Cấu hình cho Nginx
│   └── default.conf
│
├── scripts/                   # Các script tự động hóa
│   ├── log_generator.py       # Script tạo log giả (thường & bất thường)
│   ├── fetch_logs.py          # Script lấy log từ Elasticsearch
│   └── push_to_es.py          # Script đẩy kết quả AI vào Elasticsearch
│
├── notebooks/                 # Phân tích dữ liệu và huấn luyện mô hình
│   ├── 01_preprocess.ipynb
│   └── 02_train_model.ipynb
│
└── ...
```

---

## 🏁 Hướng dẫn cài đặt và chạy dự án

### Yêu cầu
- Docker và Docker Compose đã được cài đặt.
- Python 3.10+ và pip.

### Các bước thực hiện

**1. Clone repository về máy:**
```bash
git clone https://github.com/trhgbao/ELK.git
cd project-anomaly-detection
```

**2. Tạo và kích hoạt môi trường ảo Python:**
```bash
python3 -m venv .venv
source venv/bin/activate
```

**3. Cài đặt các thư viện Python cần thiết:**
```bash
pip install -r requirements.txt
```

**4. Khởi động hệ thống ELK Stack:**
Lệnh này sẽ build các image cần thiết và khởi động 4 container (elasticsearch, logstash, kibana, nginx) ở chế độ nền.
```bash
docker-compose up -d```
*Lưu ý: Lần đầu khởi động có thể mất vài phút để tải các image từ Docker Hub. Hãy chờ đến khi tất cả các service báo "done" hoặc "healthy".*
```

**5. Tạo dữ liệu log:**
Để hệ thống có dữ liệu để phân tích, hãy chạy script mô phỏng traffic trong vài phút.

Mở một terminal mới và di chuyển vào thư mục dự án.

```bash
# Kích hoạt môi trường ảo
source venv/bin/activate
```bash
# Chạy script tạo log
python3 scripts/log_generator.py
```
*Script này sẽ mô phỏng cả traffic bình thường và các cuộc tấn công. Hãy để nó chạy khoảng 3-5 phút rồi dừng lại bằng `Ctrl + C`.*

***6. Chạy Pipeline AI**

Thực thi pipeline để lấy dữ liệu, huấn luyện mô hình và đẩy kết quả phân tích trở lại Elasticsearch.

**a. Chuẩn bị môi trường cho Jupyter (Chỉ làm một lần)**

Để Jupyter Notebook nhận đúng môi trường ảo của dự án, hãy chạy lệnh sau:
```bash
pip install ipykernel
python -m ipykernel install --user --name="anomaly-detection-venv" --display-name="Python (Anomaly Detection)"
```

**b. Lấy dữ liệu và Huấn luyện mô hình**

1.  **Lấy dữ liệu log:**
    ```bash
    python scripts/fetch_logs.py
    ```

2.  **Huấn luyện mô hình:**
    - Khởi động Jupyter: `jupyter notebook`
    - Mở các file trong thư mục `notebooks/`, **chọn kernel "Python (Anomaly Detection)"** (`Kernel > Change kernel`).
    - Chạy lần lượt các notebook `01_preprocess.ipynb` và `02_train_model.ipynb`.

**c. Đẩy kết quả phân tích lên Elasticsearch**
```bash
python scripts/push_to_es.py
```
*Sau bước này, index `nginx-anomalies` sẽ được tạo ra, chứa dữ liệu đã được AI gán nhãn.*
**7. Khám phá kết quả trên Kibana**

Trực quan hóa dữ liệu đã được phân tích trên giao diện Kibana.

- **Truy cập Kibana:** `http://localhost:5601`

- **Tạo Data Views (Index Patterns):**
    - Vào **Stack Management > Data Views** và tạo 2 data views:
        1.  **`nginx-*`**: Dành cho log gốc của hệ thống.
        2.  **`nginx-anomalies*`**: Dành cho kết quả đã được phân tích bởi AI.
    - *Với mỗi data view, hãy chọn `@timestamp` làm trường thời gian.*

- **Khám phá Dashboard:**
    - Quay lại mục **Dashboard** để bắt đầu xây dựng các biểu đồ.
    - Để giám sát các cảnh báo an ninh, hãy tạo biểu đồ trên data view `nginx-anomalies*` và áp dụng bộ lọc `is_anomaly is true`.
