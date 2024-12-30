import unittest

from src.htmlnode import LeafNode
from src.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node_no_tag(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        leaf_node = LeafNode(None, "")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This is a text node", TextType.BOLD)
        leaf_node = LeafNode("b", text_node.text)
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        leaf_node = LeafNode("a", text_node.text, {"href": "https://www.boot.dev"})
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        leaf_node = LeafNode("img", text_node.text, {"src": "https://www.boot.dev", "alt": text_node.text})
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)


if __name__ == "__main__":
    unittest.main()
