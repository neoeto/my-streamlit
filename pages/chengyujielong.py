# from zhipuai import ZhipuAI
from openai import OpenAI
import streamlit as st


system_prompt = '''
    你是人工智能助手，擅长进行成语接龙，成语接龙的规则是：给出一个以对手给的成语的最后一个字为开头的成语，比如：对手给的成语是"一五一十"，那么你需要回到出一个以"十"字开头的成语，注意：你回答成语的第一个字必须和对手给的成语的最后一个字一样，而不能只是读音相同
    如果能找到相应的成语，则只需要给出成语即可，无需其他信息
    如果无法给出相应的成语，则输掉本次成语接龙，需要给出提示：我答不出来，你赢了
    必须严格按照如上规则进行
    '''

ZHIPU_KEY = "ZHIPU_LEY"
MESSAGE_KEY = "MESSAGE"
MODEL = "deepseek-chat"

if MESSAGE_KEY not in st.session_state:
    st.session_state[MESSAGE_KEY] = []

def chat_jielong(chengyu):
    # client = ZhipuAI(api_key=st.session_state[ZHIPU_KEY])
    client = OpenAI(
        api_key=st.session_state[ZHIPU_KEY],
        base_url="https://api.deepseek.com/v1"
    )
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user", "content":chengyu}
        ],
        temperature=0
    )

    return completion.choices[0].message.content

def show_chat():
    input = st.chat_input("请输入成语")
    if input:
        for chat_msg in st.session_state[MESSAGE_KEY]:
            st.chat_message(chat_msg[0]).markdown(chat_msg[1])

        st.chat_message('human').markdown(input)
        st.session_state[MESSAGE_KEY].append(['human', input])
        resp = chat_jielong(input)
        st.chat_message('assistant').markdown(resp)
        st.session_state[MESSAGE_KEY].append(['assistant', resp])


if ZHIPU_KEY not in st.session_state:
    st.session_state[ZHIPU_KEY] = ''
    with st.container():
        zhipu_key = st.text_input("请输入智谱api key")
        saved = st.button("确定")
        if saved and len(zhipu_key) > 0:
            st.session_state[ZHIPU_KEY] = zhipu_key
else:
    show_chat()
