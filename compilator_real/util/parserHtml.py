



def parser_html(file, token):
    with open(f"build/{file}", "a") as f:
        if token.strip().startswith("btn "):
            spaces_count = token.index("btn ")
            name, func = token[spaces_count+4:].split("%")
            f.write(f"{spaces_count}<button onclick={func}>{name}</button>\n")
        else:
            f.write(token)
