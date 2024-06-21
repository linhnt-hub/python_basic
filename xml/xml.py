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
def check_xpath_syntax(xpath_expression):
    try:
        # Attempt to create an XPath object with the given expression
        etree.XPath(xpath_expression)
        return True, None
    except etree.XPathSyntaxError as e:
        return False, str(e)
def get_xml_obj(dev, command):
  from jnpr.junos import Device
  try:
    # Connect to the Junos device
    # dev = Device(host=host, user=username, password=password, normalize=True)
    dev.open()
    # Execute the command and get the XML response
    try:
      rpc_cmd = dev.display_xml_rpc(command, format= 'xml').tag.replace("-", "_")
      xml_obj= eval("dev.rpc.{}(normalize=True)".format(rpc_cmd))
      return rpc_cmd, xml_obj #return rpc_name, xml object
    except Exception as e:
      print(f"Can't get rpc, xml value. Check command Error: {e}")
  except Exception as e:
    print(f"Check ip/username/password. Error: {e}")
  finally:
    # Close the connection
    dev.close()
def remove_xml_namespaces(input_xml):
    root = etree.fromstring(input_xml)
    # Iterate through all XML elements
    for elem in root.getiterator():
        # Skip comments and processing instructions,
        # because they do not have names
        if not (
            isinstance(elem, etree._Comment)
            or isinstance(elem, etree._ProcessingInstruction)
        ):
            # Remove a namespace URI in the element's name
            elem.tag = etree.QName(elem).localname
    # Remove unused namespace declarations
    etree.cleanup_namespaces(root)
    return etree.tostring(root).decode()
  
def convert_xml_pretty(element):
    from lxml import etree
    import xml.etree.ElementTree as et
    import xml.dom.minidom
    try: 
      xml_minidom = xml.dom.minidom.parseString(etree.tostring(element))
      xml_pretty = xml_minidom.toprettyxml()
    except Exception as e:
      print(f"Element Parse Fail. Error: {e}")
    return xml_pretty
