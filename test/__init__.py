import requests

# Thực hiện một request API (ví dụ)
response = requests.get("http://localhost:8081/protected")

# Kiểm tra trạng thái của response
if response.status_code == 200:
    try:
        # Giả sử response.text là chuỗi JSON
        json_data = response.json()
        print(json_data)
    except Exception as e:
        print(f"Error decoding JSON: {e}")
else:
    print(f"Request failed with status code {response.status_code}")