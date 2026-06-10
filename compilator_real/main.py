from Lexer import CreateToken
from Parser import Parser
from compilator_real.Lexer import AntiBag

with open("build/main.js", "w") as f:
    f.write("// Compiler\n")

with open("script/main.i", "r") as f:
    st = 0
    for line in f:
        st += 1
        AntiBag(line, st)
        CreateToken(line)

Parser()