from colorama import Fore
from util.tokens import tokens, peremem_nubers_name

def is_numeric(value):
    value = value.strip().strip('"').strip("'")
    try:
        float(value)
        return True
    except:
        return False



def Parser(js_name):
    backtic = False
    skobki = False
    with open(f"build/{js_name}", "a") as f:
        for token in tokens:
            if token.lex is None:
                if "%=" in token.content and "%=%" not in token.content:
                    peremen, content = token.content.split('%=')
                    value = content.strip()
                    f.write(f'let {peremen} = {value};\n')
                    if is_numeric(value):
                        peremem_nubers_name.append(peremen.strip())
                    continue
                if "#=" in token.content and "%=%" not in token.content:
                    peremen, content = token.content.split('#=')
                    value = content.strip()
                    f.write(f'const {peremen} = {value};\n')
                    continue
                elif "^=" in token.content:
                    peremen, content = token.content.split('^=')
                    peremen = peremen.strip()
                    value = content.strip()

                    if peremen in peremem_nubers_name:
                        if is_numeric(value):
                            f.write(f'{peremen} = {value};\n')
                        else:
                            print(Fore.RED + f"❌ ОШИБКА: Переменная {peremen} ЧИСЛОВАЯ, нельзя присвоить '{value}'!")
                    else:
                        print(Fore.YELLOW + f"⚠️ ПРЕДУПРЕЖДЕНИЕ: Переменная {peremen} не объявлена как числовая!")
                    continue

                elif "%=%" in token.content:
                    peremen, content = token.content.split('%=%')
                    value = content.strip()
                    f.write(f'let {peremen.strip()} = {value};\n')
                    f.write(f'console.log({peremen.strip()});\n')

                    if is_numeric(value):
                        peremem_nubers_name.append(peremen.strip())
                    continue

                elif "typeC " in token.content:
                    f.write("function " + token.content[6:] + "\n")
                    continue
                elif "TypeLego " in token.content:
                    content = token.content[9:].strip()
                    if " *=* " in content:
                        class_name, fields_str = content.split(" *=* ")
                        class_name = class_name.strip()
                        fields = [f.strip() for f in fields_str.split("%")]
                        f.write(f"{token.indent}function {class_name}({', '.join(fields)}) {{\n")
                        for field in fields:
                            f.write(f"{token.indent}    this.{field} = {field};\n")
                        f.write(f"{token.indent}}}\n")
                    continue
                if token.content.strip().endwith("`"):
                    if token.content.count("`") < 2 and backtic == False:
                        backtic = True
                    elif token.content.count("`") < 2 and backtic:
                        backtic = False
                if token.content.strip().endwith("(") and skobki == False and backtic == False:
                    skobki = True
                elif token.content.strip().endwith(")") and skobki == True and backtic == False:
                    skobki = False

                if "if" in token.content or "elif" in token.content or "else" in token.content or "while" in token.content or "for" in token.content or "function" in token.content or "fun" or token.content.strip().endswith("{") or "(" in token.content or backtic or skobki:
                    f.write(f"{token.content}\n")
                    continue
                elif token.content.strip().endswith("n^") or token.content.strip().endswith("^n"):
                    f.write(f"{token.content.replace("n^", "")}\n")
                    continue
                else:
                    f.write(f"{token.content};\n");
                    print(f"В строке {token.content} была автоматический добавлена ; если я поставил лишнее то просто в конец добавьте n^")
                continue

            if "echo " in token.lex:
                content = token.content.strip()
                f.write(f'{token.indent}console.log({content});\n')
                continue
            elif "print " in token.lex:
                content = token.content.strip()
                f.write(f'{token.indent}alert({content});\n')
                continue
            elif "startS " in token.lex:
                server_port = token.content.scrip()
                f.write(f"app.listen({server_port}, () => " + "{" + "\n")
                f.write(f"  console.log('🚀ЗАПУСК СЕРВЕРА🚀');\n")
                f.write(f"  console.log('\x1b[34m Сервер запущен на порт ->{server_port} \x1b[0m');\n")
                f.write("});\n")
                continue
            elif "fun " in token.lex:
                f.write(f"{token.indent}function {token.content}\n")
                continue