import os
import re
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Make sure you have OPENAI_API_KEY and OPENAI_API_BASE in your .env file
# or as environment variables.
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

# --- Translation ---

def translate_text(text, client, model_name, temperature):
    """Translates a single piece of text using the OpenAI API."""
    if not text.strip():
        return ""
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate the following English subtitle text to Simplified Chinese. Keep the original meaning and tone."},
                {"role": "user", "content": text}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"[Translation Error: {text}]"

# --- Main Logic ---

def main():
    """Main function to run the SRT translation script."""
    parser = argparse.ArgumentParser(description='Translate English SRT subtitles to Chinese.')
    parser.add_argument('input_file', help='The path to the input SRT file.')
    parser.add_argument('-o', '--output_file', help=f'The path for the output translated SRT file. Defaults to [input_file]_cn.srt')
    parser.add_argument('-m', '--model', default=DEFAULT_MODEL, help=f'The model to use for translation. Defaults to the value of DEFAULT_MODEL in .env or {DEFAULT_MODEL}.')
    parser.add_argument('-t', '--temperature', type=float, default=DEFAULT_TEMPERATURE, help=f'The temperature for translation. Defaults to the value of DEFAULT_TEMPERATURE in .env or {DEFAULT_TEMPERATURE}.')
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

    print("Initializing OpenAI client...")
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    print(f"Parsing SRT file: {input_path}")
    original_subtitles = parse_srt(input_path)
    
    if not original_subtitles:
        print("Could not parse SRT file. Exiting.")
        return

    print(f"Found {len(original_subtitles)} subtitle entries to translate.")
    
    translated_subtitles = []
    for i, sub in enumerate(original_subtitles):
        print(f"Translating subtitle {sub.index} ({i+1}/{len(original_subtitles)})...")
        translated_text = translate_text(sub.text, client, args.model, args.temperature)
        
        translated_sub = Subtitle(
            index=sub.index,
            start_time=sub.start_time,
            end_time=sub.end_time,
            text=translated_text
        )
        translated_subtitles.append(translated_sub)

    print(f"Writing translated subtitles to: {output_path}")
    write_srt(output_path, translated_subtitles)
    
    print("Translation complete!")

if __name__ == "__main__":
    main() 