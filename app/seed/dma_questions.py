"""DMA (Drone Maturity Assessment) dimensions and questions.

Dimensions cover the key areas municipalities/organizations need to
mature across to run an effective drone program.
"""

DMA_DIMENSIONS = [
    {"id": 1, "code": "OPS", "name": "Operations", "description": "Operational readiness, SOPs, and flight management", "weight": 1.0, "sort_order": 1},
    {"id": 2, "code": "TECH", "name": "Technology", "description": "Fleet management, maintenance, and technical infrastructure", "weight": 1.0, "sort_order": 2},
    {"id": 3, "code": "SAFE", "name": "Safety Management", "description": "Safety management system, hazard identification, and safety culture", "weight": 1.2, "sort_order": 3},
    {"id": 4, "code": "COMP", "name": "Regulatory Compliance", "description": "Understanding and adherence to drone regulations and SORA", "weight": 1.2, "sort_order": 4},
    {"id": 5, "code": "HR", "name": "Human Resources", "description": "Pilot competency, training, and crew management", "weight": 1.0, "sort_order": 5},
    {"id": 6, "code": "DATA", "name": "Data & Documentation", "description": "Data management, record keeping, and audit readiness", "weight": 0.8, "sort_order": 6},
]

DMA_QUESTIONS = [
    # Operations
    {"dimension_id": 1, "question_code": "OPS_01", "question_text": "Does the organization have documented Standard Operating Procedures (SOPs) for drone operations?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 1},
    {"dimension_id": 1, "question_code": "OPS_02", "question_text": "Is a pre-flight checklist consistently used before every operation?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 2},
    {"dimension_id": 1, "question_code": "OPS_03", "question_text": "Are post-flight debriefings conducted and documented?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 3},
    {"dimension_id": 1, "question_code": "OPS_04", "question_text": "Is there a formal process for mission planning including risk assessment?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 4},
    {"dimension_id": 1, "question_code": "OPS_05", "question_text": "Does the organization track and analyze operational metrics (flight hours, incidents, etc.)?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 5},
    # Technology
    {"dimension_id": 2, "question_code": "TECH_01", "question_text": "Is there a fleet maintenance program with scheduled inspections?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 6},
    {"dimension_id": 2, "question_code": "TECH_02", "question_text": "Are firmware/software updates managed systematically across the fleet?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 7},
    {"dimension_id": 2, "question_code": "TECH_03", "question_text": "Does the organization have redundancy systems (backup drones, spare parts)?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 8},
    {"dimension_id": 2, "question_code": "TECH_04", "question_text": "Are appropriate payload/sensor capabilities matched to mission requirements?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 9},
    {"dimension_id": 2, "question_code": "TECH_05", "question_text": "Is there a defined process for evaluating and procuring new drone technology?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 10},
    # Safety Management
    {"dimension_id": 3, "question_code": "SAFE_01", "question_text": "Does the organization have a Safety Management System (SMS) in place?", "answer_type": "scale", "weight": 1.5, "max_score": 5, "sort_order": 11},
    {"dimension_id": 3, "question_code": "SAFE_02", "question_text": "Is there a formal hazard identification and risk assessment process?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 12},
    {"dimension_id": 3, "question_code": "SAFE_03", "question_text": "Are incidents and near-misses reported, investigated, and learnings shared?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 13},
    {"dimension_id": 3, "question_code": "SAFE_04", "question_text": "Is there an Emergency Response Plan (ERP) that is regularly tested?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 14},
    {"dimension_id": 3, "question_code": "SAFE_05", "question_text": "Does leadership actively promote a safety-first culture?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 15},
    # Regulatory Compliance
    {"dimension_id": 4, "question_code": "COMP_01", "question_text": "Does the organization understand the applicable drone regulatory framework (EU/national)?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 16},
    {"dimension_id": 4, "question_code": "COMP_02", "question_text": "Has the organization completed SORA assessments for its specific operations?", "answer_type": "scale", "weight": 1.5, "max_score": 5, "sort_order": 17},
    {"dimension_id": 4, "question_code": "COMP_03", "question_text": "Is there a documented Concept of Operations (ConOps)?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 18},
    {"dimension_id": 4, "question_code": "COMP_04", "question_text": "Does the organization maintain current operator registrations and authorizations?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 19},
    {"dimension_id": 4, "question_code": "COMP_05", "question_text": "Is there a process for tracking regulatory changes and updating procedures accordingly?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 20},
    # Human Resources
    {"dimension_id": 5, "question_code": "HR_01", "question_text": "Are all remote pilots certified/qualified per applicable regulations?", "answer_type": "scale", "weight": 1.5, "max_score": 5, "sort_order": 21},
    {"dimension_id": 5, "question_code": "HR_02", "question_text": "Is there a recurrent training and proficiency checking program?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 22},
    {"dimension_id": 5, "question_code": "HR_03", "question_text": "Are crew resource management (CRM) principles applied?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 23},
    {"dimension_id": 5, "question_code": "HR_04", "question_text": "Is there a competency assessment framework for different operation types?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 24},
    {"dimension_id": 5, "question_code": "HR_05", "question_text": "Are fitness-to-fly assessments conducted before operations?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 25},
    # Data & Documentation
    {"dimension_id": 6, "question_code": "DATA_01", "question_text": "Are flight logs maintained with sufficient detail for regulatory compliance?", "answer_type": "scale", "weight": 1.2, "max_score": 5, "sort_order": 26},
    {"dimension_id": 6, "question_code": "DATA_02", "question_text": "Is there a data backup and retention policy for operational records?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 27},
    {"dimension_id": 6, "question_code": "DATA_03", "question_text": "Are maintenance records tracked and linked to specific airframes?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 28},
    {"dimension_id": 6, "question_code": "DATA_04", "question_text": "Is there an audit trail for operational decisions and approvals?", "answer_type": "scale", "weight": 1.0, "max_score": 5, "sort_order": 29},
    {"dimension_id": 6, "question_code": "DATA_05", "question_text": "Does the organization use a digital platform for managing drone operations data?", "answer_type": "scale", "weight": 0.8, "max_score": 5, "sort_order": 30},
]
