import re
from jinja2 import Template

def transform_types(input_data_type):

    transform_dict = {'int32' : 'int', 'double' : 'float', 'string' : 'str'}

    if input_data_type in transform_dict:
        return transform_dict[input_data_type]
    else:
        return input_data_type

def extract_proto_name(proto_file_path):
    """
    Extract the .proto file name for the title.
    """
    proto_name = proto_file_path.split('/')[-1].replace('.proto', '')
    return proto_name

def extract_messages_and_enums_with_attributes(proto_file_path):
    """
    Extract message names and their attributes, including descriptions from multi-line comments.
    """
    with open(proto_file_path, 'r') as file:
        content = file.read()

    # Regex to match message blocks
    message_pattern = re.compile(r'message\s+(\w+)\s*{([^}]*)}', re.DOTALL)
    enum_pattern = re.compile(r'enum\s+(\w+)\s*{([^}]*)}', re.DOTALL)
    
    messages = []
    enums = []

    for message_match in message_pattern.finditer(content):
        message_name = message_match.group(1)
        fields_block = message_match.group(2)

        fields = []
        current_comment = []
        
        # Process each line in fields_block to handle comments and fields accurately
        for line in fields_block.splitlines():
            line = line.strip()
            if line.startswith("//"):
                # Accumulate comment lines
                current_comment.append(line.strip("// ").strip())
            elif line:  # Non-empty line that might be a field definition
                # Match the field definition with optional keyword
                field_match = re.match(r'(optional\s+)?(\w+)\s+(\w+)\s*=\s*\d+;', line)
                if field_match:
                    optional_keyword = field_match.group(1) or ""  # Capture "optional" if it exists, might be useful later
                    field_type = transform_types(field_match.group(2))
                    field_name = field_match.group(3)
                    description = " ".join(current_comment).strip()
                    fields.append({
                        "name": field_name,
                        "type": field_type,
                        "optional": bool(optional_keyword.strip()),  # True if "optional" is present
                        "description": description
                    })
                    # Clear the current comment after assigning it to the field
                    current_comment = []

        messages.append({"name": message_name, "fields": fields})


    for enum_match in enum_pattern.finditer(content):
        enum_name = enum_match.group(1)
        fields_block = enum_match.group(2)

        fields = []
        
        # Process each line in fields_block to handle comments and fields accurately
        for line in fields_block.splitlines():
            line = line.strip()
            enum_value_match = re.match(r'(?:\/\/[^\n]*\n)*\s*(\w+)\s*=\s*(\d+);', line)
            if enum_value_match:
                enum_value_name = enum_value_match.group(1)
                #enum_value_value = enum_value_match.group(2) do not need at this point
                enum_description = ""
                fields.append({
                    "name": enum_value_name,
                    "description": enum_description
                })
                current_comment = []  # Clear comment after use

        enums.append({"name": enum_name, "fields": fields})

    return [messages, enums]


def render_html_with_messages(title, messages, enums, template_path, output_path):
    """
    Render a single HTML file containing all messages and their attributes.
    """
    with open(template_path, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_html = template.render(
        title=title,
        messages=messages,
        enums=enums
    )

    with open(output_path, 'w') as output_file:
        output_file.write(rendered_html)

    print(f"HTML file has been generated: {output_path}")

# Usage example
proto_file = 'generator/Material.proto'  # Path to the .proto file
template_file = 'generator/template.html'  # Path to the HTML template
output_html_file = 'generator/Material.html'  # Output HTML file

# Extract proto name for the title
proto_name = extract_proto_name(proto_file)
title = f"{proto_name} - Object Details"

# Extract all messages and their attributes
messages = extract_messages_and_enums_with_attributes(proto_file)[0]
enums = extract_messages_and_enums_with_attributes(proto_file)[1]

# Render the HTML file with all messages
render_html_with_messages(
    title=title,
    messages=messages,
    enums=enums,
    template_path=template_file,
    output_path=output_html_file
)
