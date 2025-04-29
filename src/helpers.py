import re

from textnode import TextType, TextNode, text_node_to_html_node
from blocks import BlockType, block_to_type
from htmlnode import ParentNode, LeafNode, HTMLNode

def split_nodes_delimiter(old_nodes, delimiter, input_text_type):
    ret = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret.append(node)
            continue
        txt = node.text
        orig_type = node.text_type
        delim_split = txt.split(delimiter, maxsplit=2)
        if len(delim_split) != 3:
            ret.append(node)
            continue
        for i in range(len(delim_split)):
            new_node = TextNode(delim_split[i], orig_type)
            if i == 1: 
                new_node.text_type = input_text_type
            if len(new_node.text) > 0:
                ret.append(new_node)
    # if we added a new node, we'll recurse in case there are multiple items to split on the same node
    if len(ret) != len(old_nodes):  
        ret = split_nodes_delimiter(ret, delimiter, input_text_type)
    return ret

def extract_markdown_images(text):
    rex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(rex, text)
    
def extract_markdown_links(text):
    rex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(rex, text)
    

def split_nodes_link(node_list):
    ret = []
    for node in node_list:
        if node.text_type != TextType.TEXT:
            ret.append(node)
            continue
    
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            ret.append(node)
            continue

        text = node.text
        for link_tuple in links:
            link_text, href = link_tuple
            split_matcher = f"[{link_text}]({href})"
            split_text = text.split(split_matcher)
            if split_text[0] != "":
                ret.append(TextNode(split_text[0], TextType.TEXT))
            ret.append(TextNode(link_text, TextType.LINK, href))
            text = "".join(split_text[1:])
        if text != "":
            ret.append(TextNode(text, TextType.TEXT))
    return ret

def split_nodes_image(node_list):
    ret = []
    for node in node_list:
        if node.text_type != TextType.TEXT:
            ret.append(node)
            continue
    
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            ret.append(node)
            continue

        text = node.text
        for image_tuple in images:
            alt, url = image_tuple
            split_matcher = f"![{alt}]({url})"
            split_text = text.split(split_matcher)
            if split_text[0] != "":
                ret.append(TextNode(split_text[0], TextType.TEXT))
            ret.append(TextNode(alt, TextType.IMAGE, url))
            text = "".join(split_text[1:])
        if text != "":
            ret.append(TextNode(text, TextType.TEXT))
    return ret

def text_to_textnodes(text):
    if text == "":
        return []
    orig_node = TextNode(text, TextType.TEXT)
    split_bold = split_nodes_delimiter([orig_node], "**", TextType.BOLD)
    split_ital = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_ital, "`", TextType.CODE)
    split_links = split_nodes_link(split_code)
    ret =  split_nodes_image(split_links)

    return ret


def markdown_to_blocks(markdown):
    blocks_list = markdown.split("\n\n")
    cleaned = list(map(lambda block: block.strip(), blocks_list))
    filtered = list(filter(lambda block: len(block) > 0, cleaned))

    return filtered


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_html_nodes = []
    for block in blocks:
        btype = block_to_type(block)
        block_html_node = None
        if btype == BlockType.HEADING:
                block_html_node = heading_block_to_html_parent_and_children(block)
        elif btype == BlockType.PARAGRAPH:
                block_html_node = p_block_to_html_parent_and_children(block)
        elif btype == BlockType.CODE:
                block_html_node = code_block_to_html_parent_and_children(block)
        elif btype == BlockType.QUOTE:
                block_html_node = quote_block_to_html_parent_and_children(block)
        elif btype == BlockType.UNORDERED_LIST:
                block_html_node = ul_block_to_html_parent_and_children(block)
        elif btype == BlockType.ORDERED_LIST:
                block_html_node = ol_block_to_html_parent_and_children(block)
        block_html_nodes.append(block_html_node)
    
    return ParentNode("div", children=block_html_nodes)


def text_to_children(text):
    ret = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
       html_node = text_node_to_html_node(text_node)
       ret.append(html_node)
    return ret

def handle_whitespace(block_text, is_code_block=False):
    return " ".join(block_text.split())


def p_block_to_html_parent_and_children(block_text):
    block_text = handle_whitespace(block_text)
    return ParentNode("p", children=text_to_children(block_text))

def heading_block_to_html_parent_and_children(block_text):
    block_text = handle_whitespace(block_text)
    m = re.match(r"#{1,6}", block_text).group()
    header_tag = f"h{len(m)}"
    rest = block_text.replace(m, "").strip()
    return ParentNode(header_tag, children=text_to_children(rest))

def code_block_to_html_parent_and_children(block_text):
    block_text = block_text.replace("```\n", "").replace("```", "")
    inner = LeafNode("code", block_text)
    return ParentNode("pre", [inner])

def quote_block_to_html_parent_and_children(block_text):
    block_text = handle_whitespace(block_text)
    block_text = block_text.replace(">", "").strip()
    return ParentNode("blockquote", children=text_to_children(block_text))

def ul_block_to_html_parent_and_children(block_text):
    leafnodes = generate_list_item_html(block_text)
    return ParentNode("ul", children=leafnodes)

def ol_block_to_html_parent_and_children(block_text):
    start = re.match(r"\d{1,}", block_text).group()
    props = None
    if start != "1":
        props = {"start" : start}
    leafnodes = generate_list_item_html(block_text)
    return ParentNode("ol", children=leafnodes, props=props)

def generate_list_item_html(list_text_raw):
    ret = []
    li_split = list_text_raw.split("\n")
    for line in li_split:
        m = re.match("(\d\.\s)|(\-\s)", line)
        if not bool(m):
            continue
        line = line.replace(m.group(), "").strip()
        child_nodes = text_to_children(line)
        as_html = ParentNode("li", child_nodes)
        ret.append(as_html)
    return ret
