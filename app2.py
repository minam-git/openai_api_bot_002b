
import streamlit as st
import openai
import time

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドの全ての質問に対して以下のルールに厳格に従って答えてください。
1. タロットカードの大アルカナをランダムに選択してください
2. さらに、正位置と逆位置もランダムに選択してください。
3. 質問に対して、1 と 2 でランダムに選ばれた内容を踏まえて回答してください。
"""

#chatbot_setting = st.secrets.AppSettings.chatbot_setting
chatbot_setting = systme_prompt

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": chatbot_setting}
        ]

# 文字列を順次表示する st.write
def typing_write( msgtext, intervalTime=0.1 ):
    overWrite = st.empty()
#    st.write("長さ", len(msgtext))
    for i in range(len(msgtext)+1):
        time.sleep(intervalTime)
        
        with overWrite.container():
            st.write(msgtext[:i])
            
# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
#st.write("ChatGPT APIを使ったチャットボットです。")
typing_write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
