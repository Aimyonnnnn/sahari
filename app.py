from flask import Flask, request, jsonify, render_template_string
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puter AI API 서버</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        
        .content {
            padding: 20px;
        }
        
        .api-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .api-section h3 {
            color: #667eea;
            margin-top: 0;
        }
        
        .code-block {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            overflow-x: auto;
            margin: 10px 0;
        }
        
        .endpoint {
            background: #e3f2fd;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 10px 0;
        }
        
        .endpoint h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        
        .method {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Puter AI API 서버</h1>
            <p>배포된 서버에서 Puter AI를 사용하세요</p>
        </div>
        
        <div class="content">
            <div class="api-section">
                <h3>📡 API 엔드포인트</h3>
                
                <div class="endpoint">
                    <h4><span class="method">POST</span> /chat - AI 채팅</h4>
                    <p>AI와 대화할 수 있는 메인 엔드포인트입니다.</p>
                    <div class="code-block">
{
  "message": "안녕하세요!",
  "model": "claude-sonnet-4",
  "system_prompt": "당신은 도움이 되는 AI 어시스턴트입니다."
}
                    </div>
                </div>
                
                <div class="endpoint">
                    <h4><span class="method">GET</span> /health - 서버 상태</h4>
                    <p>서버가 정상적으로 작동하는지 확인합니다.</p>
                </div>
                
                <div class="endpoint">
                    <h4><span class="method">GET</span> /models - 모델 목록</h4>
                    <p>사용 가능한 AI 모델 목록을 가져옵니다.</p>
                </div>
            </div>
            
            <div class="api-section">
                <h3>💻 사용 예시</h3>
                
                <h4>Python에서 사용:</h4>
                <div class="code-block">
import requests

url = "https://your-app-name.herokuapp.com/chat"
data = {
    "message": "파이썬에 대해 설명해주세요",
    "model": "claude-sonnet-4",
    "system_prompt": "당신은 프로그래밍 전문가입니다."
}

response = requests.post(url, json=data)
result = response.json()
print(result["response"])
                </div>
                
                <h4>JavaScript에서 사용:</h4>
                <div class="code-block">
fetch('https://your-app-name.herokuapp.com/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: '안녕하세요!',
        model: 'claude-sonnet-4',
        system_prompt: '친절하게 답변해주세요.'
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
                </div>
                
                <h4>cURL에서 사용:</h4>
                <div class="code-block">
curl -X POST https://your-app-name.herokuapp.com/chat \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "안녕하세요!",
    "model": "claude-sonnet-4",
    "system_prompt": "친절하게 답변해주세요."
  }'
                </div>
            </div>
            
            <div class="api-section">
                <h3>🔧 응답 형식</h3>
                <div class="code-block">
{
  "success": true,
  "response": "AI 응답 내용",
  "model": "claude-sonnet-4",
  "timestamp": "2024-01-01T12:00:00"
}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

class PuterAIServer:
    """Puter AI 서버 클래스"""
    
    def __init__(self):
        self.base_url = "https://api.puter.com"  # 실제 API 엔드포인트
    
    def chat(self, message: str, model: str = "claude-sonnet-4", 
             system_prompt: str = None) -> dict:
        """
        AI 채팅 요청
        
        Args:
            message: 사용자 메시지
            model: AI 모델
            system_prompt: 시스템 프롬프트
            
        Returns:
            응답 결과
        """
        try:
            # 실제 Puter API 호출 (예시)
            # 실제 구현에서는 Puter의 공식 API를 사용해야 합니다
            payload = {
                "message": message,
                "model": model
            }
            
            if system_prompt:
                payload["system_prompt"] = system_prompt
            
            # 여기서는 시뮬레이션 응답을 반환
            # 실제로는 requests.post()를 사용하여 API 호출
            return {
                "success": True,
                "response": f"시뮬레이션 응답: {message}에 대한 AI 답변입니다.",
                "model": model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# 서버 인스턴스 생성
puter_server = PuterAIServer()

@app.route('/')
def index():
    """메인 페이지"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """AI 채팅 API 엔드포인트"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "메시지가 필요합니다."
            }), 400
        
        message = data['message']
        model = data.get('model', 'claude-sonnet-4')
        system_prompt = data.get('system_prompt')
        
        # AI 응답 요청
        result = puter_server.chat(message, model, system_prompt)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health')
def health():
    """서버 상태 확인"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Puter AI API Server",
        "version": "1.0.0"
    })

@app.route('/models')
def models():
    """사용 가능한 모델 목록"""
    return jsonify({
        "models": [
            "claude-sonnet-4",
            "claude-3-5-sonnet", 
            "claude-3-opus",
            "gpt-4",
            "gpt-3.5-turbo"
        ]
    })

if __name__ == '__main__':
    # Heroku에서는 PORT 환경변수를 사용
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)