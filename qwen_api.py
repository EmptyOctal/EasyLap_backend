import requests
import json
from utils import convert

API_URL = "http://127.0.0.1:5050/chat"

def send_request(api_url, data):
    try:
        print("Sending request to API...")
        response = requests.post(api_url, json=data)
        
        # 检查 HTTP 状态码
        if response.status_code == 200:
            print("API Response:")
            res = json.loads(response.text).get("response")
            res = convert(res)
            return res
        else:
            print(f"Failed to call API. Status code: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error occurred while testing API: {e}")
        return None

# # 测试数据
# test_input = {
#     "input": "我想要一台性价比高的笔记本电脑，预算在5000-6000元之间，CPU最好是Intel系列。"
# }

# # 调用封装的函数发送请求
# response = send_request(API_URL, test_input)
# if response:
#     print(response)
