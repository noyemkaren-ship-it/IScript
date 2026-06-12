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
        st = 0
        if "AppHtml" in f.read() or "AppApend" in f.read():
            with open(f"build/{bek_compilat}", "a") as f:
                f.write("import { writeFile, readFile, appendFile } from 'node:fs/promises';\n")
                f.write("import { join } from 'node:path';\n")
                f.write(" \n")
                f.write("async function AppHtml(file, code) {\n")
                f.write("   const filePath = join(process.cwd(), file);\n")
                f.write("   await writeFile(filePath, code, 'utf-8');")
                f.write("   console.log('Файл успешно создан.');\n")
                f.write("}\n")
                f.write(" \n")
                f.write("async function AppApend(file, code) {\n")
                f.write("   const filePath = join(process.cwd(), file);\n")
                f.write("   await appendFile(filePath, code, 'utf-8');\n")
                f.write("   console.log('Файл успешно обновлен.');\n")
                f.write("}\n")

        if "initS" in f.read():
            with open(f"build/{bek_compilat}", "a") as fule:
                fule.write("const const express = require('express');\n")
                fule.write("const app = express();\n")
                fule.write("const path = require('path');\n")
            print("Константы express и app и path были созданы автоматический!")

        for line in f:
            st += 1

            if line.startswith("initS"):
                continue
            elif line.startswith("html "):
                html_mode = True
                html_file_name = line[len("html "):].strip()
                with open(f"build/{bek_compilat}", "w") as fule:
                    fule.write("\n")
                continue
            elif line.startswith("html-end"):
                html_mode = False
                continue
            elif html_mode:
                parser_html(html_file_name, line)
            AntiBag(line, st)
            CreateToken(line)
except FileNotFoundError:
    print(Fore.RED + f"ФАЙЛ {what_compilat} НЕ НАЙДЕН")

Parser(bek_compilat)