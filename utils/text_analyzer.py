from transformers import pipeline
import networkx as nx
from typing import Dict
import spacy
import logging

class TextAnalyzer:
    def __init__(self):
        try:
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            self.nlp = spacy.load("zh_core_web_sm")
        except Exception as e:
            logging.error(f"初始化 TextAnalyzer 失敗: {str(e)}")
            raise
        
    def generate_summaries(self, documents: Dict) -> Dict:
        """生成文檔摘要"""
        summaries = {}
        for doc_name, content in documents.items():
            try:
                if not content.strip():
                    summaries[doc_name] = "文件內容為空"
                    continue
                    
                if len(content) > 1024:  # BART 模型有最大輸入限制
                    content = content[:1024]
                    
                summary = self.summarizer(content, max_length=130, min_length=30, do_sample=False)
                summaries[doc_name] = summary[0]['summary_text']
            except Exception as e:
                logging.error(f"處理文件 {doc_name} 時發生錯誤: {str(e)}")
                summaries[doc_name] = f"無法生成摘要: {str(e)}"
        return summaries
    
    def highlight_important_passages(self, documents: Dict) -> str:
        """標註重要段落"""
        highlighted_text = []
        try:
            for doc_name, content in documents.items():
                if not content or not content.strip():
                    highlighted_text.append(f"<div>文件 {doc_name} 內容為空</div>")
                    continue
                    
                doc = self.nlp(content)
                
                # 使用規則識別重要段落
                important_patterns = ["結論", "研究發現", "本文提出", "實驗結果"]
                
                # 添加文檔標題
                highlighted_text.append(f"<h3>{doc_name}</h3>")
                highlighted_text.append("<div>")
                
                # 處理每個句子
                for sent in doc.sents:
                    try:
                        text = sent.text.strip()
                        if any(pattern in text for pattern in important_patterns):
                            highlighted_text.append(f'<span style="background-color: yellow">{text}</span>')
                        else:
                            highlighted_text.append(text)
                        highlighted_text.append("<br>")
                    except Exception as e:
                        logging.warning(f"處理句子時發生錯誤: {str(e)}")
                        continue
                
                highlighted_text.append("</div>")
                
        except Exception as e:
            logging.error(f"標註過程發生錯誤: {str(e)}")
            return f"<div>處理文件時發生錯誤: {str(e)}</div>"
        
        # 使用換行符連接所有文本片段
        return "\n".join(highlighted_text)

    def process_pdfs(self, files):
        documents = {}
        for file in files:
            if self.is_supported_file(file.name):
                content = file.read()
                text = self.process_pdf(content)
                documents[file.name] = text
        return documents 