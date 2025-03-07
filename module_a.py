#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module A: 结巴分词模块
提供中文文本分词功能
"""

import jieba
import json
from typing import List, Dict, Union, Optional


class JiebaSegmenter:
    """结巴分词模型类"""
    
    def __init__(self, user_dict_path: Optional[str] = None):
        """
        初始化分词器
        
        Args:
            user_dict_path: 可选的用户自定义词典路径
        """
        if user_dict_path:
            jieba.load_userdict(user_dict_path)
            
    def segment(self, text: str, cut_all: bool = False) -> List[str]:
        """
        对输入文本进行分词
        
        Args:
            text: 要分词的文本
            cut_all: 是否使用全模式分词，默认为精确模式(False)
            
        Returns:
            分词结果列表
        """
        if not text or not isinstance(text, str):
            return []
            
        if cut_all:
            return list(jieba.cut(text, cut_all=True))
        else:
            return list(jieba.cut(text))
            
    def segment_with_pos(self, text: str) -> List[tuple]:
        """
        对输入文本进行词性标注分词
        
        Args:
            text: 要分词的文本
            
        Returns:
            带词性标注的分词结果列表，每个元素为(词, 词性)的元组
        """
        import jieba.posseg as pseg
        
        if not text or not isinstance(text, str):
            return []
            
        return list(pseg.cut(text))
        
    def extract_keywords(self, text: str, top_k: int = 5) -> List[Dict[str, Union[str, float]]]:
        """
        提取文本关键词
        
        Args:
            text: 输入文本
            top_k: 返回关键词数量
            
        Returns:
            关键词列表，每个元素为包含词和权重的字典
        """
        import jieba.analyse
        
        if not text or not isinstance(text, str):
            return []
            
        keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
        return [{"word": word, "weight": weight} for word, weight in keywords]
        
    def process_text(self, text: str, mode: str = "default") -> Dict:
        """
        处理文本主函数
        
        Args:
            text: 输入文本
            mode: 分词模式，可选值:
                - "default": 默认精确模式
                - "full": 全模式
                - "pos": 词性标注
                - "keywords": 关键词提取
                
        Returns:
            包含分词结果的字典
        """
        result = {
            "original_text": text,
            "mode": mode,
            "result": None
        }
        
        if mode == "default":
            result["result"] = self.segment(text)
        elif mode == "full":
            result["result"] = self.segment(text, cut_all=True)
        elif mode == "pos":
            pos_result = self.segment_with_pos(text)
            result["result"] = [{"word": word, "pos": pos} for word, pos in pos_result]
        elif mode == "keywords":
            result["result"] = self.extract_keywords(text)
        else:
            result["result"] = self.segment(text)
            result["mode"] = "default"
            
        return result


def segment_text(text: str, mode: str = "default", user_dict: Optional[str] = None) -> Dict:
    """
    对外提供的分词接口函数
    
    Args:
        text: 要分词的文本
        mode: 分词模式
        user_dict: 可选的用户词典路径
        
    Returns:
        分词结果字典
    """
    segmenter = JiebaSegmenter(user_dict)
    return segmenter.process_text(text, mode)


if __name__ == "__main__":
    # 作为脚本运行时的示例代码
    import sys
    
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = "我爱北京天安门，天安门上太阳升。中华人民共和国万岁！"
        
    result = segment_text(input_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 词性标注示例
    pos_result = segment_text(input_text, mode="pos")
    print(json.dumps(pos_result, ensure_ascii=False, indent=2))
    
    # 关键词提取示例
    keywords_result = segment_text(input_text, mode="keywords")
    print(json.dumps(keywords_result, ensure_ascii=False, indent=2))

