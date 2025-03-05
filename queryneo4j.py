from neo4j import GraphDatabase

class Neo4jQueryHandler:
    def __init__(self, uri, username, password):
        """
        初始化 Neo4j 数据库连接
        :param uri: 数据库地址
        :param username: 用户名
        :param password: 密码
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        """
        关闭数据库连接
        """
        self.driver.close()

    def build_query(self, conditions):
        """
        根据用户输入条件动态生成 Cypher 查询语句
        :param conditions: 用户输入条件字典
        :return: Cypher 查询字符串
        """
        query = """
        MATCH (p:Product)-[:HAS_CPU]->(c:CPU),
              (p)-[:HAS_GPU]->(g:GPU),
              (p)-[:BELONGS_TO]->(cat:ProductCategory),
              (p)-[:IN_PRICE_RANGE]->(pr:PriceRange)
        WHERE 1=1
        """

        # 使用场景筛选：选择游戏本或轻薄本
        if conditions["使用场景"] in ["游戏", "编程", "影视后期"]:
            query += ' AND cat.name = "游戏本"'
        elif conditions["使用场景"] in ["办公", "学习"]:
            query += ' AND cat.name = "轻薄本"'

        # 预算筛选
        if "预算" in conditions:
            if conditions["预算"] == "1000-2000" or conditions["预算"] == "2000-3000" or conditions["预算"] =="3000-4000" or conditions["预算"] == "4000-5000" :
                query += f' AND pr.range = "{conditions["预算"]}"'
            else:
                query += f' OR pr.range = "{conditions["预算"]}"'

        # 便携性筛选：重量
        if conditions["便携性"] == "便携":
            query += ' AND toFloat(p.weight) < 2.0'

        # CPU偏好筛选：Intel 或 AMD
        if conditions["CPU偏好"] == "Intel系列":
            query += ' AND c.model CONTAINS "Intel"'
        elif conditions["CPU偏好"] == "AMD系列":
            query += ' AND c.model CONTAINS "AMD"'

        # 屏幕尺寸筛选
        if conditions["屏幕尺寸偏好"] == "较小":
            query += ' AND toFloat(p.screen_size) < 15'
        elif conditions["屏幕尺寸偏好"] == "中等":
            query += ' AND toFloat(p.screen_size) < 16'
        elif conditions["屏幕尺寸偏好"] == "较大":
            query += ' AND toFloat(p.screen_size) >= 16'

        query += ' AND ('   
        # 性能需求筛选：GPU
        if conditions["性能需求"] == "极高性能":
            query += ' (g.model CONTAINS "4070" OR g.model CONTAINS "4080" OR g.model CONTAINS "4090")'
        elif conditions["性能需求"] == "高性能":
            query += ' (g.model CONTAINS "3050" OR g.model CONTAINS "4050" OR g.model CONTAINS "4060")'
        elif conditions["性能需求"] == "普通性能":
            query += ' NOT (g.model CONTAINS "4070" OR g.model CONTAINS "4080" OR g.model CONTAINS "4090") '
    

        # 屏幕刷新率筛选
        if conditions["屏幕刷新率偏好"] == "刷新率较高":
            query += ' OR toFloat(p.screen_refresh_rate) >= 144'

        # 内存容量筛选
        if conditions["内存容量偏好"] == "较大":
            query += ' OR toInteger(p.memory) >= 32'

        query += ')'
        # 返回结果
        query += """
        RETURN p.name AS title, p.link AS link, p.image AS image, p.price AS price, 
               p.weight AS weight, c.model AS cpu, p.memory AS memory, p.disk AS disk, 
               g.model AS gpu, p.screen_size AS size, p.release_date AS ReleaseDate
        """
        return query

    def query_products(self, user_conditions):
        """
        执行查询并返回结果
        :param user_conditions: 用户输入条件字典
        :return: 查询结果列表
        """
        # 验证用户条件是否符合预期格式
        required_keys = ["使用场景", "预算", "便携性", "CPU偏好", "性能需求", "屏幕尺寸偏好", "屏幕刷新率偏好", "内存容量偏好"]
        for key in required_keys:
            if key not in user_conditions:
                print("未找到符合条件的产品。")
                return []  # 条件不完整时返回空列表

        cypher_query = self.build_query(user_conditions)
        print("生成的 Cypher 查询语句:")
        print(cypher_query)  # 打印生成的查询语句，便于调试

        with self.driver.session() as session:
            result = session.run(cypher_query)
            # 格式化返回结果
            return [
                {
                    "title": record["title"],
                    "link": record["link"],
                    "image": record["image"],
                    "price": record["price"],
                    "weight": record["weight"],
                    "cpu": record["cpu"],
                    "memory": str(record["memory"]) + "GB",
                    "disk": record["disk"],
                    "gpu": record["gpu"],
                    "size": str(record["size"])+ "英寸",
                    "ReleaseDate": record["ReleaseDate"],
                }
                for record in result
            ]


def Neo4jQuery(user_conditions):
    uri = "bolt://localhost:7687"
    username = "neo4j" # 默认用户名
    password = "password" # 默认密码
    handler = Neo4jQueryHandler(uri, username, password)
    try:
        # 查询结果
        results = handler.query_products(user_conditions)
        if results:
            print(results)
            return results
        else:
            print("未找到符合条件的产品。")
            return []
    finally:
        # 关闭数据库连接
        handler.close()

