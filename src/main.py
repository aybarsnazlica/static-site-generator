from textnode import TextNode, TextType


def main():
    tn = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(tn)


if __name__ == "__main__":
    main()
