from colorama import Fore, Style

from tokens import tokens
from Token import Token

commands = {
    "print ",
    "echo ",
    "fun "
}


def Lexer(token):
    for lex in commands:
        if lex in token:
            return lex, token
    return None


def CreateToken(token):
    result = Lexer(token)

    if result is None:
        tokens.append(Token(lex=None, content=token))
    else:
        lex, line = result
        content_position = line.find(lex)
        indent = line[:content_position]
        clear_content = line[content_position + len(lex):].strip()
        tokens.append(Token(
            lex=indent + lex,
            content=clear_content,
            indent=indent
        ))


def AntiBag(line, st: int):
    if "function" in line:
        print(Fore.RED + f"❌ ОШИБКА В СТРОКЕ {st}: Использован 'function', но принято писать 'fun'")
    if "alert" in line and "print" not in line:  # Чтобы не срабатывало на самом print
        print(Fore.RED + f"❌ ОШИБКА В СТРОКЕ {st}: Использован 'alert', используйте 'print'")
    if "(" in line:
        if ")" not in line:
            print(Fore.YELLOW + f"⚠️ ПРЕДУПРЕЖДЕНИЕ В СТРОКЕ {st}: Возможно, не закрыта скобка")
    if line.count('"') % 2 != 0:
        print(Fore.YELLOW + f"⚠️ ПРЕДУПРЕЖДЕНИЕ В СТРОКЕ {st}: Непарное количество кавычек!")
    if "console.log" in line:
        print(Fore.YELLOW + f"💡 СОВЕТ В СТРОКЕ {st}: Вместо 'console.log' можно использовать 'echo'")
    print(Style.RESET_ALL, end="")