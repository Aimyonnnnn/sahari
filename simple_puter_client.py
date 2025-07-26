import requests
import json
import time
from typing import Optional, Dict, Any

class SimplePuterClient:
    """Flask 서버에 연결하는 간단한 Puter AI 클라이언트"""
    
    def __init__(self, server_url: str = "http://localhost:5000"):
        """
        클라이언트 초기화
        
        Args:
            server_url: Flask 서버 URL
        """
        self.server_url = server_url
        self.session = requests.Session()
    
    def chat(self, message: str, model: str = "claude-sonnet-4", 
             system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        AI와 채팅
        
        Args:
            message: 사용자 메시지
            model: AI 모델
            system_prompt: 시스템 프롬프트
            
        Returns:
            응답 결과
        """
        try:
            payload = {
                "message": message,
                "model": model
            }
            
            if system_prompt:
                payload["system_prompt"] = system_prompt
            
            response = self.session.post(
                f"{self.server_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"서버 오류: {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"네트워크 오류: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"오류: {str(e)}"
            }
    
    def health_check(self) -> bool:
        """서버 상태 확인"""
        try:
            response = self.session.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_models(self) -> list:
        """사용 가능한 모델 목록 가져오기"""
        try:
            response = self.session.get(f"{self.server_url}/models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("models", [])
            return []
        except:
            return []

def interactive_chat():
    """대화형 채팅"""
    client = SimplePuterClient()
    
    # 서버 상태 확인
    if not client.health_check():
        print("❌ 서버에 연결할 수 없습니다.")
        print("Flask 서버가 실행 중인지 확인해주세요:")
        print("python puter_flask_server.py")
        return
    
    print("✅ 서버에 연결되었습니다!")
    
    # 사용 가능한 모델 표시
    models = client.get_models()
    if models:
        print(f"📋 사용 가능한 모델: {', '.join(models)}")
    
    # 시스템 프롬프트 설정
    system_prompt = input("시스템 프롬프트를 입력하세요 (기본값 사용하려면 Enter): ").strip()
    if not system_prompt:
        system_prompt = "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요."
    
    print(f"\n🤖 시스템 프롬프트: {system_prompt}")
    print("채팅을 시작합니다! 종료하려면 'quit' 또는 'exit'를 입력하세요.\n")
    
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
        response = client.chat(
            message=user_input,
            model="claude-sonnet-4",
            system_prompt=system_prompt
        )
        
        if response.get("success"):
            ai_message = response.get("response", "응답을 받지 못했습니다.")
            print(f"🤖 AI: {ai_message}\n")
        else:
            print(f"❌ 오류: {response.get('error', '알 수 없는 오류')}\n")

def batch_chat(messages: list, system_prompt: str = None) -> list:
    """
    여러 메시지를 일괄 처리
    
    Args:
        messages: 메시지 목록
        system_prompt: 시스템 프롬프트
        
    Returns:
        응답 목록
    """
    client = SimplePuterClient()
    responses = []
    
    for i, message in enumerate(messages, 1):
        print(f"처리 중... ({i}/{len(messages)})")
        
        response = client.chat(
            message=message,
            model="claude-sonnet-4",
            system_prompt=system_prompt
        )
        
        responses.append({
            "message": message,
            "response": response
        })
        
        # 요청 간 간격
        time.sleep(1)
    
    return responses

def save_conversation(responses: list, filename: str = "conversation.json"):
    """대화 내용을 파일로 저장"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)
    print(f"대화 내용이 {filename}에 저장되었습니다.")

# 사용 예시
if __name__ == "__main__":
    print("🤖 Puter AI 파이썬 클라이언트")
    print("=" * 50)
    
    # 대화형 채팅
    interactive_chat()
    
    # 일괄 처리 예시 (주석 처리)
    """
    messages = [
        "안녕하세요!",
        "파이썬에 대해 설명해주세요.",
        "감사합니다!"
    ]
    
    system_prompt = "당신은 친절한 프로그래밍 튜터입니다."
    responses = batch_chat(messages, system_prompt)
    save_conversation(responses)
    """ 