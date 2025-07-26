import sys
import requests
import json
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
import base64
import io
import os

class CommentWorker(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, post_content):
        super().__init__()
        self.post_content = post_content

    def run(self):
        try:
            # 임시 HTML 파일 생성
            html_content = self.create_html_content()
            temp_file = "temp_comment.html"
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 웹뷰 생성 및 실행
            self.web_view = QWebEngineView()
            self.web_page = CommentWebPage()
            self.web_view.setPage(self.web_page)
            
            # 로컬 서버 URL로 접근
            self.web_view.load(QUrl("http://localhost:8000/temp_comment.html"))
            
            # 응답 대기
            timeout = 30
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if self.web_page.comment_result:
                    self.result.emit(self.web_page.comment_result)
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
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>댓글 생성기</title>
        </head>
        <body>
            <div id="result"></div>
            <script src="https://js.puter.com/v2/"></script>
            <script>
                (async () => {{
                    try {{
                        const prompt = `넌 이제부터 댓글싸게야 내가 본문 복사 붙이기 하면 넌 바로 복사 붙이기 할 수 있게 댓글 적어줘 알겠지? 본문내용: "{self.post_content.replace('"', '\\"')}"`;
                        
                        const response = await puter.ai.chat(prompt, {{
                            model: 'claude-sonnet-4'
                        }});
                        
                        const result = response.message.content[0].text;
                        console.log('댓글 결과: ' + result);
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

class CommentWebPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.comment_result = None
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS Console: {message}")
        if "댓글 결과:" in message:
            self.comment_result = message.replace("댓글 결과:", "").strip()

class CommentGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('댓글 생성기')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # 제목
        title_label = QLabel('💬 댓글 생성기')
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 설명
        desc_label = QLabel('본문을 입력하면 AI가 적절한 댓글을 생성해드립니다!')
        desc_label.setStyleSheet("color: #666; margin: 5px;")
        layout.addWidget(desc_label)
        
        # 본문 입력 영역
        layout.addWidget(QLabel('📝 본문 내용:'))
        self.post_input = QTextEdit()
        self.post_input.setPlaceholderText("본문을 여기에 복사붙여넣기 하세요...")
        self.post_input.setMaximumHeight(150)
        layout.addWidget(self.post_input)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton('🤖 댓글 생성')
        self.generate_btn.clicked.connect(self.generate_comment)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                transform: translateY(-2px);
            }
            QPushButton:disabled {
                opacity: 0.6;
            }
        """)
        
        self.clear_btn = QPushButton('🗑️ 지우기')
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: #dc3545;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #c82333;
            }
        """)
        
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        
        # 결과 표시 영역
        layout.addWidget(QLabel('💭 생성된 댓글:'))
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("""
            QTextEdit {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.result_display)
        
        # 복사 버튼
        self.copy_btn = QPushButton('📋 클립보드에 복사')
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #218838;
            }
        """)
        layout.addWidget(self.copy_btn)
        
        self.setLayout(layout)
        
    def generate_comment(self):
        post_content = self.post_input.toPlainText().strip()
        
        if not post_content:
            self.result_display.setText("❌ 본문을 입력해주세요!")
            return
        
        # 로딩 상태 시작
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText('🔄 댓글 생성 중...')
        
        # 워커 시작
        self.worker = CommentWorker(post_content)
        self.worker.result.connect(self.handle_result)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
        
    def handle_result(self, comment):
        self.result_display.setText(comment)
        
        # 버튼 상태 복원
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText('🤖 댓글 생성')
        
    def handle_error(self, error_msg):
        self.result_display.setText(f"❌ 오류: {error_msg}")
        
        # 버튼 상태 복원
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText('🤖 댓글 생성')
        
    def copy_to_clipboard(self):
        comment = self.result_display.toPlainText()
        if comment and not comment.startswith("❌"):
            clipboard = QApplication.clipboard()
            clipboard.setText(comment)
            self.result_display.append("\n\n✅ 클립보드에 복사되었습니다!")
        
    def clear_all(self):
        self.post_input.clear()
        self.result_display.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 스타일 설정
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
    """)
    
    generator = CommentGenerator()
    generator.show()
    sys.exit(app.exec_())