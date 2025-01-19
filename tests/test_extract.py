import unittest
from src.extract import extract_markdown_links, extract_markdown_images


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


if __name__ == "__main__":
    unittest.main()
