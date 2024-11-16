# This file defines the manual order structure for folders and objects within the RFEM (so far
# the generator is only presuming the use with RFEM proto files).
# 
# `folder_order` specifies the custom ordering of two main folders from Data Navigator.
#
# `object_data_order` provides an ordered list of objects (by name and description) within 
# each folder, allowing each item to have a predefined position and a description. 
#
# Feel free to update the order or add descriptions as needed.


folder_order = [
    "rfem.structure_core", 
    "rfem.structure_advanced", 
    "rfem.common"
    ]


object_data_order = {
    "rfem.structure_core": [
        {"name": "Material", "description": "Defines the material properties used in structural elements."},
        {"name": "Section", "description": "Specifies the cross-sectional profile for elements like members."},
        {"name": "Thickness", "description": "Defines the thickness of surfaces."},
        {"name": "Node", "description": "Represents a point in space, defined by coordinates (e.g., x, y, z)."},
        {"name": "Line", "description": "Represents a linear element."},
        {"name": "Member", "description": "A structural element, used to model beams, columns, etc."},
        {"name": "Surface", "description": "Represents a plane bounded by lines."},
        {"name": "Opening", "description": "Defines an opening within a surface, like a window or door in a wall."},
        {"name": "Solid", "description": "Represents a 3D volume element."},
        {"name": "LineSet", "description": "A collection of lines that can be grouped and manipulated as a unit."},
        {"name": "MemberSet", "description": "A collection of members grouped together."},
        {"name": "SurfaceSet", "description": "A collection of surfaces grouped together."},
        {"name": "SolidSet", "description": "A collection of solids grouped together."}
    ],
    "rfem.structure_advanced": [
        {"name": "Block", "description": "A block represents a model component with typified properties."},
        {"name": "Intersection", "description": "Defines the intersection between structural elements."},
        {"name": "LineRelease", "description": "Allows a line to separate from connected elements under certain conditions."},
        {"name": "NodalRelease", "description": "Defines specific conditions where nodes can release forces or moments."},
        {"name": "ResultSection", "description": "Defines sections where results can be evaluated."},
        {"name": "RigidLink", "description": "Connects structural elements with a rigid link that transmits forces and moments."},
        {"name": "StructureModification", "description": "Applies modifications to structural elements, such as stiffness adjustments."},
        {"name": "SurfaceRelease", "description": "Defines conditions for surface separation from other elements."},
        {"name": "SurfaceResultsAdjustment", "description": "Adjusts the results for surfaces under specific conditions."},
        {"name": "SurfacesContact", "description": "Defines contact interactions between surfaces, such as friction or gap conditions."}
    ]
}