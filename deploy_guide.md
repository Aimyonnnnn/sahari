# 🚀 Puter AI API 서버 배포 가이드

## 📋 배포 전 준비사항

1. **Git 설치**
2. **Heroku CLI 설치** (https://devcenter.heroku.com/articles/heroku-cli)
3. **GitHub 계정**

## 🎯 Heroku 배포 (가장 간단)

### 1. Heroku 계정 생성 및 로그인
```bash
# Heroku CLI 설치 후
heroku login
```

### 2. Git 저장소 초기화
```bash
git init
git add .
git commit -m "Initial commit"
```

### 3. Heroku 앱 생성
```bash
heroku create your-puter-ai-app
```

### 4. 배포
```bash
git push heroku main
```

### 5. 앱 실행 확인
```bash
heroku open
```

## 🌐 Vercel 배포 (무료, 빠름)

### 1. Vercel 계정 생성
- https://vercel.com 에서 GitHub 계정으로 로그인

### 2. 프로젝트 연결
- GitHub 저장소를 Vercel에 연결
- 자동으로 배포됨

### 3. 도메인 확인
- `https://your-app-name.vercel.app` 형태로 접근 가능

## 🚂 Railway 배포

### 1. Railway 계정 생성
- https://railway.app 에서 GitHub 계정으로 로그인

### 2. 프로젝트 생성
- "Deploy from GitHub repo" 선택
- 저장소 연결

### 3. 환경 변수 설정 (필요시)
- Railway 대시보드에서 환경 변수 추가

## 📡 배포 후 사용법

### API 엔드포인트
```
POST https://your-app-name.herokuapp.com/chat
GET  https://your-app-name.herokuapp.com/health
GET  https://your-app-name.herokuapp.com/models
```

### Python에서 사용
```python
import requests

url = "https://your-app-name.herokuapp.com/chat"
data = {
    "message": "안녕하세요!",
    "model": "claude-sonnet-4",
    "system_prompt": "친절하게 답변해주세요."
}

response = requests.post(url, json=data)
result = response.json()
print(result["response"])
```

### JavaScript에서 사용
```javascript
fetch('https://your-app-name.herokuapp.com/chat', {
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

### cURL에서 사용
```bash
curl -X POST https://your-app-name.herokuapp.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "안녕하세요!",
    "model": "claude-sonnet-4",
    "system_prompt": "친절하게 답변해주세요."
  }'
```

## 🔧 환경 변수 설정

### Heroku
```bash
heroku config:set PUTER_API_KEY=your_api_key
```

### Vercel
- Vercel 대시보드 → Settings → Environment Variables

### Railway
- Railway 대시보드 → Variables 탭

## 📊 모니터링

### 로그 확인 (Heroku)
```bash
heroku logs --tail
```

### 앱 상태 확인
```bash
curl https://your-app-name.herokuapp.com/health
```

## 🛠️ 문제 해결

### 1. 배포 실패
- `requirements.txt` 파일이 있는지 확인
- `Procfile` 파일이 있는지 확인
- Python 버전이 `runtime.txt`와 일치하는지 확인

### 2. API 오류
- Puter API 키가 올바르게 설정되었는지 확인
- 네트워크 연결 상태 확인

### 3. 메모리 부족
- Heroku 무료 플랜의 경우 30분 후 슬립 모드
- 유료 플랜으로 업그레이드 고려

## 💡 팁

1. **도메인 커스터마이징**: Heroku에서 커스텀 도메인 설정 가능
2. **자동 배포**: GitHub에 푸시하면 자동으로 배포됨
3. **스케일링**: 트래픽에 따라 자동 스케일링
4. **백업**: 정기적으로 코드 백업 권장

## 🔒 보안 고려사항

1. **API 키 보호**: 환경 변수로 API 키 관리
2. **Rate Limiting**: 요청 제한 설정 고려
3. **CORS 설정**: 필요한 경우 CORS 헤더 추가
4. **HTTPS**: 모든 통신은 HTTPS로 암호화됨 