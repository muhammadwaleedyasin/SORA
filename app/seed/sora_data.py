"""SORA 2.5 seed data — iGRC table, ARC rules, SAIL matrix, mitigations.

Based on EASA/JARUS SORA 2.5 methodology.
Values should be verified against official publications before production use.
"""

# iGRC Dimension Classes (columns of the iGRC table)
# Each column represents a max characteristic dimension + max speed threshold
IGRC_DIMENSION_CLASSES = [
    {"id": 1, "class_label": "<1m & <=25m/s", "max_dimension_m": 1.0, "max_speed_ms": 25.0, "sort_order": 1},
    {"id": 2, "class_label": "<3m & <=35m/s", "max_dimension_m": 3.0, "max_speed_ms": 35.0, "sort_order": 2},
    {"id": 3, "class_label": "<8m & <=75m/s", "max_dimension_m": 8.0, "max_speed_ms": 75.0, "sort_order": 3},
    {"id": 4, "class_label": ">=8m or >75m/s", "max_dimension_m": 999.0, "max_speed_ms": 999.0, "sort_order": 4},
]

# iGRC Population Bands (rows of the iGRC table)
IGRC_POPULATION_BANDS = [
    {"id": 1, "band_label": "Controlled ground area", "max_pop_density": None, "is_controlled": True, "is_assembly": False, "sort_order": 1},
    {"id": 2, "band_label": "Sparsely populated (<250 ppl/km²)", "max_pop_density": 250.0, "is_controlled": False, "is_assembly": False, "sort_order": 2},
    {"id": 3, "band_label": "Populated (250-15000 ppl/km²)", "max_pop_density": 15000.0, "is_controlled": False, "is_assembly": False, "sort_order": 3},
    {"id": 4, "band_label": "Densely populated (>15000 ppl/km²)", "max_pop_density": 999999.0, "is_controlled": False, "is_assembly": False, "sort_order": 4},
    {"id": 5, "band_label": "Assembly of people", "max_pop_density": None, "is_controlled": False, "is_assembly": True, "sort_order": 5},
]

# iGRC Values: dimension_class_id × population_band_id → iGRC value
# Based on SORA 2.5 Table 3
IGRC_VALUES = [
    # Controlled ground area (row 1)
    {"id": 1, "dimension_class_id": 1, "population_band_id": 1, "igrc_value": 1, "is_out_of_scope": False},
    {"id": 2, "dimension_class_id": 2, "population_band_id": 1, "igrc_value": 2, "is_out_of_scope": False},
    {"id": 3, "dimension_class_id": 3, "population_band_id": 1, "igrc_value": 3, "is_out_of_scope": False},
    {"id": 4, "dimension_class_id": 4, "population_band_id": 1, "igrc_value": 4, "is_out_of_scope": False},
    # Sparsely populated (row 2)
    {"id": 5, "dimension_class_id": 1, "population_band_id": 2, "igrc_value": 3, "is_out_of_scope": False},
    {"id": 6, "dimension_class_id": 2, "population_band_id": 2, "igrc_value": 4, "is_out_of_scope": False},
    {"id": 7, "dimension_class_id": 3, "population_band_id": 2, "igrc_value": 5, "is_out_of_scope": False},
    {"id": 8, "dimension_class_id": 4, "population_band_id": 2, "igrc_value": 6, "is_out_of_scope": False},
    # Populated (row 3)
    {"id": 9, "dimension_class_id": 1, "population_band_id": 3, "igrc_value": 5, "is_out_of_scope": False},
    {"id": 10, "dimension_class_id": 2, "population_band_id": 3, "igrc_value": 6, "is_out_of_scope": False},
    {"id": 11, "dimension_class_id": 3, "population_band_id": 3, "igrc_value": 7, "is_out_of_scope": False},
    {"id": 12, "dimension_class_id": 4, "population_band_id": 3, "igrc_value": 8, "is_out_of_scope": False},
    # Densely populated (row 4)
    {"id": 13, "dimension_class_id": 1, "population_band_id": 4, "igrc_value": 7, "is_out_of_scope": False},
    {"id": 14, "dimension_class_id": 2, "population_band_id": 4, "igrc_value": 8, "is_out_of_scope": False},
    {"id": 15, "dimension_class_id": 3, "population_band_id": 4, "igrc_value": 9, "is_out_of_scope": True},
    {"id": 16, "dimension_class_id": 4, "population_band_id": 4, "igrc_value": 10, "is_out_of_scope": True},
    # Assembly of people (row 5)
    {"id": 17, "dimension_class_id": 1, "population_band_id": 5, "igrc_value": 8, "is_out_of_scope": False},
    {"id": 18, "dimension_class_id": 2, "population_band_id": 5, "igrc_value": 9, "is_out_of_scope": True},
    {"id": 19, "dimension_class_id": 3, "population_band_id": 5, "igrc_value": 10, "is_out_of_scope": True},
    {"id": 20, "dimension_class_id": 4, "population_band_id": 5, "igrc_value": 11, "is_out_of_scope": True},
]

# Ground Risk Mitigations
GRC_MITIGATIONS = [
    {"id": 1, "code": "M1A", "name": "Strategic mitigation for ground risk - Sheltering", "description": "Reduction based on the effect of sheltering (buildings, vehicles)", "max_reduction": 2},
    {"id": 2, "code": "M1B", "name": "Strategic mitigation for ground risk - Evaluation of people at risk", "description": "Reduction based on evaluation of the number of people at risk", "max_reduction": 2},
    {"id": 3, "code": "M1C", "name": "Strategic mitigation for ground risk - Containment", "description": "Reduction based on an Emergency Response Plan or technical containment", "max_reduction": 3},
]

GRC_MITIGATION_LEVELS = [
    # M1A: Sheltering
    {"id": 1, "mitigation_id": 1, "robustness": "none", "grc_reduction": 0},
    {"id": 2, "mitigation_id": 1, "robustness": "low", "grc_reduction": 0},
    {"id": 3, "mitigation_id": 1, "robustness": "medium", "grc_reduction": 1},
    {"id": 4, "mitigation_id": 1, "robustness": "high", "grc_reduction": 2},
    # M1B: Evaluation of people at risk
    {"id": 5, "mitigation_id": 2, "robustness": "none", "grc_reduction": 0},
    {"id": 6, "mitigation_id": 2, "robustness": "low", "grc_reduction": 1},
    {"id": 7, "mitigation_id": 2, "robustness": "medium", "grc_reduction": 2},
    {"id": 8, "mitigation_id": 2, "robustness": "high", "grc_reduction": 2},
    # M1C: Containment / ERP
    {"id": 9, "mitigation_id": 3, "robustness": "none", "grc_reduction": 0},
    {"id": 10, "mitigation_id": 3, "robustness": "low", "grc_reduction": 1},
    {"id": 11, "mitigation_id": 3, "robustness": "medium", "grc_reduction": 2},
    {"id": 12, "mitigation_id": 3, "robustness": "high", "grc_reduction": 3},
]

# ARC Initial Rules
# Priority: higher = checked first (most specific wins)
ARC_INITIAL_RULES = [
    # Segregated airspace always gets ARC-a regardless
    {"id": 1, "rule_label": "Segregated airspace below 120m", "airspace_class": None, "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": True, "is_atypical": False, "initial_arc": "ARC-a", "priority": 100},
    {"id": 2, "rule_label": "Segregated airspace 120m-FL600", "airspace_class": None, "altitude_category": "120m_to_FL600", "is_airport_env": False, "is_segregated": True, "is_atypical": False, "initial_arc": "ARC-a", "priority": 100},
    # Airport environment
    {"id": 3, "rule_label": "Airport environment below 120m", "airspace_class": None, "altitude_category": "below_120m", "is_airport_env": True, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-d", "priority": 90},
    {"id": 4, "rule_label": "Airport environment 120m-FL600", "airspace_class": None, "altitude_category": "120m_to_FL600", "is_airport_env": True, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-d", "priority": 90},
    # Controlled airspace (A-E) below 120m
    {"id": 5, "rule_label": "Controlled airspace (A) below 120m", "airspace_class": "A", "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-d", "priority": 50},
    {"id": 6, "rule_label": "Controlled airspace (B) below 120m", "airspace_class": "B", "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-d", "priority": 50},
    {"id": 7, "rule_label": "Controlled airspace (C) below 120m", "airspace_class": "C", "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-c", "priority": 50},
    {"id": 8, "rule_label": "Controlled airspace (D) below 120m", "airspace_class": "D", "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-c", "priority": 50},
    {"id": 9, "rule_label": "Controlled airspace (E) below 120m", "airspace_class": "E", "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-c", "priority": 50},
    # Uncontrolled airspace below 120m
    {"id": 10, "rule_label": "Uncontrolled airspace (F) below 120m", "airspace_class": "F", "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-b", "priority": 30},
    {"id": 11, "rule_label": "Uncontrolled airspace (G) below 120m", "airspace_class": "G", "altitude_category": "below_120m", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-b", "priority": 30},
    # Above 120m, non-segregated — generally ARC-c or ARC-d
    {"id": 12, "rule_label": "Any airspace 120m-FL600 (default)", "airspace_class": None, "altitude_category": "120m_to_FL600", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-c", "priority": 10},
    # Above FL600
    {"id": 13, "rule_label": "Above FL600", "airspace_class": None, "altitude_category": "above_FL600", "is_airport_env": False, "is_segregated": False, "is_atypical": False, "initial_arc": "ARC-d", "priority": 10},
]

# ARC Strategic Mitigations
ARC_STRATEGIC_MITIGATIONS = [
    {"id": 1, "code": "TMPR", "name": "TMPR - Temporal/spatial restrictions", "description": "Operational restrictions on time or space to reduce air risk encounter rate"},
    {"id": 2, "code": "DETECT", "name": "Detect and avoid", "description": "Ability to detect and avoid other airspace users"},
    {"id": 3, "code": "COMMON", "name": "Common structures and rules", "description": "Application of common altitude rules and structures"},
]

ARC_MITIGATION_EFFECTS = [
    # TMPR can reduce ARC-d → ARC-c, ARC-c → ARC-b, ARC-b → ARC-a
    {"id": 1, "mitigation_id": 1, "from_arc": "ARC-d", "to_arc": "ARC-c", "robustness_required": "medium"},
    {"id": 2, "mitigation_id": 1, "from_arc": "ARC-c", "to_arc": "ARC-b", "robustness_required": "medium"},
    {"id": 3, "mitigation_id": 1, "from_arc": "ARC-b", "to_arc": "ARC-a", "robustness_required": "low"},
    # DETECT can reduce one level
    {"id": 4, "mitigation_id": 2, "from_arc": "ARC-d", "to_arc": "ARC-c", "robustness_required": "high"},
    {"id": 5, "mitigation_id": 2, "from_arc": "ARC-c", "to_arc": "ARC-b", "robustness_required": "medium"},
    {"id": 6, "mitigation_id": 2, "from_arc": "ARC-b", "to_arc": "ARC-a", "robustness_required": "low"},
    # COMMON structures
    {"id": 7, "mitigation_id": 3, "from_arc": "ARC-c", "to_arc": "ARC-b", "robustness_required": "medium"},
    {"id": 8, "mitigation_id": 3, "from_arc": "ARC-b", "to_arc": "ARC-a", "robustness_required": "low"},
]

# SAIL Matrix: final_grc × residual_arc → SAIL level
# Based on SORA 2.5 Table 7
SAIL_MATRIX = []
_sail_data = {
    # (grc, arc) → sail
    (1, "ARC-a"): "I", (1, "ARC-b"): "II", (1, "ARC-c"): "IV", (1, "ARC-d"): "VI",
    (2, "ARC-a"): "I", (2, "ARC-b"): "II", (2, "ARC-c"): "IV", (2, "ARC-d"): "VI",
    (3, "ARC-a"): "II", (3, "ARC-b"): "II", (3, "ARC-c"): "IV", (3, "ARC-d"): "VI",
    (4, "ARC-a"): "II", (4, "ARC-b"): "III", (4, "ARC-c"): "IV", (4, "ARC-d"): "VI",
    (5, "ARC-a"): "III", (5, "ARC-b"): "III", (5, "ARC-c"): "IV", (5, "ARC-d"): "VI",
    (6, "ARC-a"): "III", (6, "ARC-b"): "IV", (6, "ARC-c"): "V", (6, "ARC-d"): "VI",
    (7, "ARC-a"): "IV", (7, "ARC-b"): "IV", (7, "ARC-c"): "V", (7, "ARC-d"): "VI",
}
for i, ((grc, arc), sail) in enumerate(_sail_data.items(), 1):
    SAIL_MATRIX.append({"id": i, "final_grc": grc, "residual_arc": arc, "sail_level": sail})
