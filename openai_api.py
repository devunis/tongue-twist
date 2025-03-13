import base64
from openai import OpenAI
import dotenv
import os
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def stt():
    text = ""
    with open("input.mp3", "rb") as f:
        transcriptions = client.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            language="ko"
        )
        text = transcriptions.text
        f.close()
    # 임시 파일 삭제
    os.remove("input.mp3")
    return text

def ask_gpt(query, temperature=0.5, max_tokens=1024, sys_inst=""):
    if sys_inst == "":
        sys_inst = """
        너는 세상에서 제일 강한 슈퍼 울트라 캡숑 다람쥐야. 
        말끝마다 다람쥐 썬더! 를 붙인다. 
        세계 최강 다람쥐에 걸맞는 말투와 행동을 해야해! 
        잊지마! 너는 세계 최강이야!
        """
    messages=[{"role": "system", "content": sys_inst}]
    messages.extend(query)
    # query.append({"role": "system", "content": sys_inst})
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return res.choices[0].message.content

def tts(text):
    filename = "output.wav"

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
        f.close()
        # 임시 파일 삭제
    os.remove(filename)
    return audio_tag