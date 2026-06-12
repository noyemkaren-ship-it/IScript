from colorama import Fore, Style
from util.tokens import tokens
from util.Token import Token

commands = {
    "print ",
    "echo ",
    "fun ",
    "startS ",
    "get ",
    "post ",
    "put ",
    "delete ",
    "send ",
    "json "
}


def Lexer(token):
    found_lex = None
    for lex in commands:
        if lex in token:
            if found_lex is None or len(lex) > len(found_lex):
                found_lex = lex

    if found_lex:
        return found_lex, token
    return None


def CreateToken(token):
    result = Lexer(token)

    if result is None:
        spaces = token[:len(token) - len(token.lstrip())]
        tokens.append(Token(lex=None, content=token, indent=spaces))
    else:
        lex, line = result
        content_position = line.find(lex)
        indent = line[:content_position]
        content = line[content_position + len(lex):]
        clear_content = content.strip()
        tokens.append(Token(
            lex=lex,
            content=clear_content,
            indent=indent
        ))


def AntiBag(line, st: int):
    if "function" in line:
        print(Fore.RED + f"❌ ОШИБКА В СТРОКЕ {st}: Использован 'function', но принято писать 'fun'")
    if "alert" in line and "print" not in line:
        print(Fore.RED + f"❌ ОШИБКА В СТРОКЕ {st}: Использован 'alert', используйте 'print'")
    if "(" in line:
        if ")" not in line:
            print(Fore.YELLOW + f"⚠️ ПРЕДУПРЕЖДЕНИЕ В СТРОКЕ {st}: Возможно, не закрыта скобка")
    if line.count('"') % 2 != 0:
        print(Fore.YELLOW + f"⚠️ ПРЕДУПРЕЖДЕНИЕ В СТРОКЕ {st}: Непарное количество кавычек!")
    if "console.log" in line:
        print(Fore.YELLOW + f"💡 СОВЕТ В СТРОКЕ {st}: Вместо 'console.log' можно использовать 'echo'")
    print(Style.RESET_ALL, end="")