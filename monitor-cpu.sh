#!/bin/bash

CPU_USAGE=80
TIME_INTERVAL=10  # Time interval to check CPU usage (in seconds)
SERVICE_NAME="my-laravel-service"  

function fetch_cpu_usage() {
    top -bn2 -d 1 | grep "Cpu(s)" | tail -n 1 | awk -F',' '{print $1}' | awk '{print $2 + $4}'
}

function restart_service() {
    local service_name=$1
    echo "Restarting service: $service_name"
    if systemctl restart "$service_name"; then
        echo "Service $service_name restarted successfully."
    else
        echo "Failed to restart service $service_name."
    fi
}

function watch_and_restart() {
    while true; do
        cpu_usage=$(fetch_cpu_usage)
        echo "Current CPU usage: $cpu_usage%"

        # Check if CPU usage exceeds threshold
        cpu_usage_integer=${cpu_usage%.*}
        if [ "$cpu_usage_integer" -gt "$CPU_USAGE" ]; then
            echo "CPU usage exceeded $CPU_USAGE%. Restarting service..."
            restart_service "$SERVICE_NAME"
        fi

        sleep "$TIME_INTERVAL"
    done
}

# Start monitoring
watch_and_restart
