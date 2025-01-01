# utils/claude_client.py
import anthropic
import logging
from typing import Dict

class ClaudeClient:
    def __init__(self, api_key: str):
        try:
            self.client = anthropic.Client(api_key=api_key)
        except Exception as e:
            logging.error(f"初始化 Claude Client 失敗: {str(e)}")
            raise

    def analyze_document(self, content: str) -> Dict:
        """使用 Claude 分析文檔內容"""
        try:
            prompt = f"""請分析以下學術文獻，並提供：
            1. 主要研究問題
            2. 研究方法
            3. 關鍵發現
            4. 研究貢獻

            文獻內容：
            {content}
            """
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                system="你是一個專業的學術論文分析助手。",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "analysis": response.content[0].text,
                "status": "success"
            }
            
        except Exception as e:
            logging.error(f"分析過程發生錯誤: {str(e)}")
            return {
                "analysis": f"分析失敗: {str(e)}",
                "status": "error"
            }

    def analyze_text(self, content: str, analysis_type: str) -> Dict:
        """根據不同類型分析文本"""
        try:
            if analysis_type == "keywords":
                prompt = f"請從以下文本中提取關鍵詞並解釋其重要性：\n\n{content}"
            else:  # sentiment
                prompt = f"請分析以下文本的情感傾向和語氣：\n\n{content}"
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                system="你是一個專業的文本分析助手。",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "analysis": response.content[0].text,
                "status": "success"
            }
            
        except Exception as e:
            logging.error(f"分析過程發生錯誤: {str(e)}")
            return {
                "analysis": f"分析失敗: {str(e)}",
                "status": "error"
            }