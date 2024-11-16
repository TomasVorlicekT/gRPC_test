import os
from jinja2 import Template
from folder_and_objects_data_order import * # This file contains a folder and message order


def generate_folders_and_files(source_folder):
    """
    Traverse the directory and return folder structure and file details, adding descriptions from object_data_order 
    and keeping the field order from the object_data_order and folder structure from folder_order.
    """
    folders = []
    for root, _, files in os.walk(source_folder):
        if os.path.basename(root) == "rfem":
            continue  # Skip this folder and do not add it to the folders list, it contains services and not objects

        folder_name = os.path.relpath(root, source_folder).replace("\\", ".")
        folder = {"path": folder_name, "files": []}
        
        # Check if folder is in object_data_order and use its custom order
        if folder_name in object_data_order:
            ordered_files = object_data_order[folder_name]
            for entry in ordered_files:
                folder["files"].append({
                    "name": entry["name"],
                    "url": f'generated_html/{entry["name"]}.html',
                    "description": entry["description"]
                })
        else:
            # For folders not in object_data_order, use default order and descriptions (= empty string since no description are available)
            for file in sorted(files):
                if file.endswith(".proto"):
                    name_stripped = file.replace(".proto", "")
                    folder["files"].append({
                        "name": name_stripped,
                        "url": f'generated_html/{name_stripped}.html',
                        "description": ""
                    })
                    
        if folder["files"]:
            folders.append(folder)

    # Rearrange the folders so that they correspond to the order in the folder_order
    # folder_order aims to reflect the Data Navigator
    sorted_folders = []

    # Find and insert the desired folders at the start
    for folder_name in folder_order:
        for folder in folders:
            if folder["path"].endswith(folder_name):  # Adjust based on how the name is stored
                sorted_folders.append(folder)
                folders.remove(folder)

    # Add remaining folders (sorted alphabetically)
    sorted_folders.extend(folders)
    
    return sorted_folders

def render_html_with_template(folders, template_path, output_path):
    """
    Render HTML using Jinja2 template and save to the specified output path.
    """
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    template = Template(template_content)
    rendered_html = template.render(folders=folders)

    with open(output_path, 'w') as output_file:
        output_file.write(rendered_html)

    print(f"HTML file has been generated: {output_path}")

def process_directory_and_generate_html(source_folder, template_path, output_html_file):
    """
    Main function to process the directory structure and generate HTML file.
    """
    folders = generate_folders_and_files(source_folder)
    render_html_with_template(folders, template_path, output_html_file)

# Specify paths
source_folder = 'proto'
template_file = 'generator\\template_objects_overview.html'
output_html_file = 'objects_overview.html'

# Generate HTML
process_directory_and_generate_html(source_folder, template_file, output_html_file)
