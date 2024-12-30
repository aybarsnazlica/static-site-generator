import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_no_children(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_single_parent_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>Italic text</i></p>")

    def test_to_html_nested_parent_multiple_levels(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Nested Bold text"),
                        LeafNode(None, "Nested Normal text"),
                    ],
                ),
                LeafNode(None, "Sibling text"),
            ],
        )
        self.assertEqual(node.to_html(), "<div><p><b>Nested Bold text</b>Nested Normal text</p>Sibling text</div>")

    def test_to_html_parent_no_children(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

    def test_to_html_parent_with_properties_no_children(self):
        node = ParentNode("div", [], {"class": "container"})
        self.assertEqual(node.to_html(), "<div class=\"container\"></div>")

    def test_to_html_parent_deeply_nested(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "body",
                    [
                        ParentNode(
                            "div",
                            [
                                LeafNode("h1", "Header"),
                                ParentNode(
                                    "p",
                                    [
                                        LeafNode("b", "Bold"),
                                        LeafNode(None, " and "),
                                        LeafNode("i", "Italic"),
                                    ],
                                ),
                            ],
                        )
                    ],
                )
            ],
        )

        self.assertEqual(node.to_html(),
                         "<html><body><div><h1>Header</h1><p><b>Bold</b> and <i>Italic</i></p></div></body></html>")


if __name__ == "__main__":
    unittest.main()
