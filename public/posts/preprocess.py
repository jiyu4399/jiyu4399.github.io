import re
import subprocess
import os

def execute_python_code(code):
    result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
    return result.stdout

def preprocess_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = re.compile(r'{{< python >}}(.*?){{< /python >}}', re.DOTALL)
    
    def replace_code_block(match):
        code = match.group(1).strip()
        result = execute_python_code(code)
        return f'```\n{result}\n```'

    new_content = pattern.sub(replace_code_block, content)
    
    output_file = file_path.replace('.md', '_processed.md')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f'Processed {file_path} -> {output_file}')

if __name__ == "__main__":
    content_dir = 'content/posts'
    for filename in os.listdir(content_dir):
        if filename.endswith('.md'):
            preprocess_markdown(os.path.join(content_dir, filename))
