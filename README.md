# Puter AI 챗봇

PyQt5 기반의 Puter AI 챗봇 프로그램입니다.

## 버전 정보
- `app.py`: 초기 버전 (API 호출 오류)
- `app_v2.py`: 개선된 버전
- `app_v3.py`: 최신 버전 (디버깅 정보 포함)
- `app_final.py`: Socket.IO 기반 버전
- `app_web_based.py`: **웹 기반 버전 (권장)**

## 기능
- 텍스트 질문/답변
- 이미지 첨부 가능 (이미지 인식 및 분석)
- 대화 히스토리 유지
- 직관적인 GUI 인터페이스

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 웹 서버 실행 (필수)
```bash
python -m http.server 8000
```

### 3. 프로그램 실행
```bash
# 웹 기반 버전 실행 (권장)
python app_web_based.py

# 또는 다른 버전
python app_final.py
python app_v3.py
```

## 사용법
1. **웹 서버 실행**: `python -m http.server 8000`
2. **프로그램 실행**: `python app_web_based.py`
3. **텍스트 질문**: 하단 입력창에 질문을 입력하고 '전송' 버튼 클릭
4. **이미지 첨부**: '이미지 첨부' 버튼을 클릭하여 이미지 파일 선택
5. **대화 초기화**: '대화 초기화' 버튼으로 새로운 대화 시작

## 주요 특징
- Puter AI API 사용 (인증 불필요)
- Claude Sonnet 4 모델 사용
- 멀티모달 지원 (텍스트 + 이미지)
- 비동기 응답 처리
- 웹 브라우저 기반 API 호출

## 문제 해결
- **403 Forbidden 오류**: 웹 서버가 실행되지 않았거나 잘못된 API 엔드포인트
- **네트워크 오류**: 인터넷 연결 확인
- **이미지 업로드 실패**: 이미지 형식 및 크기 확인
- **PyQtWebEngine 오류**: `pip install PyQtWebEngine` 재설치

## 기술적 설명
Puter API는 브라우저 환경에서만 작동하므로, Python에서는 웹뷰를 통해 Puter JavaScript SDK를 호출하는 방식으로 구현했습니다.