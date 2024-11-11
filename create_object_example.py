from _imports import RFEM, rfem

with RFEM('example_model') as model:

    # --- CREATE FUNCTIONS --- #

    model.create_object(rfem.structure_core.Material(no=1, name="S450 | EN 1993-1-1:2005-05"))
    model.create_object(rfem.structure_core.Material(no=2, name="Sand, well-graded (SW) | DIN 18196:2011-05"))
    model.create_object(rfem.structure_core.Node(no=1, coordinate_1= 1, coordinate_2=1, coordinate_3=-1))
    model.create_object(rfem.structure_core.Node(no=5, coordinate_1=10))
    model.create_object(rfem.structure_core.Line(no=1, definition_nodes=[1,2]))
