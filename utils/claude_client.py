# utils/claude_client.py
import anthropic
import logging
from typing import Dict

class ClaudeClient:
    def __init__(self, api_key: str):
        """初始化 Claude Client"""
        try:
            self.api_key = api_key
            # 移除 proxies 參數，使用最簡單的初始化方式
            self.client = anthropic.Client(
                api_key=self.api_key
            )
        except Exception as e:
            logging.error(f"初始化 Claude Client 失敗: {str(e)}")
            raise

    def analyze_document(self, content: str) -> Dict:
        """使用 Claude 分析文檔內容"""
        try:
            system = "你是一個專業的學術論文分析助手。"
            prompt = f"""請分析以下學術文獻，並提供：
            1. 主要研究問題
            2. 研究方法
            3. 關鍵發現
            4. 研究貢獻

            文獻內容：
            {content}
            """
            
            try:
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    system=system,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return {
                    "analysis": response.content[0].text,
                    "status": "success"
                }
            except Exception as api_error:
                logging.error(f"API 調用錯誤: {str(api_error)}")
                return {
                    "analysis": f"API 調用失敗: {str(api_error)}",
                    "status": "error"
                }
                
        except Exception as e:
            logging.error(f"分析過程發生錯誤: {str(e)}")
            return {
                "analysis": f"分析失敗: {str(e)}",
                "status": "error"
            }