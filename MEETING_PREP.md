# Meeting Prep: Drone Regulatory Compliance Platform
## Client: Gunhild Fretheim | Meeting: March 12, 2026

---

## Project Overview

We are building a **Drone Regulatory Compliance Platform** — a full-stack SaaS product that helps drone operators, municipalities, and consultants navigate the complex EASA regulatory framework. The platform has two core modules:

1. **SORA Builder** — An automated SORA 2.5 (Specific Operations Risk Assessment) calculation engine
2. **DMA (Drone Maturity Assessment)** — An organizational readiness scoring tool

The system is designed to be **data-driven** — all regulatory matrices, rules, and scoring logic live in the database, not in code. This means regulations can be updated by domain experts without developer involvement, and the platform can scale to support multiple countries and regulatory versions.

---

## Module 1: SORA Builder

### What is SORA?
SORA (Specific Operations Risk Assessment) is the EASA/JARUS methodology for assessing drone operations in the "Specific" category. It produces a structured risk assessment that determines what safety requirements an operator must meet.

### What our engine does (full pipeline):

**Step 1 — Intrinsic Ground Risk Class (iGRC)**
- Takes drone specifications (MTOM, characteristic dimension, max speed) and operational context (population density, controlled ground, assembly of people)
- Looks up the iGRC value from a 4x5 matrix (4 drone dimension classes x 5 population bands)
- Dimension classes: `<1m & <=25m/s`, `<3m & <=35m/s`, `<8m & <=75m/s`, `>=8m or >75m/s`
- Population bands: Controlled ground, Sparsely populated (<250 ppl/km2), Populated (250-15,000), Densely populated (>15,000), Assembly of people
- iGRC values range from 1-11, with certain combinations flagged as "out of SORA scope"

**Step 2 — Ground Risk Mitigations (GRC)**
- Three mitigations can reduce the iGRC:
  - **M1A** — Sheltering (buildings, vehicles) — up to -2 at high robustness
  - **M1B** — Evaluation of people at risk — up to -2 at medium/high robustness
  - **M1C** — Containment / ERP — up to -3 at high robustness
- Each mitigation has four robustness levels: none, low, medium, high
- Final GRC = iGRC minus total mitigation reductions (minimum 1)

**Step 3 — Air Risk Class (ARC)**
- Determined by airspace classification, altitude, and operational context
- 13 priority-ordered rules covering:
  - Segregated airspace (always ARC-a)
  - Airport environment (ARC-d)
  - Controlled airspace A-E below 120m (ARC-c to ARC-d)
  - Uncontrolled airspace F-G below 120m (ARC-b)
  - Above 120m and above FL600 defaults
- ARC levels: ARC-a (lowest risk) through ARC-d (highest risk)

**Step 4 — Strategic Air Mitigations**
- Three strategic mitigations can reduce the ARC:
  - **TMPR** — Temporal/spatial restrictions
  - **DETECT** — Detect and avoid capability
  - **COMMON** — Common structures and rules
- Each can step down the ARC by one level depending on robustness

**Step 5 — SAIL Determination**
- SAIL (Specific Assurance and Integrity Level) is determined by a 7x4 matrix: Final GRC (1-7) x Residual ARC (a-d)
- Produces SAIL levels I through VI
- Example: GRC 3 + ARC-b = SAIL II; GRC 5 + ARC-c = SAIL IV

**Step 6 — OSO Mapping**
- All 24 Operational Safety Objectives are mapped with required robustness per SAIL level
- Robustness levels: O (Optional), L (Low), M (Medium), H (High)
- Categories: Operator, Technical, Human Factors, Third Party
- OSOs cover everything from operator competency to UAS design to environmental conditions

**Step 7 — Country-Specific CAA Overrides**
- Currently implemented for **Norway (Luftfartstilsynet)**
- Override types: additional requirements, minimum SAIL adjustments, GRC adjustments
- Norway-specific rules include:
  - BVLOS notification requirements
  - No-fly zone framework (airport CTR, military areas, national parks)
  - Standard Scenarios STS-01 and STS-02 availability
  - Mandatory third-party liability insurance
  - Operator registration via Flydrone.no
- Date-aware effective_from/effective_to fields support rule versioning
- Architecture supports adding any EASA member state or third country

### API Endpoints (SORA):
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sora/calculate` | Full SORA assessment (end-to-end) |
| POST | `/api/v1/sora/grc` | GRC-only calculation |
| POST | `/api/v1/sora/arc` | ARC-only calculation |
| GET | `/api/v1/sora/sail-matrix` | Full SAIL lookup table |
| GET | `/api/v1/sora/osos` | All 24 OSOs with descriptions |
| GET | `/api/v1/sora/osos/{sail_level}` | OSOs filtered by SAIL level |

---

## Module 2: DMA (Drone Maturity Assessment)

### What it does
A structured assessment tool for organizations (primarily municipalities) to evaluate their readiness to establish or scale a drone program. Inspired by CMMI-style maturity models.

### 6 Assessment Dimensions:

| Code | Dimension | Weight | Focus Area |
|------|-----------|--------|------------|
| OPS | Operations | 1.0 | SOPs, pre/post-flight procedures, mission planning, operational metrics |
| TECH | Technology | 1.0 | Fleet maintenance, firmware management, redundancy, procurement |
| SAFE | Safety Management | 1.2 | SMS, hazard ID, incident reporting, ERP, safety culture |
| COMP | Regulatory Compliance | 1.2 | Regulatory framework understanding, SORA assessments, ConOps, registrations |
| HR | Human Resources | 1.0 | Pilot certification, recurrent training, CRM, competency assessment, fitness-to-fly |
| DATA | Data & Documentation | 0.8 | Flight logs, data retention, maintenance records, audit trails, digital platforms |

Note: Safety and Compliance are weighted higher (1.2x) because they are the most critical for regulatory approval. Data is weighted lower (0.8x) as it's a supporting function.

### 30 Questions (5 per dimension)
Each question is scored on a 1-5 scale and individually weighted within its dimension. Examples:
- "Does the organization have a Safety Management System (SMS) in place?" (SAFE_01, weight 1.5)
- "Has the organization completed SORA assessments for its specific operations?" (COMP_02, weight 1.5)
- "Are all remote pilots certified/qualified per applicable regulations?" (HR_01, weight 1.5)

### Scoring Engine:
- Per-dimension: Weighted average of question scores, normalized to 0-5 scale, converted to percentage
- Overall: Weighted average across all dimensions using dimension weights
- **5 Maturity Levels:**
  - **Initial** (0-29%) — Ad-hoc, no formal processes
  - **Managed** (30-49%) — Basic processes exist but inconsistent
  - **Defined** (50-69%) — Processes documented and standardized
  - **Measured** (70-89%) — Processes measured and controlled
  - **Optimized** (90-100%) — Continuous improvement, industry-leading

### Recommendations Engine:
- Automatically generates improvement recommendations for dimensions scoring below 70%
- Dimensions below 50% flagged as "significant improvement needed"
- Dimensions 50-70% flagged as "moderate maturity — consider formalizing"

### API Endpoints (DMA):
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dma/dimensions` | List all assessment dimensions |
| GET | `/api/v1/dma/questions` | List all questions (filterable by dimension) |
| POST | `/api/v1/dma/assess` | Submit responses and get scored results |
| GET | `/api/v1/dma/assessments/{id}` | Retrieve a saved assessment |

---

## Technical Architecture

### Stack
- **Language:** Python 3.13
- **Framework:** FastAPI (async, high-performance)
- **ORM:** SQLAlchemy 2.0 (async with mapped_column)
- **Validation:** Pydantic v2 with model validators
- **Database:** PostgreSQL (production) / SQLite (development)
- **Hosting:** Supabase-ready (PostgreSQL-native)
- **Testing:** pytest + pytest-asyncio (20 tests, all passing)

### Database Schema (15 tables)

**SORA Module (10 tables):**
- `igrc_dimension_classes` — 4 drone size/speed classes
- `igrc_population_bands` — 5 population density bands
- `igrc_values` — 20 intersection values (the iGRC lookup table)
- `grc_mitigations` — 3 ground risk mitigations (M1A, M1B, M1C)
- `grc_mitigation_levels` — 12 robustness/reduction mappings
- `arc_initial_rules` — 13 priority-ordered ARC determination rules
- `arc_strategic_mitigations` — 3 strategic air mitigations
- `arc_mitigation_effects` — 8 ARC reduction mappings
- `sail_matrix` — 28 GRC x ARC = SAIL entries
- `oso_catalogue` + `oso_sail_requirements` — 24 OSOs x 6 SAIL levels = 144 robustness entries

**CAA Module (2 tables):**
- `countries` — Country registry with regulatory body info
- `caa_rule_overrides` — Country-specific rules with date-based versioning

**DMA Module (3 tables):**
- `dma_dimensions` — 6 assessment dimensions with weights
- `dma_questions` — 30 questions with individual weights
- `dma_assessments` — Saved assessment results (UUID-keyed, JSON scores)

**Supporting (1 table):**
- `drone_models` — Drone specifications registry (MTOM, dimensions, speed, manufacturer)

### Key Design Decisions:
1. **Data-driven rules engine** — All SORA matrices and regulatory rules stored in DB, not code. Domain experts can update regulatory data without code changes.
2. **Idempotent seeding** — Seed runner uses upsert logic, safe to re-run without duplicating data.
3. **Country-extensible** — Adding a new country's rules requires only new seed data, no code changes.
4. **SORA version-aware** — Schema tracks which SORA version each country uses.
5. **Normalized schema** — iGRC table decomposed into dimension classes x population bands, enabling granular updates.
6. **Separation of concerns** — Each calculation step (GRC, ARC, SAIL, OSO, CAA) is an independent service module.

### Service Architecture:
```
sora_engine.py (orchestrator)
  |-- grc_calculator.py    (iGRC lookup + ground mitigations)
  |-- arc_calculator.py    (ARC rules + strategic mitigations)
  |-- sail_calculator.py   (SAIL matrix lookup)
  |-- oso_mapper.py        (OSO requirements per SAIL)
  |-- caa_service.py       (country-specific overrides)

dma_scorer.py (standalone)
  |-- weighted scoring engine
  |-- maturity level determination
  |-- recommendation generation
```

---

## Answers to Client's Call Agenda

### 1) What we built the prior compliance engine for and roughly how similar it is to this

We have experience building **data-driven rules engines** where business logic is stored entirely in database tables, not hardcoded. The architectural pattern is directly applicable:

- Structured inputs flow through a multi-step calculation pipeline
- Each step references lookup tables and regulatory matrices in the database
- Mitigations/adjustments are applied through configurable rules
- The output is a fully traceable result with every intermediate step visible
- Rules can be versioned, country-specific, and date-bounded

The SORA engine follows this exact pattern: drone specs + operational context go in, and out comes a complete risk assessment with iGRC, GRC, ARC, SAIL, and OSO determinations — all derived from database-stored matrices that can be updated independently of the application code.

The similarity to SORA specifically:
- Both involve multi-dimensional matrix lookups (iGRC table = dimension class x population band)
- Both apply cascading mitigations that modify scores (ground mitigations, strategic air mitigations)
- Both produce compliance-mapped outputs (OSOs mapped to SAIL levels, like control requirements mapped to risk levels)
- Both need country/jurisdiction-specific rule layers on top of a base framework

### 2) A quick look at the SORA prototype

The working prototype is available to demo live. It includes:

- **Full SORA 2.5 pipeline** running end-to-end: input drone specs and operational scenario, get complete risk assessment
- **Interactive web UI** for demonstration — dark-themed, professional interface with both SORA Builder and DMA Assessment tabs
- **All 24 OSOs** with proper robustness levels mapped per SAIL level
- **Norway/Luftfartstilsynet CAA rules** pre-loaded (BVLOS, STS-01/02, insurance, registration, no-fly zones)
- **DMA scoring** with 30 questions across 6 weighted dimensions, automated maturity classification
- **Live API** with Swagger/OpenAPI documentation at `/docs`

Demo scenarios to show:
1. Small drone (<1m, 2kg) in sparsely populated area, Class G airspace → SAIL II (low risk)
2. Medium drone with ground mitigations applied → reduced GRC → lower SAIL
3. Airport environment scenario → ARC-d → high SAIL
4. Large drone over assembly → out-of-scope warning
5. DMA assessment showing dimensional scoring and maturity levels

### 3) Stack preference and any questions on the spec

**Our stack (aligned with client requirements):**
- **Python + FastAPI** — Async, high-performance, automatic OpenAPI docs, industry-standard for data-heavy backends
- **PostgreSQL** — Production database, perfect for complex relational data with JSON fields for flexible rule values
- **SQLAlchemy 2.0** — Modern async ORM, type-safe mapped columns, clean migration path with Alembic
- **Pydantic v2** — Strict data validation at API boundaries, automatic serialization
- **Supabase** — PostgreSQL hosting with built-in auth, storage, and real-time capabilities ready for future phases

**Questions for the spec discussion:**
1. **SORA matrix values** — We've implemented based on publicly available SORA 2.5 materials. Does the client have specific matrix values they want verified or adjusted? Any proprietary interpretation of edge cases?
2. **DMA customization** — The 30 questions and 6 dimensions are our initial framework. Does the client want to customize questions per municipality or keep a standard set?
3. **Multi-country timeline** — We've built Norway first. What's the priority order for additional countries? (Different EASA member states may have unique CAA rules.)
4. **SORA version handling** — When SORA 3.0 or updates come, the data-driven design means we update database records. Does the client need to support running assessments against multiple SORA versions simultaneously?
5. **User workflow** — Is the SORA assessment a one-shot calculation, or do operators need to save drafts, iterate on mitigations, and compare scenarios side-by-side?
6. **Integration points** — Does the client plan to integrate with external systems (Flydrone.no, ATC systems, GIS/map services for population density)?
7. **DMA reporting** — Beyond scoring, does the client need PDF report generation, historical trend tracking, or benchmark comparisons across municipalities?
8. **Standard Scenarios** — STS-01 and STS-02 are flagged in Norway rules. Should the platform detect when an operation qualifies for a Standard Scenario and bypass full SORA?

### 4) Time estimate and budget

**Phase 1 — MVP Backend (Current prototype → Production-ready): 3-4 weeks**
- Finalize SORA matrix values against client's verified spec
- Migrate from SQLite to PostgreSQL/Supabase
- Add Alembic migration framework
- Authentication and authorization (JWT/Supabase Auth)
- Input validation hardening and edge case handling
- Comprehensive test coverage (target: 90%+)
- API documentation and endpoint finalization
- Deployment to Supabase + cloud hosting

**Phase 2 — Extended Backend Features: 2-3 weeks**
- Multi-country CAA rule support (beyond Norway)
- Assessment history, versioning, and comparison
- PDF report generation for SORA assessments and DMA results
- Drone model registry with specification management
- Batch assessment capabilities
- Webhook/notification system for rule updates

**Phase 3 — Frontend & UX (if needed): 3-4 weeks**
- Production React/Next.js frontend (replacing demo UI)
- SORA Builder wizard with step-by-step flow
- DMA questionnaire with progress saving
- Dashboard with analytics and visualizations
- Responsive design for tablet use in field

**Phase 4 — Advanced Features: 2-3 weeks**
- Standard Scenario detection (STS-01, STS-02)
- GIS integration for population density lookup
- Operational approval workflow
- Audit logging and compliance reporting
- Multi-tenant support for consulting firms

**Total estimated timeline: 10-14 weeks for the complete platform**

Budget should be discussed based on:
- Which phases the client wants to commit to initially
- Whether frontend is in scope or handled separately
- Ongoing maintenance and regulatory update support
- Hosting and infrastructure costs (Supabase plan selection)

---

## What's Already Built (Prototype Status)

| Component | Status | Details |
|-----------|--------|---------|
| Database schema | Done | 15 tables, fully normalized |
| SORA iGRC lookup | Done | 4x5 matrix, data-driven |
| GRC mitigations | Done | M1A, M1B, M1C with 4 robustness levels |
| ARC determination | Done | 13 priority-ordered rules |
| ARC strategic mitigations | Done | TMPR, DETECT, COMMON |
| SAIL matrix | Done | 28 entries (GRC 1-7 x ARC a-d) |
| OSO mapping | Done | All 24 OSOs, 144 SAIL-level entries |
| Norway CAA rules | Done | 6 rules (BVLOS, STS, insurance, registration, no-fly) |
| DMA dimensions | Done | 6 dimensions with weights |
| DMA questions | Done | 30 questions with individual weights |
| DMA scoring engine | Done | Weighted scoring, maturity levels, recommendations |
| REST API | Done | 14 endpoints across 4 modules |
| Seed data runner | Done | Idempotent, all reference data loaded |
| Test suite | Done | 20 tests, all passing |
| Demo UI | Done | Interactive single-page app for demonstration |
| Auth system | Not started | Planned for Phase 1 |
| Alembic migrations | Not started | Planned for Phase 1 |
| PDF reports | Not started | Planned for Phase 2 |
| Production frontend | Not started | Planned for Phase 3 |

---

## Key Differentiators of Our Approach

1. **Data-driven, not hardcoded** — Regulatory matrices live in the database. When EASA updates a value, we update a row, not rewrite code.
2. **Country-extensible from day one** — Adding Sweden, Denmark, or any EASA state is a seed data exercise, not an architecture change.
3. **Full traceability** — Every SORA calculation returns the complete chain: iGRC value, each mitigation applied, GRC reduction, ARC rule matched, SAIL determination, and all 24 OSO requirements.
4. **Production architecture** — Not a throwaway prototype. Clean separation of concerns, async throughout, type-safe, tested, and ready to build on.
5. **Domain alignment** — Built specifically for drone regulatory compliance, not a generic rules engine repurposed.
