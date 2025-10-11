# Giám sát Log Nginx với ELK Stack trên Docker

Đây là một dự án demo minh họa cách sử dụng **ELK Stack (Elasticsearch, Logstash, Kibana)** để xây dựng một hệ thống giám sát và quản lý log tập trung cho máy chủ web Nginx. Toàn bộ hệ thống được triển khai dễ dàng thông qua **Docker Compose**.

---

## 🚀 Tính năng nổi bật

-   **Ghi log Tập trung:** Thu thập log từ Nginx và tập trung về một nơi duy nhất.
-   **Xử lý và Làm giàu Dữ liệu:** Logstash tự động phân tích cấu trúc log JSON, đồng thời làm giàu dữ liệu bằng cách thêm thông tin vị trí địa lý (GeoIP) từ địa chỉ IP của client.
-   **Tìm kiếm và Phân tích Nhanh chóng:** Elasticsearch cung cấp khả năng tìm kiếm toàn văn và phân tích dữ liệu log gần như thời gian thực.
-   **Trực quan hóa Dữ liệu:** Xây dựng Dashboard tương tác trên Kibana để giám sát các chỉ số quan trọng:
    -   Lưu lượng truy cập theo thời gian.
    -   Thống kê mã trạng thái HTTP (200, 404, 500...).
    -   Top các địa chỉ IP truy cập nhiều nhất.
    -   Bản đồ phân bố vị trí địa lý của người dùng.
-   **Triển khai Dễ dàng:** Toàn bộ stack được đóng gói và khởi chạy chỉ bằng một lệnh duy nhất với Docker Compose.

---

## 🛠️ Công nghệ sử dụng

-   🐋 **Docker & Docker Compose:** Để đóng gói và quản lý các container.
-   🔍 **Elasticsearch:** Để lưu trữ, tìm kiếm và phân tích log.
-   🪵 **Logstash:** Để thu thập, xử lý và chuyển tiếp log.
-   📊 **Kibana:** Để trực quan hóa dữ liệu và tạo dashboard.
-   🌐 **Nginx:** Máy chủ web dùng làm nguồn log mẫu.

---

## 🏗️ Kiến trúc & Luồng dữ liệu

Luồng di chuyển của dữ liệu log trong dự án này rất đơn giản và rõ ràng:

`Client` → `Nginx (Tạo log)` → `Logstash (Thu thập & Xử lý)` → `Elasticsearch (Lưu trữ & Đánh chỉ mục)` → `Kibana (Trực quan hóa & Phân tích)`

---

## ⚙️ Hướng dẫn Cài đặt và Chạy dự án

### Yêu cầu
-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)

### Các bước thực hiện

1.  **Clone repository về máy:**
    ```bash
    git clone https://github.com/TEN_CUA_BAN/TEN_REPOSITORY.git
    cd TEN_REPOSITORY
    ```
    *(Nhớ thay thế `TEN_CUA_BAN` và `TEN_REPOSITORY` bằng thông tin thật của bạn)*

2.  **Khởi chạy toàn bộ hệ thống:**
    ```bash
    docker-compose up -d
    ```
    Hệ thống sẽ cần vài phút để khởi tạo ở lần chạy đầu tiên.

3.  **Kiểm tra trạng thái các container:**
    ```bash
    docker-compose ps
    ```
    Bạn sẽ thấy 4 container `elasticsearch`, `logstash`, `kibana`, `nginx` đang ở trạng thái `Up` hoặc `running`.

---

## Hướng dẫn Sử dụng

1.  **Tạo dữ liệu log mẫu:**
    -   Mở trình duyệt và truy cập vào máy chủ Nginx tại: `http://localhost:8080`
    -   Tải lại trang (F5) nhiều lần.
    -   Thử truy cập một vài đường dẫn không tồn tại để tạo lỗi 404, ví dụ: `http://localhost:8080/test`, `http://localhost:8080/random-page`.

2.  **Truy cập Kibana:**
    -   Mở một tab mới và truy cập vào giao diện Kibana: `http://localhost:5601`

3.  **Cấu hình Index Pattern:**
    -   Trong giao diện Kibana, vào menu **Stack Management > Index Patterns**.
    -   Nhấn **Create index pattern**.
    -   Trong ô **Index pattern name**, gõ `nginx-*`.
    -   Ở bước tiếp theo, chọn `@timestamp` làm trường thời gian (Time field).
    -   Nhấn **Create index pattern** để hoàn tất.

4.  **Khám phá Dữ liệu:**
    -   Vào menu **Discover** để xem và tìm kiếm các dòng log đã được thu thập và phân tích. Bạn sẽ thấy các trường như `status`, `remote_addr`, `geoip` đã được tách ra rõ ràng.
    -   Vào menu **Dashboard** để xem bảng điều khiển giám sát đã được dựng sẵn.

5.  **Dừng hệ thống:**
    Để tắt toàn bộ hệ thống, chạy lệnh sau trong thư mục dự án:
    ```bash
    docker-compose down
    ```
