import os
from jinja2 import Template

def generate_folders_and_files(source_folder):
    """
    Traverse the directory and return folder structure and file details.
    """
    folders = []
    for root, dirs, files in os.walk(source_folder):

        if os.path.basename(root) == "rfem":
            continue  # Skip this folder and do not add it to the folders list, it contains services and not objects

        folder = {
            "path": os.path.relpath(root, source_folder).replace("\\", "."),  # Folder path relative to source
            "files": []
        }
        for file in files:
            # Only consider .proto files, or adjust this as necessary
            if file.endswith(".proto"):
                name_stripped = file.replace(".proto", "")
                folder["files"].append({
                    "name": name_stripped,
                    "url": f'generated_html/{name_stripped}.html")',  # URL relative to root
                    "description" : ""
                })
        # If folder has files, add it to the folders list
        if folder["files"]:
            folders.append(folder)
    
    return folders



def render_html_with_template(folders, template_path, output_path):
    """
    Render HTML using Jinja2 template and save to the specified output path.
    """
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    template = Template(template_content)
    rendered_html = template.render(
        folders=folders  # Pass folder structure and file details
    )

    with open(output_path, 'w') as output_file:
        output_file.write(rendered_html)

    print(f"HTML file has been generated: {output_path}")

def process_directory_and_generate_html(source_folder, template_path, output_html_file):
    """
    Main function to process the directory structure and generate HTML file.
    """
    # Get the folder structure with file details
    folders = generate_folders_and_files(source_folder)
    
    # Generate the HTML file using the template
    render_html_with_template(folders, template_path, output_html_file)

# Specify the paths
source_folder = 'proto'  # Replace with the actual source folder
template_file = 'generator\\template_objects_overview.html'  # Path to your template file
output_html_file = 'generator\\generated_objects_overview.html'  # Path where the output will be saved

# Generate HTML
process_directory_and_generate_html(source_folder, template_file, output_html_file)
