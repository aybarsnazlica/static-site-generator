import unittest

from src.split import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestSplit(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_with_multiple_nodes(self):
        nodes = [
            TextNode("Pre-text `code` middle-text", TextType.TEXT),
            TextNode("Another `snippet` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("Pre-text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" middle-text", TextType.TEXT),
            TextNode("Another ", TextType.TEXT),
            TextNode("snippet", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    def test_bold(self):
        nodes = [TextNode("This is **bold** text.", TextType.TEXT),
                 TextNode("This is also **bold** text.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("This is also ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ])

    def test_italic(self):
        nodes = [TextNode("This is *italic* text.", TextType.TEXT),
                 TextNode("This is also *italic* text.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
            TextNode("This is also ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ])


if __name__ == '__main__':
    unittest.main()
