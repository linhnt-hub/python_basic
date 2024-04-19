def extract_variables(template_file):
    with open(template_file, 'r') as f:
        template_content = f.read()

    # Use a regular expression to find Jinja variable syntax
    variable_pattern = r'{{\s*(\w+)\s*}}'
    variables = re.findall(variable_pattern, template_content)

    return variables