# 🚀 智译字幕通 (IntelliSubs) - AI 字幕翻译工具

[![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 版本](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![代码风格: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**智译字幕通 (IntelliSubs)** 是一款免费、开源的 AI 字幕翻译工具，旨在为人工智能、科技和教育领域的视频内容提供高质量、高效率的翻译解决方案。

本项目使用 Python 开发，支持批量翻译 SRT 格式的字幕文件，并创新性地集成了可定制的 AI 专业术语库，确保专有名词和技术词汇的翻译准确性。无论您是内容创作者、课程制作者还是语言学习者，智译字幕通都能帮助您轻松打破语言障碍，让优质内容无国界传播。

---

## ✨ 核心功能

-   **🎯 精准的 AI 翻译**: 对接兼容 OpenAI 格式的各大模型 API，提供高质量的翻译结果。
-   **📚 智能术语库**: 自带 AI 领域专业术语库，并支持用户自定义，确保专有名词翻译的准确性和一致性。
-   **⚡️ 批量处理**: 支持一次性翻译文件夹内的所有 `.srt` 字幕文件，极大提升效率。
-   **⏰ 时间码保留**: 完美保留原始字幕的起止时间，只对文本内容进行翻译。
-   **⚙️ 高度可配置**: 支持通过命令行参数或 `.env` 文件自定义翻译模型、温度等参数。

---

## 🚀 快速开始

### 1. 环境准备

确保您的系统中已经安装了 Python 3。
```sh
# 从官网下载：https://www.python.org/downloads/
```

### 2. 下载与安装

```bash
# 1. 克隆或下载项目代码
git clone https://github.com/HuangYuChuh/Zhi-Yi_Subtitle_Translator.git
cd Zhi-Yi_Subtitle_Translator

# 2. 创建并激活虚拟环境 (推荐)
python3 -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
# .\venv\Scripts\activate

# 3. 安装依赖库
pip install -r requirements.txt
```

### 3. 参数配置

```bash
# 1. 复制环境文件模板
cp .env.example .env

# 2. 编辑 .env 文件，填入您的 API Key 和 Base URL
# OPENAI_API_KEY="sk-..."
# OPENAI_API_BASE="https://api.openai.com/v1"
```

### 4. (可选) 生成AI术语库

本项目依赖一个外部的AI术语库。请先完成以下步骤来生成本地的术语表 `ai_terminology_glossary.json`。

```bash
# 1. 克隆AI术语库项目
git clone https://github.com/Social-Library/Artificial-Intelligence-Terminology-Database.git

# 2. 运行脚本生成本地术语表
python create_ai_glossary.py
```

### 5. 执行翻译

```bash
# (可选) 测试 API 是否连通
python test_api.py

# 翻译单个文件
python translate_srt.py your_subtitle.srt

# 批量翻译一个文件夹内的所有 srt 文件
python translate_srt_batch.py /path/to/your/subtitle_folder
```

翻译完成后，您会在同一个文件夹下看到一个名为 `*_cn.srt` 的新文件。

---

## 🎯 路线图 (Roadmap)

我们正在积极地改进项目，以下是近期的开发计划：

### 核心优化

-   [ ] **优化字幕对齐与完整性**: 解决翻译后字幕行数可能减少导致时间轴错位的问题。确保翻译后的字幕条目数与原文100%匹配。
-   [ ] **清理冗余文件与脚本**: 移除翻译过程中产生的临时文件，并考虑将核心修复逻辑整合到主脚本中，简化项目结构。

### 功能与体验增强

-   [ ] **扩充专业术语词典**: 持续将新的AI领域术语（如 `Cursor`, `Perplexity`）添加到术语库中。
-   [ ] **评估并合并翻译脚本**: 考虑将 `translate_srt.py` 的功能合并到 `translate_srt_batch.py` 中，提供单一、更强大的执行入口。

### 未来规划

-   [ ] **支持更多字幕格式**: 增加对 `.vtt`, `.ass` 等常见字幕格式的翻译支持。
-   [ ] **开发图形用户界面 (GUI)**: 创建一个简单的图形界面，让非技术用户也能轻松使用。

---

## 🤝 贡献指南 (Contributing)

欢迎任何形式的贡献！如果您有好的想法、功能建议，或者发现了 Bug，请随时通过 [Issues](https://github.com/HuangYuChuh/Zhi-Yi_Subtitle_Translator/issues) 提交。

如果您希望贡献代码，请遵循以下步骤：
1.  Fork 本仓库。
2.  创建您的新功能分支 (`git checkout -b feature/AmazingFeature`)。
3.  提交您的代码 (`git commit -m 'Add some AmazingFeature'`)。
4.  推送到您的分支 (`git push origin feature/AmazingFeature`)。
5.  提交一个 Pull Request。

---

## 📄 许可证 (License)

本项目使用 MIT 许可证。详细信息请查阅 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢 (Acknowledgements)

本项目的 AI 专业术语库功能，其数据源自于以下优秀的开源项目，特此感谢：

-   **[Artificial-Intelligence-Terminology-Database](https://github.com/Social-Library/Artificial-Intelligence-Terminology-Database)**: 一个由社区驱动的、全面的中英人工智能术语库。

我们在 `create_ai_glossary.py` 脚本中处理该数据，以生成项目所需的 `ai_terminology_glossary.json` 文件，从而极大地提升了字幕中专业词汇的翻译准确性。 