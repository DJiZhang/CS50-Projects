from pathlib import Path
import sys
import re


def validate_file(single_file_path):
        """Validate a single file name, check if it opens.
        Supported file types: .md, .tex"""
        path = Path(single_file_path).resolve()
        if (suffix:=path.suffix.lower()) not in (".md", ".tex"):
             raise ValueError("File should have .md or .tex ext")
        return path.name

def convert(content:str, delim:dict)->str:
    """Converts all LaTex delimters in the string content to desired output
     op is dict {inline:"str", display: "str"} with the desired type of delimters.
     (Can be None)"""
    # Processing to flag environs that should not be touched (comments, verbatim, etc.)
    # \begin{verbatim|listing|minted}\end{...}
    PROTECTED_ENV = re.compile(
    r'\\begin\{(?P<type>verbatim\*?|lstlisting|minted)\}(.*?)\\end\{(?P=type)\}',
    re.DOTALL)

    # \verb \verb*
    INLINE_VERB = re.compile(
        r'\\verb\*?(.).*?\1',
        re.DOTALL)
    COMMENT = re.compile(r'(?<!\\)%(?:[^\n])*')

    protected_ranges = []
    for match in PROTECTED_ENV.finditer(content):
         protected_ranges.append(match.span(0))

    for match in  INLINE_VERB.finditer(content):
        protected_ranges.append(match.span(0))

    for match in COMMENT.finditer(content):
        protected_ranges.append(match.span(0))

    protected_ranges.sort(key = lambda x: x[0])

    # Convert display
    if delim["display"] is not None and delim["display"] != "None":
        DISPLAY_PATTERNS = {
         "dollar":r'(?<!\\)\$\$(?!\$)((?:[^$\\]|\\.)+?)(?<!\\)\$\$(?!\$)',
         "paren":r'(?<!\\)\\\[((?:[^$\\]|\\[^\)\(])+?)(?<!\\)\\\]'}
        DISPLAY_DELIMS = {"dollar": r"$$",
                      "paren-start": r"\[", "paren-end": r"\]"}

        if delim["display"] == "dollar":
            # If desired output dollar, only convert paren
            display_pattern = re.compile(DISPLAY_PATTERNS["paren"])
            display_delim_start = DISPLAY_DELIMS["dollar"]
            display_delim_end = DISPLAY_DELIMS["dollar"]
        else:
            display_pattern = re.compile(DISPLAY_PATTERNS["dollar"])
            display_delim_start = DISPLAY_DELIMS["paren-start"]
            display_delim_end = DISPLAY_DELIMS["paren-end"]

        for match in display_pattern.finditer(content):
            span = match.span(0)
            flag = False
            # Ensure span not in protected section
            for section in protected_ranges:
                if span[0]>=section[0] and span[1]<=section[1]:
                    flag = True
                    break
                if span[0]<section[0]:
                    break # No need to check
            if not flag:
                # Replace Delimeters
                start = match.start(0)
                end = match.end(0)
                content = content[:start]+display_delim_start+content[start+2:end-2]+display_delim_end+content[end:]

    # Convert inline
    if delim["inline"] is not None and delim["inline"] != "None":
        INLINE_PATTERNS = {
            "dollar":r'(?<!\$)(?<!\\)\$(?!\$)((?:[^$\\\n]|\\.)+?)(?<!\$)(?<!\\)\$(?!\$)',
            "paren":r'\\\(((?:[^\$\\\n]|\\[^()])+?)\\\)'
            }
        INLINE_DELIMS = {"dollar": r"$",
                        "paren-start": r"\(", "paren-end": r"\)"}
        if delim["inline"] == "dollar":
            # If desired output dollar, only convert paren
            inline_pattern = re.compile(INLINE_PATTERNS["paren"])
            inline_delim_start = INLINE_DELIMS["dollar"]
            inline_delim_end = INLINE_DELIMS["dollar"]
            delim_len = 2
        else:
            inline_pattern = re.compile(INLINE_PATTERNS["dollar"])
            inline_delim_start = INLINE_DELIMS["paren-start"]
            inline_delim_end = INLINE_DELIMS["paren-end"]
            delim_len = 1
        matches = list(inline_pattern.finditer(content))


        for match in reversed(matches):
            span = match.span(0)
            flag = False
            # Ensure span not in protected section
            for section in protected_ranges:
                 if span[0]>=section[0] and span[1]<=section[1]:
                      flag = True
                      break
                 if span[0]<section[0]:
                      break # No need to check
            if not flag:
                 # Replace Delimeters
                 start = match.start(0)
                 end = match.end(0)
                 content = content[:start]+inline_delim_start+content[start+delim_len:end-delim_len]+inline_delim_end+content[end:]



    return content



def main():
    file_name = "test.tex"
    path = validate_file(file_name)
    content = path.read_text(encoding="utf-8")

    with open("output.tex", "w") as f:
        f.write(convert(content,{"inline":"paren", "display":"dollar"}))


if __name__ == "__main__":
     main()
