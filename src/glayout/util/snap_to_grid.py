from gdsfactory.component import Component
from pydantic import validate_arguments


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def component_snap_to_grid(comp: Component) -> Component:
	"""snaps all polygons and ports in component to grid
	comp = the component to snap to grid
	NOTE this function will flatten the component
	"""
	# In GDSFactory v9, flatten() mutates in-place and returns None
	name = comp.name
	comp.flatten()  # Mutates comp in-place
	comp = comp.copy()  # Now copy the flattened component
	comp.name = name
	return comp


