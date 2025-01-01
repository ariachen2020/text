import streamlit as st
import os
from utils.pdf_processor import PDFProcessor
from utils.claude_client import ClaudeClient

st.set_page_config(page_title="PDF研究助手", layout="wide")

def main():
    st.title("PDF論文研究助手")
    
    # 從環境變量或 Streamlit Secrets 獲取 API key
    api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        api_key = st.sidebar.text_input("請輸入 Anthropic API Key", type="password")
        if not api_key:
            st.error("請設置 ANTHROPIC_API_KEY")
            return
    
    # 驗證 API key 格式
    if not api_key.startswith("sk-ant-"):
        st.error("無效的 API key 格式。Claude API key 應該以 'sk-ant-' 開頭")
        return
    
    try:        
        # 初始化 Claude Client
        claude = ClaudeClient(api_key)
        
        # 文件上傳區域
        uploaded_files = st.file_uploader(
            "上傳PDF文件（可多選）", 
            type="pdf",
            accept_multiple_files=True
        )
        
        if uploaded_files:
            # 初始化處理器
            processor = PDFProcessor()
            
            # 處理上傳的文件
            with st.spinner('正在處理PDF文件...'):
                # 選擇分析類型
                analysis_type = st.selectbox(
                    "選擇分析類型",
                    ["一般分析", "關鍵詞提取", "情感分析"]
                )
                
                # 批次處理PDF
                documents = processor.process_pdfs(uploaded_files)
                
                # 分析結果展示區域
                st.subheader("Claude AI 分析")
                for doc_name, content in documents.items():
                    with st.expander(f"📄 {doc_name}"):
                        # 根據選擇的分析類型進行分析
                        if analysis_type == "一般分析":
                            analysis = claude.analyze_document(content)
                        elif analysis_type == "關鍵詞提取":
                            analysis = claude.analyze_text(content, "keywords")
                        else:  # 情感分析
                            analysis = claude.analyze_text(content, "sentiment")
                            
                        if isinstance(analysis, dict) and "status" in analysis:
                            if analysis["status"] == "success":
                                st.markdown(analysis["analysis"])
                            else:
                                st.error(analysis["analysis"])
                        else:
                            st.markdown(analysis)
                
    except Exception as e:
        st.error(f"處理過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()