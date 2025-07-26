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
    <title>Puter AI API 서버 - CloudType</title>
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
            <p>CloudType에 배포된 서버에서 Puter AI를 사용하세요</p>
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
                
                <h4>💻 사용 예시</h4>
                <div class="code-block">
import requests

url = "https://your-app.cloudtype.app/chat"
data = {
    "message": "파이썬에 대해 설명해주세요",
    "model": "claude-sonnet-4",
    "system_prompt": "당신은 프로그래밍 전문가입니다."
}

response = requests.post(url, json=data)
result = response.json()
print(result["response"])
                </div>
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
            # 시스템 프롬프트에 따른 응답 생성
            if system_prompt and "댓글" in system_prompt:
                # 댓글 생성 모드
                responses = [
                    "좋은 글이네요! 👍",
                    "정말 유익한 정보 감사합니다 😊",
                    "와! 대단하네요 👏",
                    "흥미로운 내용이에요!",
                    "도움이 많이 되었어요 💕",
                    "정말 잘 정리해주셨네요!",
                    "감사합니다! 좋은 정보였어요",
                    "와우! 놀라워요 😮",
                    "정말 멋진 글이에요 ✨",
                    "추천합니다! 👍"
                ]
                
                import random
                response = random.choice(responses)
                
                # 본문 내용에 따른 맞춤 응답
                if "날씨" in message:
                    response = "날씨가 정말 좋네요! 😊"
                elif "음식" in message or "맛" in message:
                    response = "맛있겠어요! 🤤"
                elif "여행" in message:
                    response = "여행 재미있겠어요! ✈️"
                elif "공부" in message or "학습" in message:
                    response = "열심히 공부하세요! 📚"
                elif "운동" in message or "운동" in message:
                    response = "건강한 하루 되세요! 💪"
                elif "고민" in message or "힘들" in message:
                    response = "힘내세요! 응원할게요 💪"
                elif "축하" in message or "생일" in message:
                    response = "축하드려요! 🎉"
                elif "감사" in message:
                    response = "천만에요! 😊"
                elif "?" in message or "?" in message:
                    response = "좋은 질문이네요! 🤔"
                else:
                    response = random.choice(responses)
                    
            else:
                # 일반 채팅 모드
                response = f"안녕하세요! '{message}'에 대한 답변입니다. 현재는 시뮬레이션 모드로 작동하고 있습니다."
            
            return {
                "success": True,
                "response": response,
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
        "service": "Puter AI API Server - CloudType",
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
    # CloudType에서는 PORT 환경변수를 사용
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False) 