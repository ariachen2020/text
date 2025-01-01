import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib
import platform
import warnings
import hashlib

# 忽略特定警告
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# 根據作業系統選擇合適的字體
if platform.system() == 'Darwin':  # macOS
    matplotlib.rcParams['font.family'] = ['PingFang HK', 'Heiti TC']
else:  # Windows 或 Linux
    matplotlib.rcParams['font.family'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

class Visualizer:
    def _create_safe_node_id(self, text: str) -> str:
        """創建安全的節點ID"""
        # 使用 MD5 來創建唯一且安全的節點 ID
        return f"node_{hashlib.md5(text.encode()).hexdigest()[:8]}"

    def create_concept_graph(self, documents: Dict):
        """創建概念關係圖"""
        try:
            # 清除之前的圖形
            plt.close('all')
            
            # 創建一個新的圖形
            fig, ax = plt.subplots(figsize=(12, 8))
            G = nx.Graph()
            
            # 使用 TF-IDF 提取關鍵詞
            vectorizer = TfidfVectorizer(max_features=10)
            
            # 處理每個文檔
            for doc_name, content in documents.items():
                if not content.strip():
                    continue
                    
                # 提取關鍵詞
                try:
                    tfidf_matrix = vectorizer.fit_transform([content])
                    feature_names = vectorizer.get_feature_names_out()
                    
                    # 獲取前 N 個關鍵詞
                    top_n = 5
                    prev_node_id = None
                    for i in range(min(top_n, len(feature_names))):
                        word = feature_names[i]
                        # 創建安全的節點ID
                        node_id = self._create_safe_node_id(f"{word}_{doc_name}_{i}")
                        
                        # 添加節點
                        G.add_node(node_id, label=word)
                        
                        # 添加邊
                        if prev_node_id is not None:
                            G.add_edge(prev_node_id, node_id)
                        prev_node_id = node_id
                            
                except Exception as e:
                    print(f"處理文件 {doc_name} 時發生錯誤: {str(e)}")
                    continue
            
            if len(G.nodes) == 0:
                ax.text(0.5, 0.5, "沒有足夠的數據生成圖形",
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=ax.transAxes)
                return fig
            
            # 繪製圖形
            pos = nx.spring_layout(G, k=1, iterations=50)
            nx.draw(G, pos, ax=ax, with_labels=False, 
                   node_color='lightblue', 
                   node_size=2000, 
                   font_size=10)
            
            # 添加標籤
            labels = nx.get_node_attributes(G, 'label')
            nx.draw_networkx_labels(G, pos, labels, ax=ax)
            
            ax.set_title("文檔關鍵詞關係圖")
            
            # 調整布局
            plt.axis('off')
            fig.set_tight_layout(True)
            
            return fig
            
        except Exception as e:
            print(f"創建概念圖時發生錯誤: {str(e)}")
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, f"無法創建圖形: {str(e)}", 
                   horizontalalignment='center', 
                   verticalalignment='center',
                   transform=ax.transAxes)
            return fig