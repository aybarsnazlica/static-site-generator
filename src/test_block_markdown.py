import unittest
from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_split_block(self):
        """Test basic splitting into blocks."""
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_removes_empty_blocks(self):
        """Test removal of empty blocks caused by excessive newlines."""
        markdown = """# Heading


This is a paragraph.


- List item 1
- List item 2


"""
        expected_blocks = [
            "# Heading",
            "This is a paragraph.",
            "- List item 1\n- List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_single_line(self):
        """Test when there is only one line of markdown."""
        markdown = "# Single heading"
        expected_blocks = ["# Single heading"]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_multiple_paragraphs(self):
        """Test multiple paragraphs separated by double newlines."""
        markdown = """This is the first paragraph.

This is the second paragraph.

This is the third paragraph."""
        expected_blocks = [
            "This is the first paragraph.",
            "This is the second paragraph.",
            "This is the third paragraph."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_no_blocks(self):
        """Test an empty string input."""
        markdown = ""
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_only_newlines(self):
        """Test input with only newlines."""
        markdown = "\n\n\n"
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_mixed_content(self):
        """Test markdown with a mix of headers, paragraphs, and lists."""
        markdown = """# Header 1

Paragraph under header 1.

## Header 2

Paragraph under header 2.

- List item 1
- List item 2

Another paragraph."""
        expected_blocks = [
            "# Header 1",
            "Paragraph under header 1.",
            "## Header 2",
            "Paragraph under header 2.",
            "- List item 1\n- List item 2",
            "Another paragraph."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)


if __name__ == '__main__':
    unittest.main()
