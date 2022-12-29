import os
import tempfile
import unittest

from macos_installation.functions import template


class TestRenderTemplate(unittest.TestCase):
    def setUp(self):
        # Create a temporary file containing the template string
        self.template_file = tempfile.NamedTemporaryFile("w+t", delete=False)
        self.template_file.write(
            "This is a test template with key1=$key1 and key2=$key2."
        )
        self.template_file.seek(0)

    def test_render_template(self):
        # Set up test data and expected results
        template_path = self.template_file.name
        substitutions = {"key1": "value1", "key2": "value2"}
        expected_result = "This is a test template with key1=value1 and key2=value2."

        # Ensure the function returns the expected result
        result = template.render_template(template_path, substitutions)
        self.assertEqual(result, expected_result)

    def tearDown(self):
        # Close and delete the temporary file
        self.template_file.close()
        os.unlink(self.template_file.name)


if __name__ == "__main__":
    unittest.main()
