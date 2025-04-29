import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_type(block):
    if bool(re.match(r"#{1,6}\s", block)):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```") and len(block) > 3:
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- ") and len(block) > 2:
        return BlockType.UNORDERED_LIST
    elif bool(re.match(r"\d+\.\s", block)):
        return BlockType.ORDERED_LIST
    else: 
        return BlockType.PARAGRAPH