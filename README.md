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
source .venv/bin/activate
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

**5. Tạo dữ liệu log:**
Mở một terminal mới, kích hoạt môi trường ảo và chạy script `log_generator.py` trong vài phút.
```bash
source .venv/bin/activate
python scripts/log_generator.py
```
*Script này sẽ mô phỏng traffic bình thường và các cuộc tấn công để tạo dữ liệu cho hệ thống.*

**6. Chạy Pipeline AI:**
Đây là bước thực thi toàn bộ quy trình Machine Learning.```bash
# Lấy log từ Elasticsearch về file CSV
python scripts/fetch_logs.py

# (Tùy chọn) Mở các notebook để xem chi tiết các bước xử lý và huấn luyện
# jupyter notebook

# Đẩy kết quả đã được gán nhãn bởi AI vào một index mới
python scripts/push_to_es.py
```

**7. Truy cập và khám phá trên Kibana:**
- Mở trình duyệt và truy cập: `http://localhost:5601`
- **Tạo Index Pattern:**
    - Vào **Stack Management > Index Patterns > Create index pattern**.
    - Tạo một pattern cho log gốc: `nginx-*`.
    - Tạo một pattern khác cho log đã qua xử lý bởi AI: `nginx-anomalies*`.
- **Khám phá Dashboard:**
    - Vào mục **Dashboard**. Bạn có thể import các dashboard đã được thiết kế sẵn hoặc tự tạo mới để khám phá dữ liệu.
