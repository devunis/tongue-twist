"""
Tongue-Twist: AI 기반 한국어 발음 연습 앱
OpenAI Whisper와 GPT-4o-mini를 활용한 인터랙티브 발음 학습 애플리케이션
"""
import openai_api
import streamlit as st
from audiorecorder import audiorecorder
from streamlit_chat import message
from config import (
    APP_TITLE, 
    WELCOME_MESSAGE, 
    START_GAME_MESSAGE, 
    NEXT_SENTENCE_TEXT,
    SYSTEM_INSTRUCTION,
    RECORD_START_TEXT,
    RECORD_STOP_TEXT,
    RESET_BUTTON_TEXT,
    INPUT_AUDIO_FILE
)

def initialize_session():
    """세션 상태 초기화 함수"""
    if "chat" not in st.session_state:
        st.session_state.chat = []

def reset_game():
    """게임 초기화 함수"""
    st.session_state.chat = []
    st.rerun()

# 페이지 설정
st.title(APP_TITLE)
st.image("pngwing.com.png", use_container_width=True)

# 세션 상태 초기화
initialize_session()
answer = ""

with st.sidebar.container():
    # 음성 녹음 컴포넌트
    audio = audiorecorder(RECORD_START_TEXT, RECORD_STOP_TEXT)
    
    # 초기화 버튼 - 게임을 처음부터 다시 시작
    if st.sidebar.button(RESET_BUTTON_TEXT):
        reset_game()
    
    # 다음 문장 버튼 - 현재 문장을 건너뛰고 새로운 문장 요청
    if st.sidebar.button(NEXT_SENTENCE_TEXT):
        try:
            st.session_state.chat.append({"role": "user", "content": NEXT_SENTENCE_TEXT})
            # chat 중에서 role이 user, assistant인 것만 가져와서 texts에 저장
            texts = [chat for chat in st.session_state.chat if chat["role"] in ["user", "assistant"]]
            answer = openai_api.ask_gpt(texts, sys_inst=SYSTEM_INSTRUCTION)
            st.session_state.chat.append({"content": answer, "role": "assistant"})
            st.rerun()
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
        
# 환영 메시지 표시
message(WELCOME_MESSAGE)

# 게임 초기화 - 첫 방문 시 자동으로 게임 시작
if st.session_state.chat == []:
    try:
        st.session_state.chat.append({"role": "user", "content": START_GAME_MESSAGE})
        answer = openai_api.ask_gpt(st.session_state.chat, sys_inst=SYSTEM_INSTRUCTION)
        st.session_state.chat.append({"content": answer, "role": "assistant"})
    except Exception as e:
        st.error(f"게임 시작 중 오류가 발생했습니다: {str(e)}")

# 대화 기록 표시
if st.session_state.chat:
    for idx, chat in enumerate(st.session_state.chat):
        if chat["role"] == "audio":
            # 사용자가 녹음한 음성 파일 표시
            st.audio(chat["content"])
        elif chat["role"] == "user":
            # 사용자 메시지 표시
            message(chat["content"], is_user=True, key=str(idx))
        elif chat["role"] == "assistant":
            # AI 응답 메시지 표시
            message(chat["content"], is_user=False, key=str(idx))
        else:
            # 기타 오디오 콘텐츠 표시
            st.html(f'''<audio controls>{chat["content"]}</audio>''')

# 음성 녹음 처리
if len(audio) > 0:
    try:
        # 녹음된 오디오를 프론트엔드에 표시
        audio_ = audio.export().read()
        st.audio(audio_)
        st.session_state.chat.append({"content": audio_, "role": "audio"})
        
        # 오디오를 파일로 저장
        audio.export(INPUT_AUDIO_FILE, format="mp3")

        # 음성을 텍스트로 변환 (STT)
        text = openai_api.stt()
        
        # 오류 메시지 확인
        if text.startswith("오류:"):
            st.error(text)
        else:
            message(text, is_user=True)
            st.session_state.chat.append({"content": text, "role": "user"})
            
            # chat 중에서 role이 user, assistant인 것만 가져와서 texts에 저장
            texts = [chat for chat in st.session_state.chat if chat["role"] in ["user", "assistant"]]

            # GPT 응답 생성
            answer = openai_api.ask_gpt(texts, sys_inst=SYSTEM_INSTRUCTION)
            
            # 오류 메시지 확인
            if answer.startswith("오류:"):
                st.error(answer)
            else:
                st.session_state.chat.append({"content": answer, "role": "assistant"})
                message(answer)
                
    except Exception as e:
        st.error(f"음성 처리 중 오류가 발생했습니다: {str(e)}")

