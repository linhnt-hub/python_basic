from jnpr.junos import Device 
from lxml import etree

def get_xml_data(device_host, username, password, command):
    try:
        # Connect to the Junos device
        dev = Device(host=device_host, user=username, password=password)
        dev.open()
        # Execute the command and get the XML response
        response_xml = dev.cli(command, format='xml')
        # Parse the XML response
        root = etree.fromstring(response_xml)
        return root
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Close the connection
        dev.close()