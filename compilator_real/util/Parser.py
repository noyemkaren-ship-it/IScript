from colorama import Fore
from util.tokens import tokens, peremem_nubers_name

from util.commnds import ECHO_LOGIC

from util.commnds import RED_ECHO_LOGIC

from util.commnds import GREEN_ECHO_LOGIC

from util.commnds import BLUE_ECHO_LOGIC


def is_numeric(value):
    value = value.strip().strip('"').strip("'")
    try:
        float(value)
        return True
    except ValueError:
        return False


def Parser(js_name):
    backtic = False
    skobki = False
    with open(f"build/{js_name}", "a", encoding="utf-8") as f:
        for token in tokens:
            if not token.content or token.content.strip() == "":
                continue

            indent = token.indent if hasattr(token, 'indent') and token.indent else ''

            if token.lex is None:
                if "%=" in token.content and "%=%" not in token.content:
                    original_content = token.content
                    if " %= " in original_content:
                        peremen, content = original_content.split(' %= ', 1)
                    else:
                        peremen, content = original_content.split('%=', 1)

                    value = content.strip()
                    peremen_clean = peremen.strip()

                    f.write(f'{indent}let {peremen_clean} = {value};\n')

                    if is_numeric(value):
                        peremem_nubers_name.append(peremen_clean)
                    continue

                elif "#=" in token.content and "%=%" not in token.content:
                    original_content = token.content
                    if " #= " in original_content:
                        peremen, content = original_content.split(' #= ', 1)
                    else:
                        peremen, content = original_content.split('#=', 1)

                    value = content.strip()
                    peremen_clean = peremen.strip()

                    f.write(f'{indent}const {peremen_clean} = {value};\n')
                    continue

                elif "^=" in token.content:
                    original_content = token.content
                    if " ^= " in original_content:
                        peremen, content = original_content.split(' ^= ', 1)
                    else:
                        peremen, content = original_content.split('^=', 1)

                    peremen = peremen.strip()
                    value = content.strip()

                    if peremen in peremem_nubers_name:
                        if is_numeric(value):
                            f.write(f'{indent}{peremen} = {value};\n')
                        else:
                            print(Fore.RED + f"❌ ОШИБКА: Переменная {peremen} ЧИСЛОВАЯ, нельзя присвоить '{value}'!")
                            continue
                    else:
                        f.write(f'{indent}{peremen} = {value};\n')
                    continue

                elif "%=%" in token.content:
                    original_content = token.content
                    if " %=% " in original_content:
                        peremen, content = original_content.split(' %=% ', 1)
                    else:
                        peremen, content = original_content.split('%=%', 1)

                    value = content.strip()
                    peremen_clean = peremen.strip()

                    f.write(f'{indent}let {peremen_clean} = {value};\n')
                    f.write(f'{indent}console.log({peremen_clean});\n')

                    if is_numeric(value):
                        peremem_nubers_name.append(peremen_clean)
                    continue

                elif "typeC " in token.content:
                    func_def = token.content[6:].strip()
                    if not func_def.endswith('{'):
                        f.write(f"{indent}function {func_def} {{\n")
                    else:
                        f.write(f"{indent}function {func_def}\n")
                    continue

                elif "TypeLego " in token.content:
                    print("Вижу TypeLego")
                    content = token.content[9:].strip()
                    if " *=* " in content:
                        class_name, fields_str = content.split(" *=* ", 1)
                        class_name = class_name.strip()
                        fields = [f.strip() for f in fields_str.split("%")]
                        f.write(f"{indent}function {class_name}({', '.join(fields)}) {{\n")
                        for field in fields:
                            f.write(f"{indent}    this.{field} = {field};\n")
                        f.write(f"{indent}}}\n")
                    continue

                if "`" in token.content.strip():
                    clean = token.content.strip()
                    if clean.count("`") % 2 == 1:
                        backtic = not backtic

                if "(" in token.content.strip() and not backtic:
                    skobki = True
                if ")" in token.content.strip() and not backtic:
                    skobki = False

                if any(keyword in token.content for keyword in ["if", "elif", "else", "while", "for", "return"]) or \
                        "function" in token.content or \
                        "fun " in token.content or \
                        token.content.strip().endswith(("{", "}")) or \
                        backtic or skobki:
                    if token.content.strip().endswith(("{", "}")):
                        f.write(f"{indent}{token.content.strip()}\n")
                    else:
                        f.write(f"{indent}{token.content}\n")
                    continue
                elif token.content.strip().endswith(("n^", "^n")):
                    cleaned = token.content.replace('n^', '').replace('^n', '')
                    f.write(f"{indent}{cleaned}\n")
                    continue

                else:
                    content = token.content.strip()
                    if content:
                        f.write(f"{indent}{content};\n")
                    continue

            if token.lex.strip().startwith("echo"):
                if token.lex and "echo" in token.lex and "echo: r" not in token.lex and "echo: g" not in token.lex:
                    print("Вижу echo")
                    content = token.content.strip()
                    f.write(f'{ECHO_LOGIC(indent, content)}')
                    continue

                elif token.lex and "echo: r" in token.lex:
                    content = token.content.strip()
                    f.write(f'{RED_ECHO_LOGIC(indent, content)}')
                    continue

                elif token.lex and "echo: g" in token.lex:
                    content = token.content.strip()
                    f.write(f'{GREEN_ECHO_LOGIC(indent, content)}')
                    continue

                elif token.lex and "echo: b" in token.lex:
                    content = token.content.strip()
                    f.write(f"{BLUE_ECHO_LOGIC(indent, content)}")
                    continue

            elif token.lex and "get" in token.lex:
                path = token.content.strip().rstrip('{').strip()
                f.write(f"{indent}app.get({path}, (req, res) => {{\n")
                continue

            elif token.lax.strip().startwith("p"):
                if token.lex and "post" in token.lex:
                    path = token.content.strip().rstrip('{').strip()
                    f.write(f"{indent}app.post({path}, (req, res) => {{\n")
                    continue

                elif token.lex and "put" in token.lex:
                    path = token.content.strip().rstrip('{').strip()
                    f.write(f"{indent}app.put({path}, (req, res) => {{\n")
                    continue
                elif token.lex and "print" in token.lex:
                    print("Вижу print")
                    content = token.content.strip()
                    if content:
                        f.write(f'{indent}alert({content});\n')
                    continue


            elif token.lex and "delete" in token.lex:
                path = token.content.strip().rstrip('{').strip()
                f.write(f"{indent}app.delete({path}, (req, res) => {{\n")
                continue

            elif token.lex and "send" in token.lex:
                content = token.content.strip()
                f.write(f"{indent}    res.send({content});\n")
                continue

            elif token.lex and "json" in token.lex:
                print("Вижу json")
                content = token.content.strip()
                f.write(f"{indent}    res.json({content});\n")
                continue


            elif token.lex and "startS" in token.lex:
                print("Увидило startS")
                server_port = token.content.strip()
                f.write(f"{indent}app.listen({server_port}, () => {{\n")
                f.write(f"{indent}  console.log('🚀 ЗАПУСК СЕРВЕРА 🚀');\n")
                f.write(f"{indent}  console.log('\\x1b[34m Сервер запущен на порту -> {server_port} \\x1b[0m');\n")
                f.write(f"{indent}  console.log('\\x1b[34m Можно найти по сыллку -> http://localhost:{server_port} \\x1b[0m');\n")
                f.write(f"{indent}}});\n")
                continue

            elif token.lex and "fun" in token.lex:
                print("Создания fun")
                content = token.content.strip()
                func_body = content.rstrip('{').strip()
                f.write(f"{indent}function {func_body} {{\n")
                continue

    tokens.clear()
    peremem_nubers_name.clear()