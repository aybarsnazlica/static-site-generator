from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        if node.text.count(delimiter) == 0 or node.text.count(delimiter) % 2 == 1:
            raise Exception("Invalid Markdown syntax: Closing delimiter not found.")

        split_text = node.text.split(delimiter)
        for i, text in enumerate(split_text):
            if text:
                if i % 2 == 0:
                    new_list.append(TextNode(text, TextType.TEXT))
                else:
                    new_list.append(TextNode(text, text_type))

    return new_list
