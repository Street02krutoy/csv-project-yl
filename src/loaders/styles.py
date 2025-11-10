from os import listdir


def load_styles() -> str:
    stylesDir = listdir("src/styles")
    styles = ""
    for filename in stylesDir:
        if not filename.endswith(".qss"):
            continue
        content = f"\n/*{filename}*/\n"
        file = open("src/styles/"+filename)
        content += file.read()
        styles += content+"\n"
    return styles
