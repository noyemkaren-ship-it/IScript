from util.parserHtml import parser_html
from util.Lexer import CreateToken
from util.Parser import Parser
from util.Lexer import AntiBag
from util.dirs import create_dirs
from colorama import Fore
import sys
import os
from util.tokens import tokens
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

        if "initS" in full_content:
            with open(f"build/{bek_compilat}", "a") as fw:
                fw.write("const express = require('express');\n")
                fw.write("const app = express();\n")
                fw.write("const path = require('path');\n")
                fw.write("const ejs = require('ejs');\n")
                fw.write("const fs = require('fs');\n")   # ← ИСПРАВИЛ КАВЫЧКИ
                fw.write("app.use(express.static(path.join(__dirname, 'public')));\n")
                fw.write("app.use(express.urlencoded({ extended: true }));\n")
                fw.write("app.use(express.json());\n")
            print(
                "ГОТОВО INITS СРАБОТАЛО НО УБЕДИТЕСЬ ЧТО ВЫ ПИСАЛИ В ТЕРМИНАЛЕ npm init -y && npm install express && npm install ejs")
        elif "renderS" in full_content:
            with open(f"build/{bek_compilat}", "a") as fw:
                fw.write("function renderPage(file, data) {\n")
                fw.write("    const html = fs.readFileSync(__dirname + '/views/' + file, 'utf8');\n")
                fw.write("    return ejs.render(html, data);\n")
                fw.write("}\n")

        st = 0
        for line in full_content.split('\n'):
            st += 1

            if line.startswith("initS"):
                continue
            elif line.startswith("renderS"):
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