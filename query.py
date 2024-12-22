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
            query += f' OR pr.range = "{conditions["预算"]}"'

        # 便携性筛选：重量
        if conditions["便携性"] == "便携":
            query += ' OR toFloat(p.weight) < 2.0'

        # CPU偏好筛选：Intel 或 AMD
        if conditions["CPU偏好"] == "Intel系列":
            query += ' OR c.model STARTS WITH "Intel"'
        elif conditions["CPU偏好"] == "AMD系列":
            query += ' OR c.model STARTS WITH "AMD"'

        # 性能需求筛选：GPU
        if conditions["性能需求"] == "极高性能":
            query += ' OR (g.model CONTAINS "4070" OR g.model CONTAINS "4080" OR g.model CONTAINS "4090")'
        elif conditions["性能需求"] == "高性能":
            query += ' OR (g.model CONTAINS "3050" OR g.model CONTAINS "4050" OR g.model CONTAINS "4060")'
        elif conditions["性能需求"] == "普通性能":
            query += ' OR NOT (g.model CONTAINS "4070" OR g.model CONTAINS "4080" OR g.model CONTAINS "4090" '
            query += ' OR g.model CONTAINS "3050" OR g.model CONTAINS "4050" OR g.model CONTAINS "4060")'

        # 屏幕尺寸筛选
        if conditions["屏幕尺寸偏好"] == "较小":
            query += ' OR toFloat(p.screen_size) < 15'
        elif conditions["屏幕尺寸偏好"] == "中等":
            query += ' OR toFloat(p.screen_size) < 16'
        elif conditions["屏幕尺寸偏好"] == "较大":
            query += ' OR toFloat(p.screen_size) >= 16'

        # 屏幕刷新率筛选
        if conditions["屏幕刷新率偏好"] == "刷新率较高":
            query += ' OR toFloat(p.screen_refresh_rate) >= 144'

        # 内存容量筛选
        if conditions["内存容量偏好"] == "较大":
            query += ' OR toInteger(p.memory) >= 32'

        # 返回结果
        query += """
        RETURN p.name AS title, p.link AS link, p.image AS image, p.price AS price, 
               p.weight AS weight, c.model AS cpu, p.memory AS memory, p.disk AS disk, 
               g.model AS gpu, p.screen_size AS size, p.release_date AS ReleaseDate
        LIMIT 5
        """
        return query

    def query_products(self, user_conditions):
        """
        执行查询并返回结果
        :param user_conditions: 用户输入条件字典
        :return: 查询结果列表
        """
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
                    "memory": record["memory"],
                    "disk": record["disk"],
                    "gpu": record["gpu"],
                    "size": record["size"],
                    "ReleaseDate": record["ReleaseDate"],
                }
                for record in result
            ]


def Neo4jQuery(user_conditions):
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "zzh123456@"
    handler = Neo4jQueryHandler(uri, username, password)
    try:
        # 查询结果
        results = handler.query_products(user_conditions)
        if results:
            print(results)
            return results
        else:
            print("未找到符合条件的产品。")
    finally:
        # 关闭数据库连接
        handler.close()

# 测试函数
def main():
    

    # 用户输入条件
    user_conditions = {
        '使用场景': '办公',
        '预算': '5000-6000',
        '便携性': '无',
        'CPU偏好': 'Intel系列',
        '性能需求': '高性能',
        '屏幕尺寸偏好': '无',
        '屏幕刷新率偏好': '无',
        '内存容量偏好': '无'
    }

    # 调用查询函数
    Neo4jQuery(user_conditions)

if __name__ == "__main__":
    main()
