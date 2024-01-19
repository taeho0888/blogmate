# Blogmate
- 유튜브 요약노트 생성 서비스
- 챗 GPT 활용

## 기능
### 1. 메인 화면
<img width="1680" alt="image" src="https://github.com/taeho0888/blogmate/assets/105200642/24ebfd68-c258-423b-b0a4-41e683a7c967">

### 2. 유튜브 링크로 동영상 등록
<img width="1680" alt="image" src="https://github.com/taeho0888/blogmate/assets/105200642/f14709cf-981d-4783-ba7d-cd64b77a7d67">


### 3. 자막 추출
<img width="1680" alt="image" src="https://github.com/taeho0888/blogmate/assets/105200642/94ee1b7f-bec3-4c73-b7f9-0a266a5028ed">
<img width="1680" alt="image" src="https://github.com/taeho0888/blogmate/assets/105200642/e797c176-b043-46a6-8cd4-831ae1bdb24d">


### 4. GPT 요약 추출
<img width="1678" alt="image" src="https://github.com/taeho0888/blogmate/assets/105200642/1adea20a-134a-4eff-8b2b-014449f8a76d">
<img width="1680" alt="image" src="https://github.com/taeho0888/blogmate/assets/105200642/306d28f9-bf7b-4eb6-a686-090db6d9f43f">


## 세팅

### 1. 클론 & 가상환경 생성
#### Windows
```
git clone https://github.com/taeho0888/blogmate.git .
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
#### macOS
```
git clone https://github.com/taeho0888/blogmate.git .
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
### 2. `.env` 생성
루트 디렉토리에 `.env` 파일 생성 후 아래 내용 복사 붙여넣기
```
YOUTUBE_API_KEY = "Youtube Data API v3 api key"
OPENAI_API_KEY = "OpenAI api key"
```

### 3. 실행
```
uvicorn app.main:app --reload
```

### 4. 접속
```
http://127.0.0.1:8000
```

## TODO
- [ ] 복사 버튼 고치기
- [ ] GPT 프롬프트 제한 해결
- [ ] 비동기 처리
- [ ] 테스트 코드 작성
- [ ] base.html 헤더, 푸터 꾸미기
