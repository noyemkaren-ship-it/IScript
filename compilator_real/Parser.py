
from tokens import tokens

def Parser():
    with open("build/main.js", "a") as f:
        for token in tokens:
            if token.lex is None:
                if "%=" in token.content:
                    peremen, content = token.content.split('%=')
                    f.write(f'let {peremen} = {content.strip()};\n')
                    continue
                elif "%=%" in token.content:
                    peremen, content = token.content.split('%=%')
                    f.write(f'let {peremen} = {content.strip()};\n')
                    f.write(f'console.log({peremen});\n')
                    continue
                elif "typeC " in token.content:
                    f.write("function "+ token.content[6:] +  "\n")
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
                f.write(f"{token.content}\n")
                continue

            if "echo " in token.lex:
                content = token.content.strip()
                f.write(f'{token.indent}console.log({content});\n')
                continue

            elif "print " in token.lex:
                content = token.content.strip()
                f.write(f'{token.indent}alert({content});\n')
                continue

            elif "fun " in token.lex:
                f.write(f"{token.indent}function {token.content}\n")
                continue