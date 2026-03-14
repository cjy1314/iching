const fs = require('fs');

// 读取并解析JS文件中的数据
function extractData(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    // 提取 exports.xxx = [...] 或 module.exports = [...]
    const match = content.match(/exports\.\w+\s*=\s*(\[[\s\S]*?\]);?$/m) || 
                  content.match(/module\.exports\s*=\s*(\[[\s\S]*?\]);?$/m);
    if (match) {
        try {
            const data = eval('(' + match[1] + ')');
            return data;
        } catch(e) {
            console.log('Error parsing', filePath, e.message);
            return null;
        }
    }
    return null;
}

const files = [
    ['hexagramImagesDataPNG.js', 'hexagramImagesData'],
    ['hexagramTextData.js', 'hexagramTextData'],
    ['yaoText.js', 'yaoTextData'],
    ['hexagramTranslationData.js', 'hexagramTranslationData'],
    ['yaoTranslation.js', 'yaoTranslationData'],
    ['hexagramExplainSYData.js', 'hexagramExplainSYData'],
    ['hexagramExplainFPRshiyunData.js', 'hexagramExplainFPRshiyunData'],
    ['hexagramExplainFPRcaiyunData.js', 'hexagramExplainFPRcaiyunData'],
    ['hexagramExplainFPRjiazhaiData.js', 'hexagramExplainFPRjiazhaiData'],
    ['hexagramExplainFPRshentiData.js', 'hexagramExplainFPRshentiData'],
];

let result = '// 易经数据 - 浏览器兼容版本\n\n';
files.forEach(([file, varName]) => {
    const data = extractData(file);
    if (data) {
        result += 'var ' + varName + ' = ' + JSON.stringify(data) + ';\n\n';
        console.log('Extracted:', varName, 'with', data.length, 'items');
    }
});

fs.writeFileSync('iching-data.js', result);
console.log('Done! File created.');
