// Puter AI API 분석 결과

// 1. 기본 구조
// Puter AI API는 모듈화된 구조로 되어 있으며, 다음과 같은 주요 컴포넌트들이 있습니다:

// - AdvancedBase: 기본 클래스
// - Service: 서비스 관리
// - Emitter: 이벤트 처리
// - Logger: 로깅 시스템
// - Promise: 비동기 처리

// 2. 현재 사용 중인 코드 분석
const currentCode = `
<html> 
<body> 
<script src="https://js.puter.com/v2/"></script> 
<script> 
puter.ai.chat("안녕? 테스트야야", {model: 'claude-sonnet-4'}) 
.then(response => { 
    puter.print(response.message.content[0].text); 
}); 
</script> 
</body> 
</html>
`;

// 3. Puter AI API 사용법 개선 제안

// 방법 1: 더 안전한 에러 처리
const improvedCode1 = `
<html>
<head>
    <title>Puter AI Chat</title>
</head>
<body>
    <div id="output"></div>
    <script src="https://js.puter.com/v2/"></script>
    <script>
        async function chatWithPuter() {
            try {
                const response = await puter.ai.chat("안녕? 테스트야야", {
                    model: 'claude-sonnet-4'
                });
                
                if (response && response.message && response.message.content) {
                    const text = response.message.content[0].text;
                    puter.print(text);
                    document.getElementById('output').innerHTML = text;
                } else {
                    console.error('Unexpected response format:', response);
                }
            } catch (error) {
                console.error('Chat error:', error);
                puter.print('Error: ' + error.message);
            }
        }
        
        chatWithPuter();
    </script>
</body>
</html>
`;

// 방법 2: 대화형 인터페이스
const interactiveCode = `
<html>
<head>
    <title>Puter AI Interactive Chat</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #chat-container { max-width: 600px; margin: 0 auto; }
        #messages { height: 400px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
        #input-container { display: flex; }
        #message-input { flex: 1; padding: 10px; margin-right: 10px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .message { margin-bottom: 10px; padding: 10px; border-radius: 5px; }
        .user-message { background: #e3f2fd; text-align: right; }
        .ai-message { background: #f5f5f5; }
    </style>
</head>
<body>
    <div id="chat-container">
        <h2>Puter AI Chat</h2>
        <div id="messages"></div>
        <div id="input-container">
            <input type="text" id="message-input" placeholder="메시지를 입력하세요..." />
            <button onclick="sendMessage()">전송</button>
        </div>
    </div>

    <script src="https://js.puter.com/v2/"></script>
    <script>
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('message-input');

        function addMessage(text, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = \`message \${isUser ? 'user-message' : 'ai-message'}\`;
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            messageInput.value = '';

            try {
                const response = await puter.ai.chat(message, {
                    model: 'claude-sonnet-4'
                });
                
                if (response && response.message && response.message.content) {
                    const aiResponse = response.message.content[0].text;
                    addMessage(aiResponse, false);
                    puter.print(aiResponse);
                } else {
                    addMessage('응답을 받지 못했습니다.', false);
                }
            } catch (error) {
                console.error('Chat error:', error);
                addMessage('오류가 발생했습니다: ' + error.message, false);
            }
        }

        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // 초기 메시지
        addMessage('안녕하세요! 무엇을 도와드릴까요?', false);
    </script>
</body>
</html>
`;

// 4. Puter AI API 주요 기능들

// - puter.ai.chat(): AI와 대화
// - puter.print(): 콘솔 출력
// - puter.auth: 인증 관련
// - puter.fs: 파일 시스템
// - puter.ui: 사용자 인터페이스

// 5. 모델 옵션들
const availableModels = [
    'claude-sonnet-4',
    'claude-3-5-sonnet',
    'claude-3-opus',
    'gpt-4',
    'gpt-3.5-turbo'
];

console.log('Puter AI API 분석 완료');
console.log('사용 가능한 모델:', availableModels); 