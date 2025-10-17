# Bắt đầu từ image Nginx chính thức
FROM nginx:latest

# Tạo thư mục log và cấp quyền cho user 'nginx'.
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx
