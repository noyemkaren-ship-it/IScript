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

input_file = sys.argv[1]
what_compilat = input_file
bek_compilat = os.path.splitext(os.path.basename(input_file))[0] + ".js"

print(Fore.BLUE + f"ИЩУ {what_compilat}")

# Остальной код без изменений...
with open(f"build/{bek_compilat}", "w") as f:
    f.write("// Compiler functions\n")
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

try:
    with open(f"script/{what_compilat}", "r") as f:
        st = 0
        for line in f:
            st += 1
            AntiBag(line, st)
            CreateToken(line)
except FileNotFoundError:
    print(Fore.RED + f"ФАЙЛ {what_compilat} НЕ НАЙДЕН")

Parser(bek_compilat)