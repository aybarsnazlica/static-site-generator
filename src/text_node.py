from html_node import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Represents a piece of formatted text in a markdown-like structure.

    Attributes:
        text (str): The textual content.
        text_type (TextType): The type of formatting applied to the text.
        url (str | None): Optional URL for links or image sources.
    """

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        """Initializes a TextNode instance.

        Args:
            text (str): The textual content.
            text_type (TextType): The type of text formatting.
            url (str | None, optional): The URL associated with links or images. Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Checks equality with another TextNode.

            Args:
                other: The object to compare against.

            Returns:
                bool: True if equal, False otherwise.
            """
        return (
                self.text_type == other.text_type
                and self.text == other.text
                and self.url == other.url
        )

    def __repr__(self) -> str:
        """Returns a string representation of the TextNode.

        Returns:
            str: A string showing text, type, and URL.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Converts a TextNode into a corresponding LeafNode HTML representation.

    Args:
        text_node (TextNode): The TextNode to convert.

    Raises:
        ValueError: If the TextNode has an invalid or unsupported text type.

    Returns:
        LeafNode: An HTML representation of the text node.
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"invalid text type: {text_node.text_type}")
