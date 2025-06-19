#!/usr/bin/env python3
"""
AI 术语词典生成工具
基于机器之心人工智能术语数据库创建专业的翻译词典

GitHub: https://github.com/jiqizhixin/Artificial-Intelligence-Terminology-Database
"""

import json
import requests
import csv
import os
from io import StringIO

def download_terminology_data():
    """
    从机器之心 GitHub 仓库下载术语数据
    """
    print("正在下载机器之心人工智能术语数据库...")
    
    # 主要术语文件的 GitHub raw URL
    base_urls = {
        "通用术语": "https://raw.githubusercontent.com/jiqizhixin/Artificial-Intelligence-Terminology-Database/master/数据文件/AI术语库（机器之心版）.csv",
        "机器学习": "https://raw.githubusercontent.com/jiqizhixin/Artificial-Intelligence-Terminology-Database/master/数据文件/机器学习术语库.csv",
        "AI_for_Science": "https://raw.githubusercontent.com/jiqizhixin/Artificial-Intelligence-Terminology-Database/master/数据文件/AI for Science术语库.csv"
    }
    
    all_terms = {}
    
    for category, url in base_urls.items():
        try:
            print(f"下载 {category} 术语...")
            response = requests.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                # 解析 CSV 数据
                csv_content = StringIO(response.text)
                csv_reader = csv.DictReader(csv_content)
                
                category_count = 0
                for row in csv_reader:
                    # 获取英文术语和中文翻译
                    english_term = row.get('英文', '').strip()
                    chinese_term = row.get('中文', '').strip()
                    
                    # 处理可能的别名字段
                    abbr = row.get('缩写', '').strip()
                    
                    if english_term and chinese_term:
                        # 主术语
                        all_terms[english_term] = chinese_term
                        category_count += 1
                        
                        # 如果有缩写，也加入词典
                        if abbr and abbr != english_term:
                            all_terms[abbr] = chinese_term
                            category_count += 1
                
                print(f"  成功加载 {category_count} 个术语")
            else:
                print(f"  警告：无法下载 {category} 术语 (HTTP {response.status_code})")
                
        except Exception as e:
            print(f"  错误：下载 {category} 时出现问题: {e}")
            continue
    
    return all_terms

def create_comprehensive_glossary():
    """
    创建综合的 AI 术语词典文件
    """
    print("=== AI 术语词典生成工具 ===")
    print("基于机器之心人工智能术语数据库")
    print("GitHub: https://github.com/jiqizhixin/Artificial-Intelligence-Terminology-Database")
    print()
    
    # 下载术语数据
    ai_terms = download_terminology_data()
    
    if not ai_terms:
        print("错误：无法获取术语数据，将创建基础示例词典")
        # 创建一个基础的 AI 术语词典作为后备
        ai_terms = {
            "Artificial Intelligence": "人工智能",
            "Machine Learning": "机器学习", 
            "Deep Learning": "深度学习",
            "Neural Network": "神经网络",
            "Natural Language Processing": "自然语言处理",
            "Computer Vision": "计算机视觉",
            "Reinforcement Learning": "强化学习",
            "Supervised Learning": "监督学习",
            "Unsupervised Learning": "无监督学习",
            "Feature Engineering": "特征工程",
            "Gradient Descent": "梯度下降",
            "Backpropagation": "反向传播",
            "Convolutional Neural Network": "卷积神经网络",
            "Recurrent Neural Network": "循环神经网络",
            "Transformer": "变换器",
            "Attention Mechanism": "注意力机制",
            "Generative Adversarial Network": "生成对抗网络",
            "Large Language Model": "大语言模型",
            "Fine-tuning": "微调",
            "Pre-training": "预训练"
        }
    
    # 合并现有的示例词典中有用的术语
    additional_terms = {
        "API": "应用程序接口",
        "JavaScript": "JavaScript",
        "Python": "Python", 
        "New York": "纽约",
        "Los Angeles": "洛杉矶",
        "Silicon Valley": "硅谷",
        "Wall Street": "华尔街",
        "United States": "美国",
        "China": "中国",
        "Europe": "欧洲"
    }
    
    # 合并所有术语
    comprehensive_glossary = {**ai_terms, **additional_terms}
    
    # 保存为 JSON 文件
    output_file = "ai_terminology_glossary.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_glossary, f, ensure_ascii=False, indent=2, sort_keys=True)
        
        print(f"✅ 成功创建 AI 术语词典：{output_file}")
        print(f"📊 总计包含 {len(comprehensive_glossary)} 个术语")
        print()
        print("使用方法：")
        print(f"python translate_srt_batch.py your_file.srt -g {output_file}")
        print()
        print("术语词典已按字母顺序排序，包含以下类别：")
        print("- 机器学习与深度学习术语")
        print("- AI for Science 专业术语") 
        print("- 通用人工智能术语")
        print("- 编程与技术术语")
        print("- 地名与常用词汇")
        
        return output_file
        
    except Exception as e:
        print(f"❌ 保存词典文件时出错：{e}")
        return None

def preview_glossary(file_path, num_terms=10):
    """
    预览词典内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            glossary = json.load(f)
        
        print(f"\n📖 词典预览（显示前 {num_terms} 个术语）：")
        print("-" * 50)
        
        for i, (en_term, cn_term) in enumerate(list(glossary.items())[:num_terms]):
            print(f"{i+1:2d}. {en_term:<30} → {cn_term}")
        
        if len(glossary) > num_terms:
            print(f"    ... 还有 {len(glossary) - num_terms} 个术语")
            
    except Exception as e:
        print(f"预览词典时出错：{e}")

if __name__ == "__main__":
    # 创建综合词典
    glossary_file = create_comprehensive_glossary()
    
    if glossary_file:
        # 预览词典内容
        preview_glossary(glossary_file, 15)
        
        print(f"\n🎯 词典文件已保存为：{glossary_file}")
        print("您现在可以在字幕翻译中使用这个专业的 AI 术语词典了！") 