# pip install streamlit streamlit-chat streamlit-audiorecorder
# pip install streamlit-audiorecorder
# pip install streamlit-chat
# pip install audio-recorder-streamlit
import openai_api
import streamlit as st
from audiorecorder import audiorecorder
from streamlit_chat import message

sys_inst = """
우리는 앵무새 게임을 진행할거야
너가 발음하기 어려운 한국어 단어나 한국어 문장을 얘기하면
내가 그걸 듣고 다시 말할거야
그리고 내가 잘 발음했는지 확인해줘
제대로 발을하지 못했으면 틀렸으니 다시 말씀하세요 라고 얘기해
제대로 발음했으면 맞았다고 얘기하고 다음 문장을 말해주면 돼
예시로 주어진 것 중에서 20자 이내로 잘라서 말해줘
### 예시 ###
햄부기햄북 햄북어 햄북스딱스 함부르크햄부가우가 햄비기햄부거 햄부가티햄부기온앤 온을 차려오거라. 햄부기햄북 햄북어 햄북스딱스 함부르크햄부가우가 햄비기햄부거 햄부가티햄부기온앤온을 차려오라고 하지않앗느냐
안촉촉한 초코칩은 촉촉한 초코칩이 되는것을 포기하고 안촉촉한 초코칩 나라로 돌아갔다.
작은 토끼 토끼통 옆 큰 토끼 토끼통 큰 토끼 토끼통 옆 작은 토끼 토끼통
경찰청 검찰청 왼쪽 유리창 중앙 쇠창살은 녹이슨 쇠창살 이고 경찰청 검찰청 오른쪽 유리창 중앙 철창살은 녹이 안슨 철창살 이다.
간장 공장 공장장은 강 공장장이고, 된장 공장 공장장은 공 공장장이다.
목동 로얄 뉴로얄 레스토랑 뉴메뉴 미트소시지소스스파게티, 크림소시지소스스테이크
스위스에서 오셔서 산새들이 속삭이는 산림 숲속에서 숫사슴을 샅샅이 수색해 식사하고 산 속 샘물로 세수하며 사는 삼십 삼살 샴쌍둥이 미세스 스미스씨와 미스터 심슨씨는 삼성 설립 사장의 회사 자산 상속자인 사촌의 사돈 김상속씨의 숫기있고 숭글숭글한 숫색시 삼성소속 식산업 종사자 김삼순씨를 만나서 삼성 수산물 운송수송 수색 실장에게 스위스에서 숫사슴을 샅샅이 수색했던 것을 인정받아 스위스 수산물 운송 수송 과정에서 상해 삭힌 냄새가 나는 수산물을 수색해내는 삼성 소속 수산물 운송수송 수색 사원이 되서 살신성인으로 쉴새없이 수색하다 산성수에 손이 산화되어 수술실에서 수술하게 됐는데 쉽사리 수술이 잘 안돼서 심신에 좋은 산삼을 달여 슈르릅 들이켰더니 힘이 샘솟아 다시 몸사려 수색하다 삼성 소속 식산업 종사자 김삼순씨와 셋이서 삼삼오오 삼월 삼십 삼일 세시 삼십 삼분 삼십 삼초에 쉰 세살 김식사씨네 시내 스시식당에 식사하러 가서 싱싱한 샥스핀 스시와 삼색샤시참치스시를 살사소스와 슥슥삭삭 샅샅이 비빈 것과 스위스산 소세지를 샤샤샥 싹쓸어 입속에 쑤쎠넣어 살며시 삼키고 스산한 새벽 세시 삼십 삼분 삼십 삼초에 산림 숲속으로 사라졌다.
내가 그린 기린 그림은 잘 그린 기린 그림이고 네가 그린 기린 그림은 못 그린 기린 그림이다.
내가 그린 구름그림은 새털구름 그린 구름그림이고, 네가 그린 구름그림은 깃털구름 그린 구름그림이다.
저기 계신 저 분이 박 법학박사이시고 여기 계신 이 분이 백 법학박사이시다.
경찰청 철창살은 외철창살이냐 쌍철창살이냐
간장 공장 공장장은 강 공장장이고 된장 공장 공장장은 공 공장장이다.
한양 양장점 옆 한영 양장점
신인 샹송 가수의 신춘 샹송 쇼
들의 콩깍지는 깐 콩깍지인가 안 깐 콩깍지인가?
고려고 교복은 고급교복이고 고려고 교복은 고급원단을 사용했다
상표 붙인 큰 깡통은 깐 깡통인가? 안 깐 깡통인가?
칠월칠일은 평창친구 친정 칠순 잔칫날
한국관광공사 곽진광 관광과장
"""

st.title("Perroquet Chatbot")
st.image("pngwing.com.png", use_container_width=True)
answer = ""
session_state = st.session_state
if "chat" not in session_state:
    session_state.chat = []

with st.sidebar.container():
    audio = audiorecorder("녹음 시작", "녹음 종료")
    # if st.sidebar.button("초기화"):
    #     session_state.chat = []
    #     audio = []
    if st.sidebar.button("다음 문장"):
        session_state.chat.append({"role": "user", "content": "다음 문장"})
        # chat 중에서 role이 user, assistant인 것만 가져와서 texts에 저장
        texts = [chat for chat in session_state.chat if chat["role"] in ["user", "assistant"]]
        answer = openai_api.ask_gpt(session_state.chat, sys_inst=sys_inst)
        session_state.chat.append({"content": answer, "role": "assistant"})
        
message("앵무세게임에 오신것을 환영합니다")
if session_state.chat == []:
    session_state.chat.append({"role":"user", "content" : "앵무새 게임 시작"})
    answer = openai_api.ask_gpt(session_state.chat, sys_inst=sys_inst)
    session_state.chat.append({"content": answer, "role": "assistant"})
if session_state.chat:
    for idx, chat in enumerate(session_state.chat):
        if chat["role"] == "audio":
            st.audio(chat["content"])
        elif chat["role"] == "user":
            message(chat["content"], is_user=True, key=str(idx))
        elif chat["role"] == "assistant":
            message(chat["content"], is_user=False, key=str(idx))
        else:
            st.html(f'''<audio controls>{chat["content"]}</audio>''')

if len(audio) > 0:
    # To play audio in frontend:
    audio_ = audio.export().read()
    st.audio(audio_)
    session_state.chat.append({"content": audio_, "role": "audio"})
    audio.export("input.mp3", format="mp3")

    # 음성을 텍스트로 변환
    text = openai_api.stt()
    message(text, is_user=True)
    session_state.chat.append({"content": text, "role": "user"})
    
    # chat 중에서 role이 user, assistant인 것만 가져와서 texts에 저장
    texts = [chat for chat in session_state.chat if chat["role"] in ["user", "assistant"]]

    # GPT 대답 출력
    answer = openai_api.ask_gpt(texts, sys_inst=sys_inst)
    session_state.chat.append({"content": answer, "role": "assistant"})
    message(answer)

