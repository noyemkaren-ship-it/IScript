from util.parserHtml import parser_html
from util.Lexer import CreateToken
from util.Parser import Parser
from util.Lexer import AntiBag
from util.dirs import create_dirs
from colorama import Fore
import sys
import os

print(Fore.GREEN + "Создание папок")
create_dirs()
if len(sys.argv) < 2:
    print(Fore.RED + "Укажите файл для компиляции: iscript main.i")
    sys.exit(1)
html_file_name = ""

input_file = sys.argv[1]
what_compilat = input_file
bek_compilat = os.path.splitext(os.path.basename(input_file))[0] + ".js"

html_mode = False

print(Fore.BLUE + f"ИЩУ {what_compilat}")

with open(f"build/{bek_compilat}", "w") as file:
    file.write("// Compiler\n")

print("WARNING")
print("ПРЕДУПРЕЖДЕНИЕ ЗАРАНЕЕ ; НЕ НУНЖЫ ВООБЩЕ !")

try:
    with open(f"script/{what_compilat}", "r") as f:
        # Читаем ВЕСЬ файл ОДИН раз
        full_content = f.read()

        # Проверяем AppHtml/AppApend
        if "AppHtml" in full_content or "AppApend" in full_content:
            with open(f"build/{bek_compilat}", "a") as fw:
                fw.write("import { writeFile, readFile, appendFile } from 'node:fs/promises';\n")
                fw.write("import { join } from 'node:path';\n")
                fw.write(" \n")
                fw.write("async function AppHtml(file, code) {\n")
                fw.write("   const filePath = join(process.cwd(), file);\n")
                fw.write("   await writeFile(filePath, code, 'utf-8');")
                fw.write("   console.log('Файл успешно создан.');\n")
                fw.write("}\n")
                fw.write(" \n")
                fw.write("async function AppApend(file, code) {\n")
                fw.write("   const filePath = join(process.cwd(), file);\n")
                fw.write("   await appendFile(filePath, code, 'utf-8');\n")
                fw.write("   console.log('Файл успешно обновлен.');\n")
                fw.write("}\n")

        # Проверяем initS
        if "initS" in full_content:
            with open(f"build/{bek_compilat}", "a") as fw:
                fw.write("const express = require('express');\n")  # ← убрал двойной const
                fw.write("const app = express();\n")
                fw.write("const path = require('path');\n")
            print("Константы express и app и path были созданы автоматический!")

        # Обрабатываем построчно
        st = 0
        for line in full_content.split('\n'):
            st += 1

            if line.startswith("initS"):
                continue
            elif line.startswith("html "):
                html_mode = True
                html_file_name = line[len("html "):].strip()
                continue
            elif line.startswith("html-end"):
                html_mode = False
                continue
            elif html_mode:
                parser_html(html_file_name, line)
            else:
                AntiBag(line, st)
                CreateToken(line)
except FileNotFoundError:
    print(Fore.RED + f"ФАЙЛ {what_compilat} НЕ НАЙДЕН")

Parser(bek_compilat)
import re
def fix_compiled_file(js_name):
    filepath = f"build/{js_name}"

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        if not stripped:
            fixed_lines.append('')
            continue
        if stripped and not stripped.endswith(('{', '}', ';', ':')):
            if not any(keyword in stripped for keyword in ['if', 'else', 'for', 'while', 'function', '=>']):
                if not stripped.startswith(('.', '(', ')', '[', ']')):
                    line = line.rstrip() + ';'

        fixed_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))

fix_compiled_file(bek_compilat)