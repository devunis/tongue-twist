"""
OpenAI API 통합 모듈
음성-텍스트 변환(STT), GPT 챗봇, 텍스트-음성 변환(TTS) 기능 제공
"""
import base64
import os
from typing import List, Dict, Optional
from openai import OpenAI
import dotenv

# 환경 변수 로드
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

def stt() -> str:
    """
    음성 파일을 텍스트로 변환 (Speech-to-Text)
    
    Returns:
        str: 변환된 텍스트
        
    Raises:
        Exception: 파일 처리 또는 API 호출 실패 시
    """
    try:
        with open("input.mp3", "rb") as f:
            transcriptions = client.audio.transcriptions.create(
                file=f,
                model="whisper-1",
                language="ko"
            )
            text = transcriptions.text
        
        # 임시 파일 삭제
        if os.path.exists("input.mp3"):
            os.remove("input.mp3")
            
        return text
    except FileNotFoundError:
        return "오류: 음성 파일을 찾을 수 없습니다."
    except Exception as e:
        return f"오류: 음성 인식 중 문제가 발생했습니다. ({str(e)})"

def ask_gpt(query: List[Dict[str, str]], temperature: float = 0.5, 
            max_tokens: int = 1024, sys_inst: str = "") -> str:
    """
    GPT 모델에 질문하고 응답을 받음
    
    Args:
        query: 대화 기록 리스트 [{"role": "user", "content": "..."}]
        temperature: 응답의 창의성 조절 (0.0-2.0)
        max_tokens: 최대 응답 토큰 수
        sys_inst: 시스템 인스트럭션 (역할 지정)
        
    Returns:
        str: GPT 모델의 응답 텍스트
        
    Raises:
        Exception: API 호출 실패 시
    """
    try:
        if sys_inst == "":
            sys_inst = """
            너는 세상에서 제일 강한 슈퍼 울트라 캡숑 다람쥐야. 
            말끝마다 다람쥐 썬더! 를 붙인다. 
            세계 최강 다람쥐에 걸맞는 말투와 행동을 해야해! 
            잊지마! 너는 세계 최강이야!
            """
        
        messages = [{"role": "system", "content": sys_inst}]
        messages.extend(query)
        
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"오류: GPT 응답 생성 중 문제가 발생했습니다. ({str(e)})"

def tts(text: str) -> str:
    """
    텍스트를 음성으로 변환 (Text-to-Speech)
    
    Args:
        text: 음성으로 변환할 텍스트
        
    Returns:
        str: base64 인코딩된 오디오 태그
        
    Raises:
        Exception: 파일 처리 또는 API 호출 실패 시
    """
    filename = "output.wav"
    
    try:
        with client.audio.speech.with_streaming_response.create(
            model='tts-1',
            voice='coral',
            input=text
        ) as response:
            response.stream_to_file(filename)
        
        with open(filename, "rb") as f:
            audio = f.read()
            base64_encoded = base64.b64encode(audio).decode("utf-8")
            audio_tag = f'<source src="data:audio/wav;base64,{base64_encoded}" type="audio/wav" />'
        
        # 임시 파일 삭제
        if os.path.exists(filename):
            os.remove(filename)
            
        return audio_tag
    except Exception as e:
        return f'<p>오류: 음성 합성 중 문제가 발생했습니다. ({str(e)})</p>'