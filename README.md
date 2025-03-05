# EasyLap_backend

## 运行方法

**我们的自建neo4j数据库暂未公开，如有部署需求，可以先联系我们获取数据库。**

先安装运行所需环境
```bash
pip install -r requirements.txt
```
然后，直接运行main.py即可
```bash
python main.py
```

由于本项目部署使用微调后的Qwen-7B大模型，如本地算力不够，可部署到[autodl](https://www.autodl.com/)。我们用了一张4090显卡可流畅运行。

将模型部署在autodl的话，可利用[SSH隧道进行端口映射](https://www.autodl.com/docs/ssh_proxy/)与前端进行连接。
![](https://picbed.octalzhihao.top/img/202503050902214.png)

**注意将远程代理端口号和代码运行端口保持一致。**
默认使用5001端口，如需要自定义，直接修改main.py中的运行端口即可：
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001) # 后端运行端口，默认5001
```

## API 文档

### **1. Endpoint**

`POST /analyze`

### **2. 请求参数**

| 参数   | 类型   | 必需 | 描述              |
|--------|--------|------|-------------------|
| `text` | string | 是   | 用户输入的文本内容 |

请求示例：

```json
{
    "text": "推荐一些16GB内存的笔记本"
}
```

### **3. 响应字段**

| 字段             | 类型   | 描述                       |
|------------------|--------|----------------------------|
| `query`          | string | 用户输入的查询文本         |
| `results`        | array  | 搜索结果列表               |
| `results[].title`| string | 笔记本标题                 |
| `results[].description` | array | 笔记本的简要描述       |
| `results[].link` | string | 笔记本详情链接             |
| `results[].image`| string | 笔记本图片链接             |
| `results[].price`| string | 笔记本价格                 |
| `results[].weight`| string | 笔记本重量               |
| `results[].cpu`  | string | 处理器规格                 |
| `results[].memory`| string | 内存规格                  |
| `results[].disk` | string | 硬盘规格                   |
| `results[].gpu`  | string | 显卡规格                   |
| `results[].size` | string | 屏幕尺寸                   |
| `results[].ReleaseDate` | string | 发布日期            |
| `total_results`  | number | 搜索结果总数               |

响应示例：

```json
{
    "query": "推荐一些16GB内存的笔记本",
    "data": [
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
        }
    ],
    "total": 3
}
```
