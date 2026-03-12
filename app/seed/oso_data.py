"""OSO catalogue and robustness requirements per SAIL level.

All 24 OSOs from SORA 2.5 with required robustness (O=Optional, L=Low, M=Medium, H=High)
per SAIL level (I through VI).

Values should be verified against official SORA 2.5 Annex E before production use.
"""

OSO_CATALOGUE = [
    {"oso_number": 1, "title": "Ensure the operator is competent and/or proven", "category": "operator"},
    {"oso_number": 2, "title": "UAS manufactured by competent and/or proven entity", "category": "technical"},
    {"oso_number": 3, "title": "UAS maintained by competent and/or proven entity", "category": "technical"},
    {"oso_number": 4, "title": "UAS developed to design standards", "category": "technical"},
    {"oso_number": 5, "title": "UAS is designed considering system safety and reliability", "category": "technical"},
    {"oso_number": 6, "title": "C3 link performance is adequate", "category": "technical"},
    {"oso_number": 7, "title": "Inspection of the UAS (product inspection) to ensure consistency to the approved design", "category": "technical"},
    {"oso_number": 8, "title": "Operational procedures are defined, validated and adhered to", "category": "operator"},
    {"oso_number": 9, "title": "Remote crew trained and current and able to control the abnormal situation", "category": "human_factors"},
    {"oso_number": 10, "title": "Safe recovery from technical issue", "category": "technical"},
    {"oso_number": 11, "title": "Procedures are in-place to handle adverse operating conditions", "category": "operator"},
    {"oso_number": 12, "title": "The UAS is designed to manage the deterioration of external systems supporting UAS operation", "category": "technical"},
    {"oso_number": 13, "title": "External services supporting UAS operations are adequate to the operation", "category": "operator"},
    {"oso_number": 14, "title": "Operational volume is defined appropriately and considers necessary risk buffers", "category": "operator"},
    {"oso_number": 15, "title": "An adequate Emergency Response Plan (ERP) is in place, validated and implemented", "category": "operator"},
    {"oso_number": 16, "title": "Multi-crew coordination is adequate", "category": "human_factors"},
    {"oso_number": 17, "title": "Remote crew is fit to operate", "category": "human_factors"},
    {"oso_number": 18, "title": "Automatic protection of the flight envelope from human errors", "category": "human_factors"},
    {"oso_number": 19, "title": "Safe design and target level of robustness for ground risk mitigation", "category": "technical"},
    {"oso_number": 20, "title": "A Human Factors evaluation has been performed and the HMI found adequate", "category": "human_factors"},
    {"oso_number": 21, "title": "Adequate containment in place for BVLOS operations", "category": "technical"},
    {"oso_number": 22, "title": "The applicant takes due account of other airspace users for collision avoidance", "category": "third_party"},
    {"oso_number": 23, "title": "Environmental conditions for safe operations are defined, measurable and adhered to", "category": "operator"},
    {"oso_number": 24, "title": "UAS designed and qualified for adverse environmental conditions", "category": "technical"},
]

# OSO robustness requirements per SAIL level
# Format: {oso_number: {"I": "O/L/M/H", "II": ..., ..., "VI": ...}}
# O=Optional, L=Low, M=Medium, H=High
OSO_REQUIREMENTS_BY_SAIL = {
    1:  {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    2:  {"I": "O", "II": "O", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    3:  {"I": "O", "II": "L", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    4:  {"I": "O", "II": "O", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    5:  {"I": "O", "II": "O", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    6:  {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    7:  {"I": "O", "II": "O", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    8:  {"I": "L", "II": "M", "III": "H", "IV": "H", "V": "H", "VI": "H"},
    9:  {"I": "L", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    10: {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    11: {"I": "L", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    12: {"I": "O", "II": "L", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    13: {"I": "O", "II": "L", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    14: {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    15: {"I": "L", "II": "M", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    16: {"I": "O", "II": "L", "III": "M", "IV": "M", "V": "H", "VI": "H"},
    17: {"I": "L", "II": "L", "III": "M", "IV": "M", "V": "H", "VI": "H"},
    18: {"I": "O", "II": "O", "III": "L", "IV": "M", "V": "H", "VI": "H"},
    19: {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    20: {"I": "O", "II": "O", "III": "L", "IV": "M", "V": "M", "VI": "H"},
    21: {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    22: {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    23: {"I": "L", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
    24: {"I": "O", "II": "L", "III": "M", "IV": "H", "V": "H", "VI": "H"},
}
