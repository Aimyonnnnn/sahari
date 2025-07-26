import requests
import json
import time
from typing import Optional, Dict, Any

class PuterAIClient:
    """Puter AI API를 사용하는 파이썬 클라이언트"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Puter AI 클라이언트 초기화
        
        Args:
            api_key: Puter API 키 (선택사항)
        """
        self.api_key = api_key
        self.base_url = "https://api.puter.com"  # 실제 API 엔드포인트
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })
    
    def chat(self, message: str, model: str = "claude-sonnet-4", 
             system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        AI와 채팅
        
        Args:
            message: 사용자 메시지
            model: 사용할 AI 모델
            system_prompt: 시스템 프롬프트
            
        Returns:
            AI 응답
        """
        try:
            payload = {
                "message": message,
                "model": model
            }
            
            if system_prompt:
                payload["system_prompt"] = system_prompt
            
            # 실제 API 호출 (예시)
            response = self.session.post(
                f"{self.base_url}/ai/chat",
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API 오류: {response.status_code} - {response.text}")
                
        except Exception as e:
            return {"error": str(e)}

# 사용 예시
def main():
    # 클라이언트 초기화
    client = PuterAIClient()
    
    # 시스템 프롬프트 설정
    system_prompt = "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요."
    
    print("🤖 Puter AI 채팅을 시작합니다!")
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
        response = client.chat(
            message=user_input,
            model="claude-sonnet-4",
            system_prompt=system_prompt
        )
        
        if "error" in response:
            print(f"❌ 오류: {response['error']}")
        else:
            # 응답 출력
            ai_message = response.get("message", {}).get("content", [{}])[0].get("text", "응답을 받지 못했습니다.")
            print(f"🤖 AI: {ai_message}\n")

if __name__ == "__main__":
    main() 