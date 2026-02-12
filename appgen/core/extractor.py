
import re

def extract_code_blocks_with_filenames(md: str):
    """
    Robust code block extraction handling filenames and multiple blocks.
    """
    pattern = re.compile(
        r"(?:###\s*filename:\s*(?P<file>[^\n]+)\n)?\s*```(?P<lang>\w*)\n(?P<code>.*?)```",
        re.DOTALL | re.IGNORECASE
    )

    blocks = []
    for match in pattern.finditer(md):
        blocks.append({
            "filename": match.group("file"),
            "language": match.group("lang") or "text",
            "code": match.group("code").strip()
        })
    return blocks
