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
    patterns = [
        r'exports\.\w+\s*=\s*(\[)',
        r'module\.exports\s*=\s*(\[)',
    ]
    
    start_pos = None
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            # 找到 = 后面的 [ 位置
            start_pos = match.end() - 1
            break
    
    if start_pos is None:
        return None
    
    # 找到数组的结束位置
    content_stripped = content.rstrip()
    end_pos = -1
    for end_pattern in ['];', '];\n', ']']:
        end_pos = content_stripped.rfind(end_pattern)
        if end_pos != -1:
            if end_pattern == ']':
                after_bracket = content_stripped[end_pos+1:].strip()
                if after_bracket and not after_bracket.startswith('//') and not after_bracket.startswith('/*'):
                    continue
            break
    else:
        return None
    
    # 提取数组内容
    array_str = content_stripped[start_pos:end_pos+1]
    
    try:
        # 转换JS对象语法为Python可解析的格式
        array_str = re.sub(r'(\w+):', r'"\1":', array_str)
        array_str = re.sub(r'//.*?$', '', array_str, flags=re.MULTILINE)
        data = eval(array_str)
        return data
    except Exception as e:
        print(f'Error parsing {file_path}: {e}')
        return None

files = [
    ('hexagramImagesDataPNG.js', 'hexagramImagesData'),
    ('hexagramTextData.js', 'hexagramTextData'),
    ('yaoText.js', 'yaoTextData'),
    ('hexagramTranslationData.js', 'hexagramTranslationData'),
    ('yaoTranslation.js', 'yaoTranslationData'),
    ('hexagramExplainSYData.js', 'hexagramExplainSYData'),
    ('hexagramExplainFPRshiyunData.js', 'hexagramExplainFPRshiyunData'),
    ('hexagramExplainFPRcaiyunData.js', 'hexagramExplainFPRcaiyunData'),
    ('hexagramExplainFPRjiazhaiData.js', 'hexagramExplainFPRjiazhaiData'),
    ('hexagramExplainFPRshentiData.js', 'hexagramExplainFPRshentiData'),
    # 新增爻辞解读数据
    ('yaoExplainSY.js', 'yaoExplainSYData'),
    ('yaoExplainFPRshiyun.js', 'yaoExplainFPRshiyunData'),
    ('yaoExplainFPRcaiyun.js', 'yaoExplainFPRcaiyunData'),
    ('yaoExplainFPRjiazhai.js', 'yaoExplainFPRjiazhaiData'),
    ('yaoExplainFPRshenti.js', 'yaoExplainFPRshentiData'),
]

result = '// 易经数据 - 浏览器兼容版本\n\n'

for file_name, var_name in files:
    print(f'Processing {file_name}...')
    data = extract_data(file_name)
    if data:
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        result += f'var {var_name} = {json_str};\n\n'
        print(f'  Extracted: {var_name} with {len(data)} items')
    else:
        print(f'  Failed to extract: {file_name}')

# 写入文件
with open('iching-data.js', 'w', encoding='utf-8') as f:
    f.write(result)

print('Done! File created.')
