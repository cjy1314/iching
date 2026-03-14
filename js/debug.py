import re
import json
import os

# 切换到JS目录
os.chdir(r'C:\Users\cjy\WorkBuddy\IChing\js')

def extract_data(file_path):
    """从JS文件中提取数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尝试匹配 exports.xxx = [...] 或 module.exports = [...]
    # 需要找到 = 后面开始的 [
    patterns = [
        r'exports\.\w+\s*=\s*(\[)',
        r'module\.exports\s*=\s*(\[)',
    ]
    
    start_pos = None
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            # 找到 = 后面的 [ 位置
            start_pos = match.end() - 1  # 回到 [ 位置
            print(f"  Found array start at position {start_pos}")
            break
    
    if start_pos is None:
        print(f"  No pattern found!")
        return None
    
    # 找到数组的结束位置
    content_stripped = content.rstrip()
    # 尝试多种结束模式
    end_pos = -1
    for end_pattern in ['];', '];\n', ']']:
        end_pos = content_stripped.rfind(end_pattern)
        if end_pos != -1:
            # 如果是单纯的 ] ，检查后面是否有其他内容
            if end_pattern == ']':
                # 看看 ] 后面是否还有其他非空白字符
                after_bracket = content_stripped[end_pos+1:].strip()
                if after_bracket and not after_bracket.startswith('//') and not after_bracket.startswith('/*'):
                    continue  # 继续寻找
            print(f"  Found end at {end_pos} using pattern '{end_pattern}'")
            break
    else:
        print(f"  No end found! Last chars: {content_stripped[-30:]}")
        return None
    
    # 提取数组内容（只提取 [ 后面的部分）
    array_str = content_stripped[start_pos:end_pos+1]
    
    # 打印前100个字符用于调试
    print(f"  Array start: {array_str[:100]}")
    
    try:
        # 转换JS对象语法为Python可解析的格式
        # 1. 给没有引号的键添加引号
        array_str = re.sub(r'(\w+):', r'"\1":', array_str)
        # 2. 移除注释
        array_str = re.sub(r'//.*?$', '', array_str, flags=re.MULTILINE)
        # 使用 eval 来解析JS数组
        data = eval(array_str)
        return data
    except Exception as e:
        print(f"  Error: {e}")
        # 打印更多上下文
        print(f"  Array sample: {array_str[:300]}")
        return None

# 测试一个文件
data = extract_data('hexagramImagesDataPNG.js')
if data:
    print(f"Success! Got {len(data)} items")
    print(f"First item: {data[0]}")
