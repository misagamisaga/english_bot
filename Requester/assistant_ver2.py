import warnings
warnings.filterwarnings("ignore")

import os
import streamlit as st
import random
# import requests
# import re

# from langchain.llms import OpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# ---- 准备工作 ----
os.environ["OPENAI_API_BASE"] = "https://api.chatanywhere.tech/v1"

template_evaluate = """
You are a very skilled English teacher. Now you need to evaluate the student's performance in English conversation. Please guide this user to engage in English conversation and test their English language ability.  

The evaluation section needs to consist of three parts. When the other party provides an English answer, please primarily evaluate in Chinese.  
1. Rate the other party's response on a scale of 0-10 points, with 0 indicating poor response and 10 indicating excellent response.  
2. Check if there are any grammar or vocabulary errors in the other party's answer. If so, please point out the errors and provide suggestions for correction.  
3. Provide an example to demonstrate the correct English expression and explain why it is better to say it that way.  

Please note that the correct demonstration sentence you provide must be in English.

Chat history:{chat_history}

Answer from the student:{user_question}
"""

template_conversation = """
You are a very skilled English teacher. Now you need to practice English with a student through conversation. Please guide this user to engage in English conversation and test their English language ability.  

Based on the history of the conversation, continue the English conversation, guide him to speak more English, and try to test his English language ability as much as possible.  

Chat history:{chat_history}

Answer from the student:{user_question}
"""

# 改为雅思题库
text_list_yasi = [
    "Are there many advertisements in your country?", 
    "Why do you think there are so many advertisements in your country now?", 
    "What are the various places where we see advertisements?", 
    "How do you feel about advertisements?", 
    "How do children celebrate birthdays in your country?", 
    "How did you celebrate your last birthday?", 
    "What kind of birthday gift did you like toreceive?", 
    "Is there a difference between the way you celebrated your birthday in the past and in the present?", 
    "Do you like flowers?", 
    "What flowers do you like?", 
    "Which/What is your favorite flower?", 
    "Do you think flowers are importnat?", 
    "Are flowers important in your culture?", 
    "On what occasions are flowers important?", 
    "Do people in your country ever use flowers for special occasions?", 
    "In your country, do people give flowers as a gift?", 
    "What are the occasions when people give or receive flowers?", 
]
text_start = "The IELTS exam has officially begun, and AI assistants will act as examiners to ask initial questions and assess students' English proficiency through chat. Please have students engage in a dialogue based on the examiner's questions."

# ---- 页面内容 ----

# 设置本页在侧边栏中的名称和图标
# st.set_page_config("AI英语陪练", "🤖")

col1, col2 = st.columns([2, 1])
with col1:
    # 页面头部的东西
    st.title("AI英语雅思陪练")

with col2:
    st.markdown("\n")
    if_clean = st.button("新对话")

if if_clean:
    # st.cache_data.clear()
    # st.cache_resource.clear()
    st.session_state.chat_history = [
        SystemMessage(content=text_start), 
        AIMessage(content=random.choice(text_list_yasi))
    ]

st.markdown("""> 您好！感谢您试用我。由于模型还在开发阶段，以下内容可能需要您注意: 
> * **请等待模型回答完毕后再提问下一个问题，以防止回答内容被覆盖。** 
> * **目前模型的回答质量还不错，但仍然处于开发阶段，反应较慢，且回答可能有所偏差。** 请您谅解，我们会持续改进模型的能力，并且很乐意收到您的反馈。
---
""")

api_in = st.text_input(label="请输入您的api-key")

# 初始化页面的时候让AI显示一条欢迎语，并存入messages
if "chat_history" not in st.session_state:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.chat_history = [
        SystemMessage(content=text_start), 
        AIMessage(content=random.choice(text_list_yasi))
    ]

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# def get_response_chat(user_query, chat_history):
#     prompt = ChatPromptTemplate.from_template(template_conversation)
#     llm = ChatOpenAI(model="gpt-4")
#     chain = prompt | llm | StrOutputParser()
#     return chain.stream({
#         "chat_history": chat_history,
#         "user_question": user_query,
#     })

# def get_response_eval(user_query, chat_history):
#     prompt = ChatPromptTemplate.from_template(template_evaluate)
#     llm = ChatOpenAI(model="gpt-4")
#     chain = prompt | llm | StrOutputParser()
#     return chain.stream({
#         "chat_history": chat_history,
#         "user_question": user_query,
#     })

# 等待用户输入然后按回车
if ques_user := st.chat_input("你好，有什么可以帮你？"):

    llm = ChatOpenAI(model="gpt-4o-2024-08-06", api_key=api_in)
    
    # 在messages里面存入用户的消息
    st.session_state.chat_history.append(HumanMessage(content=ques_user))

    # 在messages里面显示用户的回答
    with st.chat_message("Human"):
        st.markdown(ques_user)

    # 在messages里面流式显示AI的回答
    with st.chat_message("AI"):
        # response = st.write_stream(get_response_chat(ques_user, st.session_state.chat_history))
        prompt_chat = ChatPromptTemplate.from_template(template_conversation)
        chain_chat = prompt_chat | llm | StrOutputParser()
        response = st.write_stream(chain_chat.stream({
            "chat_history": st.session_state.chat_history,
            "user_question": ques_user,
        }))
    
    # 在messages里面存入本次AI的回答
    st.session_state.chat_history.append(AIMessage(content=response))

    # ----- 评估部分 -----
    prompt_eval = ChatPromptTemplate.from_template(template_evaluate)
    chain_eval = prompt_eval | llm | StrOutputParser()

    with st.sidebar:
        st.markdown("### 本次问答评价：")
        st.write_stream(chain_eval.stream({
            "chat_history": st.session_state.chat_history,
            "user_question": ques_user,
        }))
