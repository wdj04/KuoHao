from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def is_valid_brackets(s: str) -> bool:
    # 创建括号匹配字典
    brackets_map = {
        ")": "(",
        "}": "{",
        "]": "["
    }
    
    # 创建栈来存储左括号
    stack = []
    
    # 遍历字符串中的每个字符
    for char in s:
        # 如果是右括号
        if char in brackets_map:
            # 如果栈为空或者栈顶元素与当前右括号不匹配，返回False
            if not stack or stack[-1] != brackets_map[char]:
                return False
            # 匹配成功，弹出栈顶元素
            stack.pop()
        # 如果是左括号，压入栈中
        elif char in brackets_map.values():
            stack.append(char)
    
    # 最后检查栈是否为空
    return len(stack) == 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_brackets():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        input_string = data.get('input', '')
        if not isinstance(input_string, str):
            return jsonify({'error': 'Input must be a string'}), 400
            
        result = is_valid_brackets(input_string)
        return jsonify({'valid': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)