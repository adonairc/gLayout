from gdsfactory.component import Component
import gdsfactory as gf
from gdsfactory.geometry.boolean import boolean


def sky130_add_npc(comp: Component) -> Component:
	"""To keep with the generic generator structure,
	we do NOT add nitride poly cut layer in the generic generators (npc is specfic to sky130).
	Because it is easy to add idenpedently, 
	we implement this as a function wrapper to correctly lay npc
	returns the modified component"""
	# extract licon polygons which are over poly (using booleans)
	licon_comp = comp.extract(layers=[(66,44)])
	poly_comp = comp.extract(layers=[(66,20)])
	existing_npc = comp.extract(layers=[(95,20)])
	# TODO: see about an implemtation using gdsfactory component metadata
	if len(licon_comp.get_polygons()) < 2 and len(poly_comp.get_polygons()) < 2:
		return comp
	liconANDpoly = boolean(licon_comp, poly_comp, layer=(1,2), operation="and")
	if len(existing_npc.get_polygons()) > 1:
		liconANDpoly = boolean(liconANDpoly, existing_npc, layer=(1,2), operation="A-B")
	licon_polygons = liconANDpoly.get_polygons(as_array=False)
	# iterate through all licon and create npc (ignore merges for now)
	npc_polygons = list()
	for licon_polygon in licon_polygons:
		bbox = licon_polygon.bounding_box()
		licon_polygonxmin = bbox[0][0]
		licon_polygonymin = bbox[0][1]
		licon_polygonxmax = bbox[1][0]
		licon_polygonymax = bbox[1][1]
		padding_points = [
			[licon_polygonxmin - 0.1, licon_polygonymin - 0.1],
			[licon_polygonxmax + 0.1, licon_polygonymin - 0.1],
			[licon_polygonxmax + 0.1, licon_polygonymax + 0.1],
			[licon_polygonxmin - 0.1, licon_polygonymax + 0.1],
		]
		npc_polygons.append(gf.kdb.DPolygon(padding_points))
	# determine which npc polygons should be merged
	# also merge them by adding a polygon over them
	# naive approach, n^2 complexity
	npc_merged_polygons = list()
	for i, npc_polygon in enumerate(npc_polygons):
		for j, other_polygon in enumerate(npc_polygons):
			# use the fact that all npc polys have the same width (at this point)
			bbox_i = npc_polygon.bbox()
			bbox_j = other_polygon.bbox()
			center_i = ((bbox_i.left + bbox_i.right) / 2, (bbox_i.bottom + bbox_i.top) / 2)
			center_j = ((bbox_j.left + bbox_j.right) / 2, (bbox_j.bottom + bbox_j.top) / 2)
			yviolation = abs(center_i[1] - center_j[1]) < 0.64#0.27+0.37
			xviolation = abs(center_i[0] - center_j[0]) < 0.64
			if i==j:#skip same polygon
				continue
			elif (xviolation and yviolation):
				nxmax = max(bbox_i.right, bbox_j.right)
				nxmin = min(bbox_i.left, bbox_j.left)
				nymax = max(bbox_i.top, bbox_j.top)
				nymin = min(bbox_i.bottom, bbox_j.bottom)
				points = [
					[nxmin,nymin],
					[nxmax,nymin],
					[nxmax,nymax],
					[nxmin,nymax],
				]
				npc_merged_polygons.append(gf.kdb.DPolygon(points))
	# add npc and return
	npc_polygons_to_add = npc_polygons + npc_merged_polygons
	for poly in npc_polygons_to_add:
		comp.add_polygon(poly, layer=(95, 20))
	return comp
