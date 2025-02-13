from textnode import TextNode, TextType
from util import copy_content


# def generate_page(from_path, template_path, dest_path):
#     print(f"Generating page from {from_path} to {dest_path} using {template_path}")
#     with open(from_path, "r", encoding="utf-8") as f:
#         from_page = f.read()
#
#     with open(template_path, "r", encoding="utf-8") as f:
#         template = f.read()


def main():
    tn = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(tn)
    copy_content("./static", "./public")


if __name__ == "__main__":
    main()
