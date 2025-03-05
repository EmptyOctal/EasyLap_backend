from flask import Flask, request, jsonify
from flask_cors import CORS
from qwen_api import send_request
from queryneo4j import Neo4jQuery
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    user_text = data.get('text', '')
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    print("User text:", user_text)
    request2neo4j = send_request("http://127.0.0.1:5050/chat", {"input": user_text})
    data = Neo4jQuery(request2neo4j)
    response = {
        "query": user_text,
        "data": data,
        "total": len(data),
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5001) # 后端运行端口，默认5001