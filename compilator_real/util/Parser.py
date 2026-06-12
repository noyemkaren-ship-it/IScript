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
                        f.write(f'{peremen} = {value};\n')  # ← работает для всего
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

                if token.content.strip().endswith("`"):
                    if token.content.count("`") < 2 and backtic == False:
                        backtic = True
                    elif token.content.count("`") < 2 and backtic:
                        backtic = False

                if token.content.strip().endswith("(") and skobki == False and backtic == False:
                    skobki = True
                elif token.content.strip().endswith(")") and skobki == True and backtic == False:
                    skobki = False

                # ← ИСПРАВЛЕНО: "fun " вместо "fun"
                if "if" in token.content or "elif" in token.content or "else" in token.content or "while" in token.content or "for" in token.content or "function" in token.content or "fun " in token.content or token.content.strip().endswith(
                        "{") or "(" in token.content or backtic or skobki:
                    f.write(f"{token.content}\n")
                    continue

                elif token.content.strip().endswith("n^") or token.content.strip().endswith("^n"):
                    f.write(f"{token.content.replace('n^', '').replace('^n', '')}\n")
                    continue

                else:
                    f.write(f"{token.content};\n")
                    continue

            # ===== ОСНОВНЫЕ КОМАНДЫ =====

            if "echo " in token.lex:
                content = token.content.strip()
                f.write(f'{token.indent}console.log({content});\n')
                continue

            elif "get " in token.lex:
                path = token.content.strip()
                f.write(f"{token.indent}app.get({path}, (req, res) => {{\n")
                continue

            elif "post " in token.lex:
                path = token.content.strip()
                f.write(f"{token.indent}app.post({path}, (req, res) => {{\n")
                continue

            elif "put " in token.lex:
                path = token.content.strip()
                f.write(f"{token.indent}app.put({path}, (req, res) => {{\n")
                continue

            elif "delete " in token.lex:
                path = token.content.strip()
                f.write(f"{token.indent}app.delete({path}, (req, res) => {{\n")
                continue

            elif "send " in token.lex:
                content = token.content.strip()
                f.write(f"{token.indent}    res.send({content})\n")
                continue

            elif "json " in token.lex:
                content = token.content.strip()
                f.write(f"{token.indent}    res.json({content})\n")
                continue

            elif "print " in token.lex:
                content = token.content.strip()
                f.write(f'{token.indent}alert({content});\n')
                continue

            elif "startS " in token.lex:
                server_port = token.content.strip()  # ← ИСПРАВЛЕНО: strip вместо scrip
                f.write(f"app.listen({server_port}, () => {{\n")
                f.write(f"  console.log('🚀 ЗАПУСК СЕРВЕРА 🚀');\n")
                f.write(f"  console.log('\\x1b[34m Сервер запущен на порту -> {server_port} \\x1b[0m');\n")
                f.write("});\n")
                continue

            elif "fun " in token.lex:
                f.write(f"{token.indent}function {token.content}\n")
                continue