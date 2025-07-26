import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PIL import Image
import base64
import io
import json
import time

# Puter AI API - 실제 엔드포인트 사용
class PuterWorker(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, message, image_path=None):
        super().__init__()
        self.message = message
        self.image_path = image_path

    def run(self):
        try:
            # Puter의 실제 API 엔드포인트
            api_url = "https://api.puter.com/v1/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json"
            }
            
            # 메시지 구성
            content = [{"type": "text", "text": self.message}]
            
            # 이미지가 있는 경우 추가
            if self.image_path:
                with open(self.image_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_data}"
                        }
                    })
            
            messages = [{"role": "user", "content": content}]
            
            data = {
                "model": "claude-sonnet-4",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            print(f"API 요청 데이터: {json.dumps(data, indent=2)}")
            
            response = requests.post(api_url, headers=headers, json=data, timeout=60)
            
            print(f"API 응답 상태: {response.status_code}")
            print(f"API 응답 헤더: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API 응답: {json.dumps(result, indent=2)}")
                
                if 'choices' in result and len(result['choices']) > 0:
                    assistant_message = result['choices'][0]['message']['content']
                    self.result.emit(assistant_message)
                else:
                    self.error.emit("응답 형식이 올바르지 않습니다.")
            else:
                error_text = response.text
                self.error.emit(f"API 호출 실패: {response.status_code} - {error_text}")
                
        except requests.exceptions.RequestException as e:
            self.error.emit(f"네트워크 오류: {str(e)}")
        except Exception as e:
            self.error.emit(f"오류: {str(e)}")

class ChatBot(QWidget):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.image_path = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Puter AI 챗봇 v3')
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