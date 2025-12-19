# 🦜 Tongue-Twist (앵무새 게임)

AI 기반 한국어 발음 연습 앱 - AI-powered Korean Pronunciation Practice App

## 📖 소개 (Introduction)

Tongue-Twist는 OpenAI의 최신 AI 기술을 활용하여 한국어 발음 연습을 도와주는 인터랙티브 웹 애플리케이션입니다. 사용자는 어려운 한국어 문장(혀 꼬이는 말)을 듣고 따라 말하면, AI가 발음의 정확도를 평가하고 피드백을 제공합니다.

Tongue-Twist is an interactive web application that helps users practice Korean pronunciation using OpenAI's latest AI technology. Users listen to difficult Korean sentences (tongue twisters), repeat them, and receive AI-powered pronunciation feedback.

## ✨ 주요 기능 (Key Features)

- 🎤 **음성 인식**: OpenAI Whisper를 사용한 정확한 한국어 음성-텍스트 변환
- 🤖 **AI 발음 평가**: GPT-4o-mini를 활용한 실시간 발음 정확도 평가 및 피드백
- 🎨 **인터랙티브 UI**: Streamlit 기반의 직관적이고 사용하기 쉬운 인터페이스
- 📝 **다양한 연습 문장**: 한국어 학습자를 위한 다양한 난이도의 혀 꼬이는 말 제공
- 💬 **실시간 채팅**: 음성 녹음 및 즉각적인 피드백 제공

## 🛠️ 기술 스택 (Tech Stack)

- **Language**: Python 3.8+
- **Web Framework**: Streamlit
- **AI/ML**: 
  - OpenAI Whisper (음성 인식)
  - GPT-4o-mini (발음 평가)
  - OpenAI TTS (음성 합성)
- **Libraries**:
  - streamlit-audiorecorder (음성 녹음)
  - streamlit-chat (채팅 UI)
  - python-dotenv (환경 변수 관리)

## 📦 설치 방법 (Installation)

### 1. 저장소 클론 (Clone Repository)

```bash
git clone https://github.com/devunis/tongue-twist.git
cd tongue-twist
```

### 2. 패키지 설치 (Install Dependencies)

```bash
pip install -r requirements.txt
```

### 3. 환경 설정 (Environment Setup)

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일을 열고 당신의 OpenAI API 키를 입력하세요:

```
OPENAI_API_KEY=your_openai_api_key_here
```

OpenAI API 키는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

## 🚀 실행 방법 (How to Run)

```bash
streamlit run app.py
```

브라우저가 자동으로 열리지 않으면, 터미널에 표시된 URL(보통 `http://localhost:8501`)로 접속하세요.

## 💡 사용 방법 (How to Use)

1. **게임 시작**: 앱이 실행되면 AI가 첫 번째 혀 꼬이는 말을 제시합니다.

2. **음성 녹음**: 
   - 사이드바의 "녹음 시작" 버튼을 클릭하여 녹음을 시작하세요
   - 제시된 문장을 또박또박 발음하세요
   - "녹음 종료" 버튼을 클릭하여 녹음을 마칩니다

3. **피드백 확인**: 
   - AI가 당신의 발음을 분석하고 평가합니다
   - 정확하게 발음했다면 다음 문장으로 넘어갑니다
   - 발음이 정확하지 않다면 다시 시도하라는 피드백을 받습니다

4. **다음 문장**: "다음 문장" 버튼을 클릭하여 새로운 문장으로 건너뛸 수 있습니다

## 📝 프로젝트 구조 (Project Structure)

```
tongue-twist/
├── app.py              # 메인 Streamlit 애플리케이션
├── openai_api.py       # OpenAI API 통합 모듈
├── requirements.txt    # Python 의존성 패키지
├── .env.example        # 환경 변수 템플릿
├── .gitignore         # Git 무시 파일 목록
├── LICENSE            # MIT 라이선스
└── README.md          # 프로젝트 문서 (이 파일)
```

## 🤝 기여하기 (Contributing)

기여는 언제나 환영합니다! 버그 리포트, 기능 제안, 풀 리퀘스트 등을 자유롭게 제출해주세요.

## 📄 라이선스 (License)

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👤 저자 (Author)

Jeong-Yoon Huh

## 🙏 감사의 말 (Acknowledgments)

- OpenAI의 Whisper, GPT-4o-mini, TTS 모델
- Streamlit 프레임워크
- 모든 기여자들에게 감사드립니다
