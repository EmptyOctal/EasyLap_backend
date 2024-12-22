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