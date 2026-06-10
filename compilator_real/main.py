from Lexer import CreateToken
from Parser import Parser
from Lexer import AntiBag
from dirs import create_dirs
from colorama import Fore

create_dirs()

print(Fore.BLUE + "ИЩУ main.i В ПАПКЕ script")

with open("build/main.js", "w") as f:
    f.write("// Compiler\n")

try:
    with open("script/main.i", "r") as f:
        st = 0
        for line in f:
            st += 1
            AntiBag(line, st)
            CreateToken(line)
except FileNotFoundError:
    print(Fore.RED + "ФАЙЛ main.i НЕ НАЙДЕН")

Parser()