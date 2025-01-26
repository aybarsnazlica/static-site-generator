from textnode import TextNode, TextType
from util import copy_content


def main():
    tn = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(tn)
    copy_content("./static", "./public")


if __name__ == "__main__":
    main()
