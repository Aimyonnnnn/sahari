# 🚀 CloudType 배포 가이드

## 📋 CloudType에 Flask 앱 배포하기

### 1. GitHub에 코드 업로드

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

### 2. CloudType에서 배포

1. **CloudType 계정 생성**: https://cloudtype.io
2. **새 프로젝트 생성**: "Create New Project" 클릭
3. **GitHub 연결**: GitHub 저장소 선택
4. **배포 설정**:
   - **Language**: Python
   - **Framework**: Flask
   - **Build Command**: `pip install -r requirements_cloudtype.txt`
   - **Start Command**: `python cloudtype_app.py`
   - **Port**: 8080

### 3. 배포 완료 후

배포가 완료되면 다음과 같은 URL로 접근 가능:
```
https://your-app-name.cloudtype.app
```

## 📡 API 엔드포인트

### POST /chat - AI 채팅
```bash
curl -X POST https://your-app-name.cloudtype.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "안녕하세요!",
    "model": "claude-sonnet-4",
    "system_prompt": "친절하게 답변해주세요."
  }'
```

### GET /health - 서버 상태
```bash
curl https://your-app-name.cloudtype.app/health
```

### GET /models - 모델 목록
```bash
curl https://your-app-name.cloudtype.app/models
```

## 💻 사용 예시

### Python에서 사용
```python
import requests

url = "https://your-app-name.cloudtype.app/chat"
data = {
    "message": "파이썬에 대해 설명해주세요",
    "model": "claude-sonnet-4",
    "system_prompt": "당신은 프로그래밍 전문가입니다."
}

response = requests.post(url, json=data)
result = response.json()
print(result["response"])
```

### JavaScript에서 사용
```javascript
fetch('https://your-app-name.cloudtype.app/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: '안녕하세요!',
        model: 'claude-sonnet-4',
        system_prompt: '친절하게 답변해주세요.'
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## 🔧 파일 구조

```
├── cloudtype_app.py          # 메인 Flask 앱
├── requirements_cloudtype.txt # Python 패키지 목록
├── cloudtype.json            # CloudType 설정
└── README_cloudtype.md       # 이 파일
```

## 🛠️ 문제 해결

### 1. 배포 실패
- `requirements_cloudtype.txt` 파일이 있는지 확인
- Python 버전이 호환되는지 확인
- 포트 번호가 8080인지 확인

### 2. API 오류
- 서버가 정상적으로 실행되었는지 확인
- `/health` 엔드포인트로 서버 상태 확인

### 3. 로그 확인
- CloudType 대시보드에서 로그 확인
- 실시간 로그 모니터링 가능

## 💡 팁

1. **자동 배포**: GitHub에 푸시하면 자동으로 재배포됨
2. **환경 변수**: CloudType 대시보드에서 환경 변수 설정 가능
3. **도메인 커스터마이징**: 커스텀 도메인 설정 가능
4. **SSL 인증서**: 자동으로 HTTPS 적용됨

## 🔒 보안

- 모든 통신은 HTTPS로 암호화됨
- API 키는 환경 변수로 관리 권장
- Rate limiting 설정 고려 