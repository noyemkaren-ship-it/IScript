
def make_echo(indent, content, color_code=None):
    if not content:
        return None

    if color_code:
        log_value = f"'{color_code}' + {content} + '\\x1b[0m'"
    else:
        log_value = content

    return f"{indent}console.log({log_value});\n"

def ECHO_LOGIC(indent, content):
    return make_echo(indent, content)

def RED_ECHO_LOGIC(indent, content):
    return make_echo(indent, content, color_code=r"\x1b[31m")

def GREEN_ECHO_LOGIC(indent, content):
    return make_echo(indent, content, color_code=r"\x1b[32m")

def BLUE_ECHO_LOGIC(indent, content):
    return make_echo(indent, content, color_code=r"\x1b[34m")
