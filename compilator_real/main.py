from util.Lexer import CreateToken
from util.Parser import Parser
from util.Lexer import AntiBag
from util.dirs import create_dirs
from colorama import Fore
create_dirs()
what_compilat = str(input("Названия ФАЙЛА в script: "))
bek_compilat = str(input("Названия ФАЙЛА который создаться в  build  вы хотите скомпилировать: "))
print(Fore.BLUE + f"ИЩУ {what_compilat} В ПАПКЕ script")

with open(f"build/{bek_compilat}", "w") as f:
    f.write("// Compiler\n")

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