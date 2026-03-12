"""Norway-specific CAA (Luftfartstilsynet) rules and overrides.

Based on Norwegian implementation of EU drone regulations and SORA.
"""

NORWAY_COUNTRY = {
    "id": 1,
    "code": "NO",
    "name": "Norway",
    "regulatory_body": "Luftfartstilsynet (Norwegian Civil Aviation Authority)",
    "sora_version": "2.5",
    "notes": "Norway follows EASA regulations as an EEA member. Additional national requirements apply for operations in certain zones.",
}

# Norway-specific rule overrides
NORWAY_RULES = [
    {
        "country_id": 1,
        "rule_type": "additional_requirement",
        "rule_key": "bvlos_notification",
        "rule_value": {"requirement": "Luftfartstilsynet must be notified for BVLOS operations in specific category"},
        "description": "BVLOS operations in specific category require notification to the Norwegian CAA",
        "effective_from": None,
        "effective_to": None,
    },
    {
        "country_id": 1,
        "rule_type": "additional_requirement",
        "rule_key": "no_fly_zones",
        "rule_value": {
            "requirement": "Operations prohibited within airport CTR without ATC clearance",
            "zones": ["airport_ctr", "military_areas", "national_parks_restricted"],
        },
        "description": "Norwegian no-fly zones and restricted areas - ATC coordination required",
        "effective_from": None,
        "effective_to": None,
    },
    {
        "country_id": 1,
        "rule_type": "additional_requirement",
        "rule_key": "sts_01_available",
        "rule_value": {
            "standard_scenario": "STS-01",
            "description": "VLOS over controlled ground area in populated environment",
            "max_height_m": 120,
            "max_dimension_m": 3,
            "max_mtom_kg": 25,
        },
        "description": "Standard Scenario STS-01 available in Norway - bypasses full SORA for qualifying operations",
        "effective_from": None,
        "effective_to": None,
    },
    {
        "country_id": 1,
        "rule_type": "additional_requirement",
        "rule_key": "sts_02_available",
        "rule_value": {
            "standard_scenario": "STS-02",
            "description": "BVLOS with airspace observer over sparsely populated area",
            "max_height_m": 120,
            "max_dimension_m": 3,
            "max_mtom_kg": 25,
            "max_range_m": 2000,
        },
        "description": "Standard Scenario STS-02 available in Norway - BVLOS with airspace observer",
        "effective_from": None,
        "effective_to": None,
    },
    {
        "country_id": 1,
        "rule_type": "additional_requirement",
        "rule_key": "insurance",
        "rule_value": {"requirement": "Third-party liability insurance is mandatory for all drone operations"},
        "description": "Insurance requirement per Norwegian/EU regulation",
        "effective_from": None,
        "effective_to": None,
    },
    {
        "country_id": 1,
        "rule_type": "additional_requirement",
        "rule_key": "registration",
        "rule_value": {"requirement": "All UAS operators must register with Luftfartstilsynet via Flydrone.no"},
        "description": "Operator registration requirement",
        "effective_from": None,
        "effective_to": None,
    },
]
