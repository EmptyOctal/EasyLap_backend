import re

def convert(input_string):
    # 定义固定的键
    keys = ["使用场景:", "预算:", "便携性:", "CPU偏好:", "性能需求:", "屏幕尺寸偏好:", "屏幕刷新率偏好:", "内存容量偏好:"]

    # 构造正则表达式
    pattern = r"({})".format("|".join(re.escape(key) for key in keys))

    # 使用正则分割字符串并解析
    parts = re.split(pattern, input_string)
    result = {}

    # 遍历分割后的部分，构造字典
    current_key = None
    for part in parts:
        part = part.strip(", ")
        if part in keys:  # 如果是键
            current_key = part[:-1]  # 去掉冒号
        elif current_key:  # 如果是值
            result[current_key] = part
            current_key = None
    return result

if __name__ == "__main__":
    # 定义字符串
    input_string = "使用场景: 游戏, 预算: 5000-6000, 便携性: 无, CPU偏好: Intel系列, 性能需求: 高性能, 屏幕尺寸偏好: 较小, 屏幕刷新率偏好: 无, 内存容量偏好: 无"

    # 输出结果
    print(convert(input_string))
