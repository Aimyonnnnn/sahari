from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import os

class PuterSeleniumClient:
    """Selenium을 사용한 Puter AI 클라이언트"""
    
    def __init__(self, headless: bool = False):
        """
        Selenium 클라이언트 초기화
        
        Args:
            headless: 헤드리스 모드 여부
        """
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """웹드라이버 설정"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Chrome 드라이버 초기화 오류: {e}")
            print("ChromeDriver가 설치되어 있는지 확인해주세요.")
            raise
    
    def create_chat_page(self):
        """채팅 페이지 생성"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Puter AI Chat</title>
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
                let lastResponse = '';

                function addMessage(text, isUser = false) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
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
                            lastResponse = aiResponse;
                            
                            // 응답을 페이지에 저장
                            document.getElementById('last-response').textContent = aiResponse;
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

                // 전역 함수로 노출
                window.sendMessageToAI = sendMessage;
                window.getLastResponse = () => lastResponse;
            </script>
            
            <!-- 응답을 저장할 숨겨진 요소 -->
            <div id="last-response" style="display: none;"></div>
        </body>
        </html>
        """
        
        # 임시 HTML 파일 생성
        with open("temp_chat.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # 브라우저에서 페이지 로드
        file_path = os.path.abspath("temp_chat.html")
        self.driver.get(f"file://{file_path}")
        
        # 페이지 로드 대기
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "message-input"))
        )
    
    def send_message(self, message: str) -> str:
        """
        메시지 전송 및 응답 받기
        
        Args:
            message: 전송할 메시지
            
        Returns:
            AI 응답
        """
        try:
            # 메시지 입력
            message_input = self.driver.find_element(By.ID, "message-input")
            message_input.clear()
            message_input.send_keys(message)
            
            # 전송 버튼 클릭
            send_button = self.driver.find_element(By.XPATH, "//button[text()='전송']")
            send_button.click()
            
            # 응답 대기 (최대 30초)
            wait = WebDriverWait(self.driver, 30)
            
            # AI 메시지가 나타날 때까지 대기
            ai_message = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "ai-message"))
            )
            
            # 마지막 AI 메시지 가져오기
            ai_messages = self.driver.find_elements(By.CLASS_NAME, "ai-message")
            if ai_messages:
                response = ai_messages[-1].text
                return response
            
            return "응답을 받지 못했습니다."
            
        except Exception as e:
            return f"오류 발생: {str(e)}"
    
    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
        
        # 임시 파일 삭제
        try:
            os.remove("temp_chat.html")
        except:
            pass

def main():
    """메인 함수"""
    client = None
    
    try:
        print("🤖 Puter AI Selenium 클라이언트를 시작합니다...")
        client = PuterSeleniumClient(headless=False)  # 브라우저 표시
        client.create_chat_page()
        
        print("채팅이 준비되었습니다!")
        print("종료하려면 'quit' 또는 'exit'를 입력하세요.\n")
        
        while True:
            # 사용자 입력
            user_input = input("👤 사용자: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("채팅을 종료합니다. 안녕히 가세요!")
                break
            
            if not user_input:
                continue
            
            print("🤖 AI가 응답을 생성하는 중...")
            
            # AI 응답 요청
            response = client.send_message(user_input)
            print(f"🤖 AI: {response}\n")
    
    except Exception as e:
        print(f"오류 발생: {e}")
    
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    main() 