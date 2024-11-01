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

# 일본어 안내 페이지 콘텐츠 함수
def japanese_page():
    st.title("外国人住民の申請アシスタント - 日本語")
    st.write("このページでは外国人の住所変更に関する情報を提供しています。")

    # 質問 입력
    query = st.text_input("以下に質問を入力してください", "例: 引っ越しをしたいのですが、どのような手続きをすればよいですか？")

    # 질문이 특정 내용일 경우 기본 응답을 설정
    default_response = """
    まず、住所変更を届け出る必要があります。引っ越し後15日以内に住所変更を届け出る必要があります。
    遅れて届け出をする場合は、新しい住所地の出入国管理局または地方自治体の事務所で申告してください。
    必要な書類:
    1. 住所変更届出書
    2. 身分証明書（外国人登録証）
    3. 住所証明（賃貸契約書、宿泊証明書など）
    """

    # 질문 버튼
    if st.button("質問を送信"):
        if "move" in query.lower() or "procedures" in query.lower():
            st.write("### 回答")
            st.write(default_response)

            # 추가 질문 제공
            follow_up = st.radio(
                "外国人住所変更届を英語で確認したいですか？ それとも韓国語で入力しますか？",
                ("自分で進めますので、英語版の書式のリンクだけ教えてください", "はい、韓国語で入力します", "いいえ、大丈夫です")
            )

            # 사용자 선택에 따른 응답
            if follow_up == "自分で進めますので、英語版の書式のリンクだけ教えてください":
                st.write("### 外国人住所変更届（英語）")
                form_url = "https://www.hygn.go.kr/00428/00435/00501.web"
                st.markdown(f"[英語版の書式を開く]({form_url})", unsafe_allow_html=True)

            elif follow_up == "はい、韓国語で入力します":
                st.write("### 外国人住所変更届の作成")
                st.write("韓国語で書式の入力を進めてください。")

        else:
            # 일반적인 질문 처리
            selected_file_path = pdf_files.get("외국인 체류지변경 신고서", "ファイルが見つかりません")
            print(selected_file_path)
            db = prepare_embeddings(selected_file_path)
            retriever = db.as_retriever()

            # 프롬프트 템플릿 설정
            template = """
              あなたはPDFファイルから情報を抽出するAIアシスタントです。文脈に基づいて回答を提供してください。
              クエリ: {query}
              {context}
            """
            prompt = ChatPromptTemplate.from_template(template)

            # 대화 체인 생성
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

# 일본어 안내 페이지 렌더링
japanese_page()
