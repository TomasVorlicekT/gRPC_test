import re
from jinja2 import Template

def extract_proto_name(proto_file_path):
    """
    Extract the .proto file name for the title.
    """
    proto_name = proto_file_path.split('/')[-1].replace('.proto', '')
    return proto_name

def extract_messages_with_attributes(proto_file_path):
    """
    Extract message names and their attributes, including descriptions from multi-line comments.
    """
    with open(proto_file_path, 'r') as file:
        content = file.read()

    # Regex to match message blocks
    message_pattern = re.compile(r'message\s+(\w+)\s*{([^}]*)}', re.DOTALL)
    
    # Updated regex to match multi-line comments followed by a field, with optional "optional" keyword
    field_pattern = re.compile(r'(?:\/\/[^\n]*\n)*\s*(optional\s+)?(\w+)\s+(\w+)\s*=\s*\d+;', re.MULTILINE)

    messages = []

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
                    optional_keyword = field_match.group(1) or ""  # Capture "optional" if it exists
                    field_type = field_match.group(2)
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

    return messages


def render_html_with_messages(title, messages, template_path, output_path):
    """
    Render a single HTML file containing all messages and their attributes.
    """
    with open(template_path, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_html = template.render(
        title=title,
        messages=messages
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
messages = extract_messages_with_attributes(proto_file)

# Render the HTML file with all messages
render_html_with_messages(
    title=title,
    messages=messages,
    template_path=template_file,
    output_path=output_html_file
)
