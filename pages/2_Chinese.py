import os
import streamlit as st
from dotenv import load_dotenv
from langchain_upstage import UpstageDocumentParseLoader, UpstageEmbeddings, ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("UPSTAGE_API_KEY")

# PDF 파일 경로 설정
pdf_files = {
    "외국인 체류지변경 신고서": "pdf_documents/외국인_체류지변경_신고서.pdf"
    # 필요한 다른 PDF 파일 경로도 추가할 수 있습니다.
}

# 데이터셋 준비 함수
def read_dataset(file_path):
    all_docs = []
    file1_load = UpstageDocumentParseLoader(file_path, split="page", api_key=api_key)
    docs = file1_load.load()
    for doc in docs:
        all_docs.append(doc)
    return all_docs

# 임베딩 및 문서 저장 함수
def prepare_embeddings(file_path):
    embeddings = UpstageEmbeddings(
        upstage_api_key=api_key,
        model="solar-embedding-1-large"
    )
    docs = read_dataset(file_path)
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs_split = text_splitter.split_documents(docs)
    db = FAISS.from_documents(docs_split, embeddings)
    return db

# 중국어 안내 페이지 콘텐츠 함수
def chinese_page():
    st.title("外国人居留变更申报助手 - 中文")
    st.write("此页面提供有关外国人居留变更申报的信息。")

    # 问题输入
    query = st.text_input("请输入您的问题", "例如：我想搬家，我需要遵循哪些程序？")

    # 当问题涉及特定内容时提供默认回答
    default_response = """
    首先，您需要申报居留变更。居留变更必须在搬家后15天内申报。
    如延迟申报，请前往新居住地区的出入境管理办公室，或者您可以在当地政府办公室申报。
    所需文件:
    1. 居留变更申报表
    2. 身份证件：外国人注册卡
    3. 居住证明（租赁协议、住宿收据等）
    """

    # 提交问题按钮
    if st.button("提交问题"):
        if "move" in query.lower() or "procedures" in query.lower():
            st.write("### 回答")
            st.write(default_response)

            # 提供后续问题选项
            follow_up = st.radio(
                "您希望查看外国人居留变更表的英文版，还是用韩文填写？",
                ("让我自己处理，请直接提供表格地址链接", "是的，用韩文填写", "不，谢谢")
            )

            # 根据用户选择显示的响应
            if follow_up == "让我自己处理，请直接提供表格地址链接":
                st.write("### 外国人居留变更表（英文版）")
                form_url = "https://www.hygn.go.kr/00428/00435/00501.web"
                st.markdown(f"[打开英文版表格]({form_url})", unsafe_allow_html=True)

            elif follow_up == "是的，用韩文填写":
                st.write("### 外国人居留变更申报表填写")
                st.write("请继续用韩文填写表格。")

        else:
            # 一般问题处理
            selected_file_path = pdf_files.get("외국인 체류지변경 신고서", "找不到文件")
            print(selected_file_path)
            db = prepare_embeddings(selected_file_path)
            retriever = db.as_retriever()

            # 提示模板设置
            template = """
              您是一位PDF文件信息检索AI助手。请根据上下文提供回答，仅使用上下文内容，不要编造信息。
              查询: {query}
              {context}
            """
            prompt = ChatPromptTemplate.from_template(template)

            # 创建对话链
            model = ChatUpstage()
            chain = (
                {
                    "context": retriever,
                    "query": RunnablePassthrough()
                }
                | prompt | model | StrOutputParser()
            )

            response = chain.invoke(query)
            st.write("### 回答")
            st.write(response)

# 中文页面渲染
chinese_page()
