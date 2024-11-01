# Hello.py
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="올인원 챗봇",
    page_icon="👋",
)

# 메인 페이지 내용
st.write("# Welcome to 올인원 챗봇! 👋")

# 사이드바 안내 메시지
st.sidebar.success("Select your language.")

st.markdown(
    """
    I will assist you with preparing your civil complaint document in korean language. 
    **👈 Please select your desired language from the options on the left.**
    """
)
