import os
import re
import argparse
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", 0.7))

# --- SRT Parsing and Generation ---

class Subtitle:
    """Represents a single subtitle block."""
    def __init__(self, index, start_time, end_time, text):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def __str__(self):
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.text}"

def parse_srt(file_path):
    """Parses an SRT file and returns a list of Subtitle objects."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

    subtitle_blocks = content.strip().split('\n\n')
    subtitles = []
    
    for block in subtitle_blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            try:
                index = int(lines[0])
                time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', lines[1])
                if time_match:
                    start_time, end_time = time_match.groups()
                    text = '\n'.join(lines[2:])
                    subtitles.append(Subtitle(index, start_time, end_time, text))
            except (ValueError, IndexError):
                print(f"Skipping malformed block:\n{block}")
                continue
                
    return subtitles

def write_srt(file_path, subtitles):
    """Writes a list of Subtitle objects to an SRT file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for sub in subtitles:
            f.write(str(sub) + '\n\n')

# --- Intelligent Batch Translation ---

def create_batch_groups(subtitles, batch_size=10, max_chars=3000):
    """
    Groups subtitles into batches for context-aware translation.
    
    Args:
        subtitles: List of Subtitle objects
        batch_size: Maximum number of subtitles per batch
        max_chars: Maximum characters per batch to avoid API limits
    
    Returns:
        List of subtitle batches
    """
    batches = []
    current_batch = []
    current_chars = 0
    
    for subtitle in subtitles:
        subtitle_chars = len(subtitle.text)
        
        # If adding this subtitle would exceed limits, start a new batch
        if (len(current_batch) >= batch_size or 
            current_chars + subtitle_chars > max_chars) and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_chars = 0
        
        current_batch.append(subtitle)
        current_chars += subtitle_chars
    
    # Add the last batch if it's not empty
    if current_batch:
        batches.append(current_batch)
    
    return batches

def translate_batch(batch, client, model_name, temperature, context_memory=""):
    """
    Translates a batch of subtitles with context awareness.
    
    Args:
        batch: List of Subtitle objects to translate
        client: OpenAI client
        model_name: Model to use for translation
        temperature: Temperature for translation
        context_memory: Previous context to maintain consistency
    
    Returns:
        Tuple of (translated_texts, updated_context_memory)
    """
    if not batch:
        return [], context_memory
    
    # Prepare the input for batch translation
    input_texts = []
    for i, subtitle in enumerate(batch, 1):
        input_texts.append(f"{i}. {subtitle.text}")
    
    batch_text = "\n".join(input_texts)
    
    # Create context-aware prompt
    system_prompt = """你是一位专业的字幕翻译专家。请按照以下要求翻译字幕：

1. 保持翻译的一致性和连贯性
2. 确保专有名词、人名、地名的翻译统一
3. 保持对话的自然流畅
4. 保留原文的语气和情感
5. 返回格式必须与输入格式完全一致（数字编号 + 翻译内容）

请将以下英文字幕翻译成简体中文，保持编号不变："""

    user_prompt = batch_text
    if context_memory:
        user_prompt = f"上下文参考（保持翻译一致性）：\n{context_memory}\n\n当前待翻译内容：\n{batch_text}"
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
        )
        
        translated_content = response.choices[0].message.content.strip()
        
        # Parse the translated content
        translated_texts = []
        lines = translated_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and re.match(r'^\d+\.', line):
                # Remove the number prefix and get the translated text
                translated_text = re.sub(r'^\d+\.\s*', '', line)
                translated_texts.append(translated_text)
        
        # Update context memory with recent translations for consistency
        recent_context = "\n".join(translated_texts[-3:])  # Keep last 3 translations as context
        updated_context_memory = recent_context
        
        # Ensure we have the right number of translations
        while len(translated_texts) < len(batch):
            translated_texts.append(f"[Translation Error for subtitle {len(translated_texts) + 1}]")
        
        return translated_texts[:len(batch)], updated_context_memory
        
    except Exception as e:
        print(f"An error occurred during batch translation: {e}")
        error_texts = [f"[Translation Error: {sub.text}]" for sub in batch]
        return error_texts, context_memory

def translate_with_glossary(subtitles, client, model_name, temperature, glossary_file=None):
    """
    Advanced translation with optional glossary support for consistent terminology.
    
    Args:
        subtitles: List of Subtitle objects
        client: OpenAI client
        model_name: Model name
        temperature: Temperature setting
        glossary_file: Optional path to JSON file with term translations
    
    Returns:
        List of translated Subtitle objects
    """
    # Load glossary if provided
    glossary = {}
    if glossary_file and os.path.exists(glossary_file):
        try:
            with open(glossary_file, 'r', encoding='utf-8') as f:
                glossary = json.load(f)
            print(f"Loaded glossary with {len(glossary)} terms from {glossary_file}")
        except Exception as e:
            print(f"Warning: Could not load glossary file {glossary_file}: {e}")
    
    # Create batches
    batches = create_batch_groups(subtitles)
    print(f"Created {len(batches)} batches for translation")
    
    translated_subtitles = []
    context_memory = ""
    
    # Add glossary to initial context if available
    if glossary:
        glossary_context = "术语对照表：\n"
        for en_term, cn_term in glossary.items():
            glossary_context += f"- {en_term} → {cn_term}\n"
        context_memory = glossary_context
    
    for i, batch in enumerate(batches):
        print(f"Translating batch {i+1}/{len(batches)} ({len(batch)} subtitles)...")
        
        translated_texts, context_memory = translate_batch(
            batch, client, model_name, temperature, context_memory
        )
        
        # Create translated subtitle objects
        for j, (original_sub, translated_text) in enumerate(zip(batch, translated_texts)):
            translated_sub = Subtitle(
                index=original_sub.index,
                start_time=original_sub.start_time,
                end_time=original_sub.end_time,
                text=translated_text
            )
            translated_subtitles.append(translated_sub)
    
    return translated_subtitles

# --- Main Logic ---

def main():
    """Main function to run the intelligent SRT translation script."""
    parser = argparse.ArgumentParser(description='Intelligently translate English SRT subtitles to Chinese with context awareness.')
    parser.add_argument('input_file', help='The path to the input SRT file.')
    parser.add_argument('-o', '--output_file', help='The path for the output translated SRT file. Defaults to [input_file]_cn.srt')
    parser.add_argument('-m', '--model', default=DEFAULT_MODEL, help=f'The model to use for translation. Defaults to {DEFAULT_MODEL}.')
    parser.add_argument('-t', '--temperature', type=float, default=DEFAULT_TEMPERATURE, help=f'The temperature for translation. Defaults to {DEFAULT_TEMPERATURE}.')
    parser.add_argument('-g', '--glossary', help='Optional JSON glossary file for consistent terminology translation.')
    parser.add_argument('-b', '--batch_size', type=int, default=10, help='Number of subtitles per batch (default: 10).')
    
    args = parser.parse_args()

    input_path = args.input_file
    if args.output_file:
        output_path = args.output_file
    else:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_cn{ext}"

    if not API_KEY:
        print("Error: OPENAI_API_KEY environment variable not found.")
        print("Please create a .env file and add your API key.")
        return

    print("=== 智能字幕翻译工具 (SRT AI-Translator) ===")
    print(f"输入文件: {input_path}")
    print(f"输出文件: {output_path}")
    print(f"使用模型: {args.model}")
    print(f"翻译温度: {args.temperature}")
    print(f"批处理大小: {args.batch_size}")
    if args.glossary:
        print(f"术语词典: {args.glossary}")
    print()

    print("Initializing OpenAI client...")
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    print(f"Parsing SRT file: {input_path}")
    original_subtitles = parse_srt(input_path)
    
    if not original_subtitles:
        print("Could not parse SRT file. Exiting.")
        return

    print(f"Found {len(original_subtitles)} subtitle entries to translate.")
    print("Starting intelligent batch translation with context awareness...")
    
    translated_subtitles = translate_with_glossary(
        original_subtitles, 
        client, 
        args.model, 
        args.temperature,
        args.glossary
    )

    print(f"Writing translated subtitles to: {output_path}")
    write_srt(output_path, translated_subtitles)
    
    print("Translation complete!")
    print(f"Translated {len(translated_subtitles)} subtitles with improved context awareness.")

if __name__ == "__main__":
    main() 