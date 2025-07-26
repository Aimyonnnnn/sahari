import sys
import requests
import json
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineProfile
from PyQt5.QtCore import QUrl
from PIL import Image
import base64
import io
import os

class PuterWebPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_result = None
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS Console: {message}")
        if "AI 응답:" in message:
            self.chat_result = message.replace("AI 응답:", "").strip()

class PuterWorker(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, message, image_path=None):
        super().__init__()
        self.message = message
        self.image_path = image_path
        self.web_view = None

    def run(self):
        try:
            # 임시 HTML 파일 생성
            html_content = self.create_html_content()
            temp_file = "temp_chat.html"
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 웹뷰 생성 및 실행
            self.web_view = QWebEngineView()
            self.web_page = PuterWebPage()
            self.web_view.setPage(self.web_page)
            
            # 로컬 서버 URL로 접근
            self.web_view.load(QUrl("http://localhost:8000/temp_chat.html"))
            
            # 응답 대기
            timeout = 30
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if self.web_page.chat_result:
                    self.result.emit(self.web_page.chat_result)
                    break
                time.sleep(0.5)
            else:
                self.error.emit("응답 시간 초과")
                
            # 임시 파일 삭제
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e:
            self.error.emit(f"오류: {str(e)}")

    def create_html_content(self):
        # 이미지 처리
        image_script = ""
        if self.image_path:
            with open(self.image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                image_script = f"""
                const img = document.createElement('img');
                img.src = 'data:image/jpeg;base64,{img_data}';
                document.body.appendChild(img);
                """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Puter AI Chat</title>
        </head>
        <body>
            <div id="result"></div>
            {image_script}
            <script src="https://js.puter.com/v2/"></script>
            <script>
                (async () => {{
                    try {{
                        const response = await puter.ai.chat(
                            "{self.message.replace('"', '\\"')}", 
                            {{
                                model: 'claude-sonnet-4'
                            }}
                        );
                        
                        const result = response.message.content[0].text;
                        console.log('AI 응답: ' + result);
                        document.getElementById('result').innerHTML = result;
                        
                    }} catch (error) {{
                        console.error('오류:', error);
                        document.getElementById('result').innerHTML = '오류: ' + error.message;
                    }}
                }})();
            </script>
        </body>
        </html>
        """

class ChatBot(QWidget):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.image_path = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Puter AI 챗봇 (웹 기반)')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # 채팅 히스토리 표시 영역
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(QLabel('대화 내용:'))
        layout.addWidget(self.chat_display)
        
        # 이미지 첨부 영역
        image_layout = QHBoxLayout()
        self.image_label = QLabel('이미지 없음')
        self.image_label.setFixedSize(100, 100)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        
        self.attach_btn = QPushButton('이미지 첨부')
        self.attach_btn.clicked.connect(self.attach_image)
        
        self.clear_image_btn = QPushButton('이미지 제거')
        self.clear_image_btn.clicked.connect(self.clear_image)
        
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.attach_btn)
        image_layout.addWidget(self.clear_image_btn)
        image_layout.addStretch()
        layout.addLayout(image_layout)
        
        # 입력 영역
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton('전송')
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        
        # 대화 초기화 버튼
        self.clear_btn = QPushButton('대화 초기화')
        self.clear_btn.clicked.connect(self.clear_chat)
        layout.addWidget(self.clear_btn)
        
        self.setLayout(layout)
        
    def attach_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '이미지 선택', '', 
            'Images (*.png *.jpg *.jpeg *.gif *.bmp)'
        )
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText('')
            
    def clear_image(self):
        self.image_path = None
        self.image_label.clear()
        self.image_label.setText('이미지 없음')
        
    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return
            
        # 사용자 메시지 추가
        self.messages.append({
            "role": "user",
            "content": message,
            "image": self.image_path
        })
        
        # 채팅 표시 업데이트
        self.update_chat_display()
        
        # 입력 필드 초기화
        self.input_field.clear()
        
        # API 호출
        self.worker = PuterWorker(message, self.image_path)
        self.worker.result.connect(self.handle_response)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
        
        # 전송 버튼 비활성화
        self.send_btn.setEnabled(False)
        self.send_btn.setText('응답 대기 중...')
        
    def handle_response(self, response_text):
        # AI 응답 추가
        self.messages.append({
            "role": "assistant",
            "content": response_text
        })
        
        self.update_chat_display()
        
        # 전송 버튼 재활성화
        self.send_btn.setEnabled(True)
        self.send_btn.setText('전송')
        
    def handle_error(self, error_msg):
        self.chat_display.append(f"❌ 오류: {error_msg}")
        self.send_btn.setEnabled(True)
        self.send_btn.setText('전송')
        
    def update_chat_display(self):
        self.chat_display.clear()
        for msg in self.messages:
            if msg['role'] == 'user':
                self.chat_display.append(f"👤 사용자: {msg['content']}")
                if msg.get('image'):
                    self.chat_display.append("   [이미지 첨부됨]")
            else:
                self.chat_display.append(f"🤖 AI: {msg['content']}")
            self.chat_display.append("")
            
    def clear_chat(self):
        self.messages = []
        self.chat_display.clear()
        self.clear_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatbot = ChatBot()
    chatbot.show()
    sys.exit(app.exec_())