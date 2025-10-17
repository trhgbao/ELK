import requests
import time
import random

BASE_URL = "http://127.0.0.1:8080"

def simulate_normal_traffic(duration_minutes=1):
    """Mô phỏng người dùng bình thường, truy cập các trang khác nhau với độ trễ ngẫu nhiên."""
    print(f"--- Simulating NORMAL traffic for {duration_minutes} minute(s) ---")
    end_time = time.time() + duration_minutes * 60
    while time.time() < end_time:
        try:
            # Các trang người dùng thường truy cập
            pages = ["/", "/index.html", "/products", "/about-us"]
            requests.get(f"{BASE_URL}{random.choice(pages)}", timeout=2)
            print(".", end='', flush=True)
        except requests.exceptions.RequestException:
            print("E", end='', flush=True) # Lỗi kết nối
        
        # Người dùng nghỉ ngơi ngẫu nhiên
        time.sleep(random.uniform(0.5, 3))
    print("\nNormal traffic simulation finished.")

def simulate_brute_force_attack(attempts=30):
    """Mô phỏng tấn công dò mật khẩu vào trang đăng nhập."""
    print(f"\n!!! Simulating ANOMALY: Brute-force attack on /login ({attempts} attempts) !!!")
    for i in range(attempts):
        try:
            # Giả sử /login trả về lỗi 401 hoặc 404
            requests.get(f"{BASE_URL}/login", timeout=2)
            print("x", end='', flush=True)
        except requests.exceptions.RequestException:
            print("E", end='', flush=True)
        
        # Tấn công diễn ra rất nhanh
        time.sleep(0.1)
    print("\nBrute-force attack finished.")
    
def simulate_scanning_attack(pages_to_scan=50):
    """Mô phỏng bot đang quét các đường dẫn có thể tồn tại trên web."""
    print(f"\n!!! Simulating ANOMALY: Directory scanning attack ({pages_to_scan} pages) !!!")
    for i in range(pages_to_scan):
        try:
            # Cố gắng truy cập các trang không tồn tại
            requests.get(f"{BASE_URL}/admin_backup/config_{i}.txt", timeout=2)
            print("s", end='', flush=True)
        except requests.exceptions.RequestException:
            print("E", end='', flush=True)

        time.sleep(0.2)
    print("\nScanning attack finished.")

if __name__ == "__main__":
    # --- KỊCH BẢN DEMO ---
    # Chạy traffic bình thường trong 1 phút
    simulate_normal_traffic(duration_minutes=1)

    # Chờ một chút
    time.sleep(5)

    # Bắt đầu các kịch bản tấn công
    simulate_brute_force_attack(attempts=40)
    time.sleep(5)
    simulate_scanning_attack(pages_to_scan=60)
