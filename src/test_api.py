import os
from openai import OpenAI
from dotenv import load_dotenv

def test_llm_connection():
    """
    Tests the connection to the OpenAI-compatible API.
    """
    print("正在加载 .env 文件中的环境变量...")
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE")
    model_name = os.getenv("DEFAULT_MODEL")

    if not api_key or "your-key-here" in api_key:
        print("错误：OPENAI_API_KEY 未设置或仍为默认值。")
        print("请创建 .env 文件并填入您有效的 API 密钥。")
        return

    print("已成功加载 API 密钥和 Base URL。")
    print(f"使用的 API Base URL: {base_url}")
    print(f"将要测试的模型: {model_name if model_name else 'API 默认'}")

    try:
        print("\n正在初始化 OpenAI 客户端...")
        client = OpenAI(api_key=api_key, base_url=base_url)

        print("正在向模型发送测试消息...")
        
        create_params = {
            "messages": [
                {"role": "system", "content": "你是一个有用的助手。"},
                {"role": "user", "content": "你好！请用中文回答'你好'来确认通信正常。"}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        if model_name:
            create_params['model'] = model_name

        response = client.chat.completions.create(**create_params)

        print("\n--- API 响应 ---")
        print(response.choices[0].message.content)
        print("\n--------------------")
        print("\n连接成功！API 调用已完成。")

    except Exception as e:
        print("\n--- 发生错误 ---")
        print(f"无法连接到 API。错误信息: {e}")
        print("\n-------------------------")
        print("请检查以下几点：")
        print("1. 您的网络连接以及任何代理或防火墙设置。")
        print("2. .env 文件中的 OPENAI_API_KEY 是否正确。")
        print("3. .env 文件中的 OPENAI_API_BASE URL 是否正确且可以访问。")
        print("4. .env 文件中的 DEFAULT_MODEL 名称是否被您的 API 服务所支持。")

if __name__ == "__main__":
    test_llm_connection() 