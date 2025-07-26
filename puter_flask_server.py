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
    <title>Puter AI Flask 서버</title>
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
        
        .chat-section {
            margin-bottom: 30px;
        }
        
        .chat-section h3 {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .input-group {
            display: flex;
            margin-bottom: 15px;
        }
        
        input, textarea, select {
            flex: 1;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        input:focus, textarea:focus, select:focus {
            border-color: #667eea;
        }
        
        button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-left: 10px;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        .output {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            min-height: 100px;
            white-space: pre-wrap;
            font-family: monospace;
        }
        
        .api-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .api-section h4 {
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
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Puter AI Flask 서버</h1>
        </div>
        
        <div class="content">
            <div class="chat-section">
                <h3>웹 인터페이스</h3>
                <div class="input-group">
                    <input type="text" id="message-input" placeholder="메시지를 입력하세요..." />
                    <select id="model-select">
                        <option value="claude-sonnet-4">Claude Sonnet 4</option>
                        <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
                        <option value="claude-3-opus">Claude 3 Opus</option>
                        <option value="gpt-4">GPT-4</option>
                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    </select>
                    <button onclick="sendMessage()">전송</button>
                </div>
                <textarea id="system-prompt" placeholder="시스템 프롬프트 (선택사항)" rows="3">당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.</textarea>
                <div id="chat-output" class="output">응답이 여기에 표시됩니다...</div>
            </div>
            
            <div class="api-section">
                <h4>📡 API 엔드포인트</h4>
                <p>파이썬에서 다음과 같이 사용할 수 있습니다:</p>
                
                <div class="code-block">
# POST 요청으로 채팅
import requests

url = "http://localhost:5000/chat"
data = {
    "message": "안녕하세요!",
    "model": "claude-sonnet-4",
    "system_prompt": "당신은 도움이 되는 AI 어시스턴트입니다."
}

response = requests.post(url, json=data)
result = response.json()
print(result["response"])
                </div>
                
                <h4>🔗 API 정보</h4>
                <ul>
                    <li><strong>POST /chat</strong> - AI 채팅</li>
                    <li><strong>GET /health</strong> - 서버 상태 확인</li>
                    <li><strong>GET /models</strong> - 사용 가능한 모델 목록</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const messageInput = document.getElementById('message-input');
            const modelSelect = document.getElementById('model-select');
            const systemPrompt = document.getElementById('system-prompt');
            const output = document.getElementById('chat-output');
            
            const message = messageInput.value.trim();
            if (!message) return;
            
            output.textContent = '응답을 기다리는 중...';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        model: modelSelect.value,
                        system_prompt: systemPrompt.value
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    output.textContent = result.response;
                    messageInput.value = '';
                } else {
                    output.textContent = `오류: ${result.error}`;
                }
            } catch (error) {
                output.textContent = `네트워크 오류: ${error.message}`;
            }
        }
        
        // Enter 키로 메시지 전송
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
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
        "service": "Puter AI Flask Server"
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
    print("🚀 Puter AI Flask 서버를 시작합니다...")
    print("📱 웹 인터페이스: http://localhost:5000")
    print("📡 API 엔드포인트: http://localhost:5000/chat")
    print("🔍 서버 상태: http://localhost:5000/health")
    print("📋 모델 목록: http://localhost:5000/models")
    print("\n종료하려면 Ctrl+C를 누르세요.\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 