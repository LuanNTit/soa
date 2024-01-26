import subprocess

services = [
    ("frontend", 8085),
    ("authentication", 8081),
    ("category_service", 8082),
    ("event_service", 8083),
    ("order_service", 8084),
    # ("test", 8086)
]

for service, port in services:
    command = f"flask --app {service} run --port {port}"
    subprocess.Popen(command, shell=True)
