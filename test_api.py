import requests

url = "http://127.0.0.1:5000/analyze"

# 测试输入文本
payload = {
    "text": "推荐一些16GB内存的笔记本"
}

# 发送 POST 请求
response = requests.post(url, json=payload)

# 输出结果
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
