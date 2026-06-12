from colorama import Fore
from util.tokens import tokens, peremem_nubers_name


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
            if token.content.strip() == "":
                continue

            if token.lex is None:
                if "%=" in token.content and "%=%" not in token.content:
                    peremen, content = token.content.split('%=', 1)
                    value = content.strip()  # Делаем strip для чистоты значения
                    peremen_clean = peremen.strip()  # Но имя переменной чистим

                    # Проверяем, не является ли значение вызовом функции
                    if '(' in value and ')' in value:
                        f.write(f'let {peremen_clean} = {value};\n')
                    else:
                        f.write(f'let {peremen_clean} = {value};\n')

                    if is_numeric(value):
                        peremem_nubers_name.append(peremen_clean)
                    continue

                if "#=" in token.content and "%=%" not in token.content:
                    peremen, content = token.content.split('#=', 1)
                    value = content.strip()
                    peremen_clean = peremen.strip()

                    if '(' in value and ')' in value:
                        f.write(f'const {peremen_clean} = {value};\n')
                    else:
                        f.write(f'const {peremen_clean} = {value};\n')
                    continue

                elif "^=" in token.content:
                    peremen, content = token.content.split('^=', 1)
                    peremen = peremen.strip()
                    value = content.strip()
                    if peremen in peremem_nubers_name:
                        if is_numeric(value):
                            f.write(f'{peremen} = {value};\n')
                        else:
                            print(Fore.RED + f"❌ ОШИБКА: Переменная {peremen} ЧИСЛОВАЯ, нельзя присвоить '{value}'!")
                            continue
                    else:
                        f.write(f'{peremen} = {value};\n')
                    continue

                elif "%=%" in token.content:
                    peremen, content = token.content.split('%=%', 1)
                    value = content.strip()
                    peremen_clean = peremen.strip()
                    f.write(f'let {peremen_clean} = {value};\n')
                    f.write(f'console.log({peremen_clean});\n')
                    if is_numeric(value):
                        peremem_nubers_name.append(peremen_clean)
                    continue

                elif "typeC " in token.content:
                    # ИСПРАВЛЕНО: Правильная обработка typeC
                    func_def = token.content[6:].strip()
                    if not func_def.endswith('{'):
                        f.write(f"function {func_def} {{\n")
                    else:
                        f.write(f"function {func_def}\n")
                    continue

                elif "TypeLego " in token.content:
                    content = token.content[9:].strip()
                    if " *=* " in content:
                        class_name, fields_str = content.split(" *=* ", 1)
                        class_name = class_name.strip()
                        fields = [f.strip() for f in fields_str.split("%")]
                        f.write(f"{token.indent}function {class_name}({', '.join(fields)}) {{\n")
                        for field in fields:
                            f.write(f"{token.indent}    this.{field} = {field};\n")
                        f.write(f"{token.indent}}}\n")
                    continue

                if "`" in token.content.strip():
                    clean = token.content.strip()
                    if clean.count("`") % 2 == 1:
                        backtic = not backtic

                if "(" in token.content.strip() and not backtic:
                    skobki = True
                if ")" in token.content.strip() and not backtic:
                    skobki = False

                # ИСПРАВЛЕНО: Добавлена проверка на function
                if any(keyword in token.content for keyword in ["if", "elif", "else", "while", "for"]) or \
                        "function" in token.content or \
                        "fun " in token.content or \
                        token.content.strip().endswith(("{", "}")) or \
                        "(" in token.content or \
                        backtic or skobki:
                    f.write(f"{token.content}\n")
                    continue

                elif token.content.strip().endswith(("n^", "^n")):
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
                server_port = token.content.strip()
                f.write(f"app.listen({server_port}, () => {{\n")
                f.write(f"  console.log('🚀 ЗАПУСК СЕРВЕРА 🚀');\n")
                f.write(f"  console.log('\\x1b[34m Сервер запущен на порту -> {server_port} \\x1b[0m');\n")
                f.write("});\n")
                continue

            elif "fun " in token.lex:
                content = token.content.strip()
                func_body = content[4:] if content.startswith('fun ') else content

                if not func_body.endswith('{'):
                    f.write(f"{token.indent}function {func_body} {{\n")
                else:
                    f.write(f"{token.indent}function {func_body}\n")
                continue