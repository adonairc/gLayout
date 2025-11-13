"""
usage: from gf180_mapped import gf180_mapped_pdk
"""

from ..gf180_mapped.gf180_grules import grulesobj
from ..mappedpdk import MappedPDK, SetupPDKFiles
from pathlib import Path
import os
from gdsfactory.typings import LayerSpec
from gdsfactory.technology import LayerMap
from gdsfactory.typings import Layer
# Actual Pin definations for GlobalFoundries 180nmMCU from the PDK manual
# Ref: https://gf180mcu-pdk.readthedocs.io/en/latest/

#LAYER["fusetop"]=(75, 0)
class LayerMapGf180(LayerMap):
    metal5: Layer =  (81, 0)
    via4: Layer =  (41, 0)
    metal4: Layer =  (46, 0)
    via3: Layer =  (40, 0)
    metal3: Layer =  (42, 0)
    via2: Layer =  (38, 0)
    metal2: Layer =  (36, 0)
    via1: Layer =  (35, 0)
    metal1: Layer =  (34, 0)
    contact: Layer =  (33, 0)
    poly2: Layer =  (30, 0)
    comp: Layer =  (22, 0)
    nplus: Layer =  (32, 0)
    pplus: Layer =  (31, 0)
    nwell: Layer =  (21, 0)
    lvpwell: Layer =  (204, 0)
    dnwell: Layer =  (12, 0)
    CAP_MK: Layer =  (117, 5)
    # _Label Layer Definations
    metal5_label: Layer =  (81,10)
    metal4_label: Layer =  (46,10)
    metal3_label: Layer =  (42,10)
    metal2_label: Layer =  (36,10)
    metal1_label: Layer =  (34,10)
    poly2_label: Layer =  (30,10)
    comp_label: Layer =  (22,10)

LAYER = LayerMapGf180

gf180_glayer_mapping: dict[str,LayerSpec]  = {
    "met5": "metal5",
    "via4": "via4",
    "met4": "metal4",
    "via3": "via3",
    "met3": "metal3",
    "via2": "via2",
    "met2": "metal2",
    "via1": "via1",
    "met1": "metal1",
    "mcon": "contact",
    "poly": "poly2",
    "active_diff": "comp",
    "active_tap": "comp",
    "n+s/d": "nplus",
    "p+s/d": "pplus",
    "nwell": "nwell",
    "pwell": "lvpwell",
    "dnwell": "dnwell",
    "capmet": "CAP_MK",
    # _pin layer ampping
    "met5_pin": "metal5_label",
    "met4_pin": "metal4_label",
    "met3_pin": "metal3_label",
    "met2_pin": "metal2_label",
    "met1_pin": "metal1_label",
    "poly_pin": "poly2_label",
    "active_diff_pin": "comp_label",
    # _label layer mapping
    "met5_label": "metal5_label",
    "met4_label": "metal4_label",
    "met3_label": "metal3_label",
    "met2_label": "metal2_label",
    "met1_label": "metal1_label",
    "poly_label": "poly2_label",
    "active_diff_label": "comp_label",
}

gf180_valid_bjt_sizes = {
    "npn" : [
        (0.54, 2.0),
        (0.54, 4.0),
        (0.54, 8.0),
        (0.54, 16.0),
        (5.0, 5.0),
        (10.0, 10.0),
    ],
    "pnp" : [
        (5.0, 0.42),
        (5.0, 5.0),
        (10.0, 0.42),
        (10.0, 10.0),
    ],
}

# note for DRC, there is mim_option 'A'. This is the one configured for use

gf180_lydrc_file_path = Path(__file__).resolve().parent / "gf180mcu_drc.lydrc"
# openfasoc_dir = Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent
# pdk_root = Path('/usr/bin/miniconda3/share/pdk/')
pdk_root = Path(os.getenv('PDK_ROOT'))
lvs_schematic_ref_file = Path(__file__).resolve().parent / "gf180mcu_osu_sc_9T.spice"
magic_drc_file = pdk_root / "gf180mcuC" / "libs.tech" / "magic" / "gf180mcuC.magicrc"
lvs_setup_tcl_file = pdk_root / "gf180mcuC" / "libs.tech" / "netgen" / "gf180mcuC_setup.tcl"
temp_dir = None


pdk_files = SetupPDKFiles(
    pdk_root=pdk_root,
    klayout_drc_file=gf180_lydrc_file_path,
    lvs_schematic_ref_file=lvs_schematic_ref_file,
    lvs_setup_tcl_file=lvs_setup_tcl_file,
    magic_drc_file=magic_drc_file,
    temp_dir=temp_dir,
    pdk='gf180'
).return_dict_of_files()

gf180_mapped_pdk = MappedPDK(
    name="gf180",
    glayers=gf180_glayer_mapping,
	models={
        'nfet': 'nfet_03v3',
		'pfet': 'pfet_03v3',
		'mimcap': 'mimcap_1p0fF'
    },
    layers=LAYER,
    pdk_files=pdk_files,
    grules=grulesobj,
    valid_bjt_sizes=gf180_valid_bjt_sizes
)

# configure the grid size and other settings
# gf180_mapped_pdk.gds_write_settings.precision = 5*10**-9
# gf180_mapped_pdk.cell_decorator_settings.cache=False
gf180_mapped_pdk.layers = LAYER