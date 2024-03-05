from lxml import etree

def evaluate_xpath(xml_content, xpath_expression):
    try:
        # Parse the XML content
        root = etree.fromstring(xml_content)
        
        # Use XPath to evaluate the expression
        result = root.xpath(xpath_expression)

        return result
    except etree.XPathError as e:
        return f"XPathError: {e}"

if __name__ == "__main__":
    # Example XML content
    example_xml = """
    <root>
        <element1 attribute="value1">Text1</element1>
        <element2 attribute="value2">Text2</element2>
        <element3 attribute="value3">Text3</element3>
    </root>
    """

    # Example XPath expression
    example_xpath = "//element2/text()"

    # Evaluate the XPath expression on the XML content
    result = evaluate_xpath(example_xml, example_xpath)

    # Display the result
    print(f"XPath Expression: {example_xpath}")
    print("Result:")
    for item in result:
        print(item)
def check_xpath_syntax(xpath_expression):
    try:
        # Attempt to create an XPath object with the given expression
        etree.XPath(xpath_expression)
        return True, None
    except etree.XPathSyntaxError as e:
        return False, str(e)

if __name__ == "__main__":
    # Example XPath expression to check
    example_xpath = "//element[@attribute='value']"

    # Check the syntax of the XPath expression
    is_valid, error_message = check_xpath_syntax(example_xpath)

    # Display the result
    print(f"XPath Expression: {example_xpath}")
    if is_valid:
        print("Syntax is valid.")
    else:
        print(f"Syntax is invalid. Error message: {error_message}")