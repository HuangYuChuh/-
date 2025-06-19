# SRT 字幕翻译工具

这是一个 Python 脚本，可以使用兼容 OpenAI 格式的 API，将英文 SRT 字幕文件（`.srt`）自动翻译成中文。脚本会保留原始的时间轴，只翻译字幕文本内容。

## 功能

-   解析 SRT 文件格式。
-   逐条将英文字幕文本发送到 API 进行翻译。
-   保留原始字幕的时间码。
-   生成一个新的、包含中文翻译的 SRT 文件。

## 环境准备

1.  **Python 3**: 确保您的系统中已经安装了 Python 3。
    -   您可以从 [python.org](https://www.python.org/downloads/) 下载并安装。

## 设置步骤

1.  **下载代码**:
    将本项目的所有文件（`translate_srt.py`, `requirements.txt`）下载到您的本地文件夹中。

2.  **创建虚拟环境 (推荐)**:
    在项目文件夹中打开终端，运行以下命令来创建一个虚拟环境。这可以避免不同项目间的库依赖冲突。
    ```bash
    python3 -m venv venv
    ```
    激活虚拟环境：
    -   **macOS / Linux**: `source venv/bin/activate`
    -   **Windows**: `.\venv\Scripts\activate`

3.  **安装依赖**:
    在激活虚拟环境的终端中，运行以下命令来安装所有必需的库：
    ```bash
    pip install -r requirements.txt
    ```

4.  **配置 API 密钥**:
    项目提供了一个环境文件模板 `.env.example`。请将其复制一份并重命名为 `.env`：
    ```bash
    cp .env.example .env
    ```
    然后，打开新的 `.env` 文件，根据其中的中文注释填入您自己的 API 密钥和自定义配置。

## 如何使用

### 1. (可选) 测试 API 连接

在开始翻译前，建议先运行测试脚本，确保您的 API 配置和网络都正常。
```bash
python test_api.py
```
如果脚本成功输出 "连接成功！"，说明您的配置无误。如果报错，请根据错误提示检查您的 `.env` 文件和网络设置。

### 2. 运行翻译

将您需要翻译的 `.srt` 字幕文件放入项目文件夹中（例如 `my_movie.srt`）。

打开终端，并确保您已经激活了虚拟环境。运行翻译脚本：
```bash
python translate_srt.py my_movie.srt
```

脚本会开始逐条翻译字幕。翻译完成后，您会在同一个文件夹下看到一个名为 `my_movie_cn.srt` 的新文件，这就是翻译好的中文字幕文件。

### 自定义输出文件名

如果您想指定输出文件的名称或路径，可以使用 `-o` 或 `--output_file` 参数：
```bash
python translate_srt.py my_movie.srt -o /path/to/your/translated_subtitle.srt
```

### 自定义模型及参数

您可以在运行时通过命令行参数，或在 `.env` 文件中设置默认值，来配置翻译时使用的模型及参数。

**通过命令行参数配置 (运行时生效):**

-   **模型**: 使用 `-m` 或 `--model` 参数来指定模型，例如 `gpt-4o`。
    ```bash
    python translate_srt.py my_movie.srt -m gpt-4o
    ```
-   **温度 (Temperature)**: 使用 `-t` 或 `--temperature` 参数来调整翻译的随机性 (0.0 到 2.0 之间)。值越高，翻译越有创造性；值越低，翻译越固定。
    ```bash
    python translate_srt.py my_movie.srt -t 0.5
    ```

**通过 `.env` 文件配置 (设置默认值):**

您可以在 `.env` 文件中设置 `DEFAULT_MODEL` 和 `DEFAULT_TEMPERATURE` 来更改脚本的默认行为，这样就不必每次都输入命令行参数。

现在，您可以开始使用了！

---

## 致谢 (Acknowledgements)

本项目的AI专业术语库功能，其数据源自于以下优秀的开源项目，特此感谢：

-   **[Artificial-Intelligence-Terminology-Database](https://github.com/Social-Library/Artificial-Intelligence-Terminology-Database)**: 一个由社区驱动的、全面的中英人工智能术语库。

我们在 `create_ai_glossary.py` 脚本中处理该数据，以生成项目所需的 `ai_terminology_glossary.json` 文件，从而极大地提升了字幕中专业词汇的翻译准确性。 