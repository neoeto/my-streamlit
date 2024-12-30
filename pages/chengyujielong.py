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
RESULT_KEY = "RESULT"
MODEL = "deepseek-chat"
# MODEL = "glm-4-plus"

if MESSAGE_KEY not in st.session_state:
    st.session_state[MESSAGE_KEY] = []

def chat_jielong(chengyu):
    # client = ZhipuAI(api_key=st.session_state[ZHIPU_KEY])
    client = OpenAI(
        api_key=st.session_state[ZHIPU_KEY],
        base_url="https://api.deepseek.com"
    )
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user", "content":chengyu}
        ],
        stream=False,
        temperature=0
    )

    return completion.choices[0].message.content

def is_legal_chengyu(first, yours):
    if len(first) <= 0:
        return True
    if len(yours) <= 0:
        return False
    return first[-1] == yours[0]

if RESULT_KEY not in st.session_state:
    st.session_state[RESULT_KEY] = True

def show_chat():
    if not st.session_state[RESULT_KEY]:
        return
    input = st.chat_input("请输入成语")
    if input:
        for chat_msg in st.session_state[MESSAGE_KEY]:
            st.chat_message(chat_msg[0]).markdown(chat_msg[1])

        st.chat_message('human').markdown(input)
        if len(st.session_state[MESSAGE_KEY]) > 0 and \
              not is_legal_chengyu(st.session_state[MESSAGE_KEY][-1][1], input):
            st.chat_message('assistant').write('你的回答错咯')
            return
        
        st.session_state[MESSAGE_KEY].append(['human', input])
        resp = chat_jielong(input)
        if not is_legal_chengyu(input, resp):
            resp = "我回答不出来，认输了!"

        st.chat_message('assistant').markdown(resp)
        st.session_state[MESSAGE_KEY].append(['assistant', resp])


if ZHIPU_KEY not in st.session_state:
    st.session_state[ZHIPU_KEY] = None

def api_key_submit(key):
    if len(key) > 0:
        st.session_state[ZHIPU_KEY] = key

if st.session_state[ZHIPU_KEY] is None:
    key = st.text_input('api key')
    def sub():
        api_key_submit(key)
    st.button('提交', on_click=sub)
else:
    show_chat()