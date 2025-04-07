from enum import Enum

from html_node import ParentNode
from inline_markdown import text_to_textnodes
from text_node import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Splits markdown text into individual blocks of content.

    Args:
        markdown (str): The complete markdown text.

    Returns:
        list[str]: A list of block strings separated by blank lines.
    """
    blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    """Determines the block type (e.g., heading, paragraph, code) of a markdown block.

    Args:
        block (str): A markdown block.

    Returns:
        BlockType: The type of the markdown block.
    """
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Converts complete markdown text into an HTML node tree.

    Args:
        markdown (str): Markdown text to convert.

    Returns:
        ParentNode: A root HTML node representing the parsed markdown.
    """
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    """Converts a markdown block to its corresponding HTML node.

    Args:
        block (str): A single block of markdown.

    Returns:
        ParentNode: An HTML representation of the block.
    """
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    raise ValueError("invalid block type")


def text_to_children(text: str) -> list:
    """Converts inline markdown text to a list of HTML child nodes.

    Args:
        text (str): Inline markdown text.

    Returns:
        list: A list of HTML nodes representing the inline content.
    """
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    """Converts a paragraph block into an HTML <p> element.

    Args:
        block (str): A paragraph block of markdown.

    Returns:
        ParentNode: An HTML <p> node with inline children.
    """
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)

    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    """Converts a heading block into an HTML heading tag (h1-h6).

    Args:
        block (str): A heading block of markdown.

    Returns:
        ParentNode: An HTML heading node.
    """
    level = 0

    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)

    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    """Converts a code block into an HTML <pre><code> block.

    Args:
        block (str): A code block in markdown.

    Returns:
        ParentNode: An HTML <pre><code> node.
    """
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")

    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])

    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    """Converts an ordered list markdown block into an HTML <ol> element.

    Args:
        block (str): An ordered list block.

    Returns:
        ParentNode: An HTML <ol> node with <li> children.
    """
    items = block.split("\n")
    html_items = []

    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    """Converts an unordered list markdown block into an HTML <ul> element.

    Args:
        block (str): An unordered list block.

    Returns:
        ParentNode: An HTML <ul> node with <li> children.
    """
    items = block.split("\n")
    html_items = []

    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    """Converts a quote block into an HTML <blockquote> element.

    Args:
        block (str): A quote block in markdown.

    Returns:
        ParentNode: An HTML <blockquote> node.
    """
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)

    return ParentNode("blockquote", children)
