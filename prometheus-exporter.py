import os
import time
import requests
from prometheus_client import start_http_server, Gauge
 
# Environment Variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "admin")
 
SERVER_PORT = int(os.getenv("EXPORTER_PORT", "8000"))
 
# Define Prometheus Gauges
QUEUE_MESSAGES = Gauge(
    "rabbitmq_individual_queue_messages",
    "Total messages in queue",
    ["host", "vhost", "name"]
)
QUEUE_MESSAGES_READY = Gauge(
    "rabbitmq_individual_queue_messages_ready",
    "Messages ready in queue",
    ["host", "vhost", "name"]
)
QUEUE_MESSAGES_UNACKED = Gauge(
    "rabbitmq_individual_queue_messages_unacknowledged",
    "Unacknowledged messages in queue",
    ["host", "vhost", "name"]
)
 
HTTP_RABBITMQ_QUEUE_PATH = "api/queues"
 
 
def get_queue_data():
    url = f"http://{RABBITMQ_HOST}:{RABBITMQ_PORT}/{HTTP_RABBITMQ_QUEUE_PATH}"
    response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
    try:
        response.raise_for_status()
        return response.json()
    except:
        return []
 
 
def sync_metrics():
    queues = get_queue_data()
    for queue in queues:
        vhost = queue.get("vhost", "unknown")
        name = queue.get("name", "unknown")
 
        QUEUE_MESSAGES.labels(
            host=RABBITMQ_HOST, vhost=vhost, name=name
        ).set(queue.get("messages", 0))
        QUEUE_MESSAGES_READY.labels(
            host=RABBITMQ_HOST, vhost=vhost, name=name
        ).set(messages_ready = queue.get("messages_ready", 0))
        QUEUE_MESSAGES_UNACKED.labels(
            host=RABBITMQ_HOST, vhost=vhost, name=name
        ).set(queue.get("messages_unacknowledged", 0))
 
 
def main():
    start_http_server(SERVER_PORT)
 
    while True:
        sync_metrics()
        time.sleep(10.0)
 
if __name__ == "__main__":
    main()