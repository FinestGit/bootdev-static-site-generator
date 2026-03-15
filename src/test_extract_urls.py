import unittest
from extract_urls import extract_markdown_images, extract_markdown_links


class TestExtractUrls(unittest.TestCase):
    def test_extract_single_images_from_text(self):
        alt_text = "image"
        url = "https://i.imgur.com/zjjcJKZ.png"
        text = f"This is text with an ![{alt_text}]({url})"
        result = extract_markdown_images(text)
        self.assertListEqual([(alt_text, url)], result)

    def test_extract_multiple_images_from_text(self):
        alt_text = "rick roll"
        url = "https://i.imgur.com/aKaOqIh.png"
        alt_text2 = "obi wan"
        url2 = "https://i.imgur.com/fJRm4Vk.jpeg"
        text = f"This is text with a ![{alt_text}]({url}) and ![{alt_text2}]({url2})"
        result = extract_markdown_images(text)
        self.assertListEqual([(alt_text, url), (alt_text2, url2)], result)

    def test_extract_single_link_from_text(self):
        alt_text = "lorem ipsum generator"
        url = "https://www.lipsum.com"
        text = f"This takes you to a [{alt_text}]({url})"
        result = extract_markdown_links(text)
        self.assertListEqual([(alt_text, url)], result)

    def test_extract_multiple_links_from_text(self):
        alt_text = "to boot dev"
        url = "https://www.boot.dev"
        alt_text2 = "to youtube"
        url2 = "https://www.youtube.com"
        text = f"This is text with a link [{alt_text}]({url}) and [{alt_text2}]({url2})"
        result = extract_markdown_links(text)
        self.assertListEqual([(alt_text, url), (alt_text2, url2)], result)


if __name__ == "__main__":
    unittest.main()
