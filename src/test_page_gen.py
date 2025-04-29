import unittest

from page_gen import extract_title

class TestExtractHeader(unittest.TestCase):
    def test_header(self):
        md = """
not this

## or this

# definitely this tho 
"""
        want = "definitely this tho"
        got = extract_title(md)
        self.assertEqual(want, got)



if __name__ == "__main__":
    unittest.main()