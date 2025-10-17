FROM docker.elastic.co/logstash/logstash:8.10.4

# Copy cấu hình logstash
COPY pipeline.conf /usr/share/logstash/pipeline/logstash.conf

# Cài plugin cần thiết
RUN logstash-plugin install logstash-filter-useragent

