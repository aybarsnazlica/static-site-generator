import unittest

from inline_markdown import split_nodes_delimiter, split_nodes_link, split_nodes_image, extract_markdown_links, \
    extract_markdown_images, extract_title, text_to_textnodes
from textnode import TextNode, TextType


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

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://images.com/image1.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://images.com/image1.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://images.com/image1.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://images.com/image1.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://images.com/image1.png) and another ![second image](https://images.com/image2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://images.com/image1.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://images.com/image2.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_links(self):
        # Test with multiple links
        text = "This is a [link](https://example.com) and another [one](https://test.com)."
        expected = [("link", "https://example.com"), ("one", "https://test.com")]
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with no links
        text = "This has no markdown links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with special characters in link text and URL
        text = "Here is [a link with special chars](https://example.com/path?arg=value&other=1)."
        expected = [("a link with special chars", "https://example.com/path?arg=value&other=1")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images(self):
        # Test with multiple images
        text = ("Here is an image ![alt text](https://example.com/image.png) and another ![another]("
                "https://example.com/another.jpg).")
        expected = [("alt text", "https://example.com/image.png"), ("another", "https://example.com/another.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with no images
        text = "This has no markdown images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with special characters in alt text and URL
        text = "Here is ![image with special chars](https://example.com/image.png?query=test&foo=bar)."
        expected = [("image with special chars", "https://example.com/image.png?query=test&foo=bar")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_title_basic(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_spaces(self):
        markdown = "#   Trimmed Title   "
        self.assertEqual(extract_title(markdown), "Trimmed Title")

    def test_extract_title_without_space_after_hash(self):
        markdown = "#TitleWithoutSpace"
        self.assertEqual(extract_title(markdown), "TitleWithoutSpace")

    def test_extract_title_with_extra_hashes(self):
        markdown = "## Not an H1"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_multiline(self):
        markdown = """
            # First Title
            ## Second Title
            ### Third Title
        """
        self.assertEqual(extract_title(markdown), "First Title")

    def test_extract_title_no_title(self):
        markdown = "Just some text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty_string(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_node_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), nodes)


if __name__ == '__main__':
    unittest.main()
