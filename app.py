from flask import Flask, request, jsonify
from flask_cors import CORS
from qwen_api import send_request
from query import Neo4jQuery
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # 允许跨域请求

# 假数据
mock_data = [
    {
        "title": "机械革命极光X（i7-12800HX/16G/512G/RTX4060）",
        "description": ["性能还不错", "价格适中", "容易卡死", "这品控真的很看运气"],
        "link": "https://detail.zol.com.cn/notebook/index2066357.shtml",
        "image": "https://2a.zol-img.com.cn/product/267_500x375/164/ceGAQ3VacMbuY.png",
        "price": "6299",
        "weight": "2.2kg",
        "cpu": "Intel 酷睿 i7 12800HX",
        "memory": "16GB",
        "disk": "512GB",
        "gpu": "NVIDIA GeForce RTX 4060",
        "size": "16英寸",
        "ReleaseDate": "2024/7/1"
    },
    {
        "title": "荣耀X16 Plus 2024（R7 8845HS/16G/512G/780M集显）",
        "description": ["电脑性价比很高", "很流畅", "键盘比预想的手感要好", "价格便宜"],
        "link": "https://detail.zol.com.cn/notebook/index1990880.shtml",
        "image": "https://2f.zol-img.com.cn/product/260_500x375/929/ce4oUdtD79eg.jpg",
        "price": "4899",
        "weight": "2.2kg",
        "cpu": "Intel 酷睿 i7 12800HX",
        "memory": "16GB",
        "disk": "512GB",
        "gpu": "NVIDIA GeForce RTX 4060",
        "size": "16英寸",
        "ReleaseDate": "2024/3"
    },
    {
        "title": "七彩虹隐星P15 2024(i7 13620H/16GB/512GB/RTX4060)",
        "description": ["性能还不错", "价格适中", "容易卡死", "这品控真的很看运气"],
        "link": "https://detail.zol.com.cn/notebook/index2066357.shtml",
        "image": "https://2a.zol-img.com.cn/product/267_500x375/164/ceGAQ3VacMbuY.png",
        "price": "6299",
        "weight": "2.2kg",
        "cpu": "Intel 酷睿 i7 12800HX",
        "memory": "16GB",
        "disk": "512GB",
        "gpu": "NVIDIA GeForce RTX 4060",
        "size": "15.6英寸",
        "ReleaseDate": "2024年"
    }
]

@app.route('/analyze', methods=['POST'])
def analyze_text():
    # 获取用户输入文本
    data = request.json
    user_text = data.get('text', '')
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    print("User text:", user_text)
    request2neo4j = send_request("http://127.0.0.1:5050/chat", {"input": user_text})
    print("Request to Neo4j:", request2neo4j)
    # 分析逻辑（假设返回数据）
    data = Neo4jQuery(request2neo4j)
    print("Response data:", data)
    response = {
        "query": user_text,
        "data": data,
        "total": len(data),
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
