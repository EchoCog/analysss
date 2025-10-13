# Entity Relation Updates - Evidence Package 2025-08-11

## Document Purpose
This document updates entity profiles and relationships based on the trustee appointment letter and August 2025 email evidence package.

---

## New Entity: The Faucitt Family Trust

### Entity Details
- **Entity Type**: Trust
- **Legal Name**: The Faucitt Family Trust
- **Registration Number**: IT 3651/2013
- **Tax Number**: 9132219271
- **Main Trustee**: Peter Andrew Faucitt (appointed July 1, 2025 - backdated)
- **Appointing Parties**: Peter Andrew Faucitt, Jacqueline Faucitt
- **Actual Appointment Date**: August 11, 2025 (41-day backdate)

### Agent Properties
```

json
{
  "entity_type": "trust",
  "legal_aggression": 0.9,
  "control_seeking": 1.0,
  "evidence_dismissal": 0.9,
  "vulnerability_to_pressure": 0.1,
  "ethical_compliance": 0.1,
  "information_control": 0.8,
  "asset_protection_priority": 1.0
}
```

### Strategic Goals
1. Consolidate asset control under Peter's exclusive authority
2. Provide legal structure for asset protection from claims
3. Facilitate asset transfers from other entities (RST, Villa Via)
4. Create legal barrier to Dan/Jax asset recovery
5. Backdate appointment to coincide with other sabotage activities

### Behavioral Rules
- IF assets at risk THEN transfer to trust structure


- IF legal challenge threatened THEN claim trust protection
- IF questioned about timing THEN cite backdated appointment date (July 1)
- IF asset transfer needed THEN use trustee authority
- IF beneficiary questions raised THEN maintain opacity

### Relationships
- **Peter Andrew Faucitt**: 1.0 (trustee, primary beneficiary likely)
- **Jacqueline Faucitt**: 0.5 (co-signatory, potential duress)
- **Daniel Faucitt**: -1.0 (excluded, adversarial, asset claims threat)
- **Villa Via**: 0.9 (likely trust asset or beneficiary)
- **RST (Regima Skin Treatments)**: 0.9 (likely trust asset or beneficiary)
- **Rynette**: 0.9 (facilitates trustee appointment documentation)
- **Bantjies**: 0.8 (receives trustee appointment, aware of Peter's authority)

### Evidence Sources
- LetterofAppointment11082025.pdf
- Phishing_*.eml (email chain)

---

## Updated Entity: Rynette (Bookkeeper)

### Previous Profile
- **Role**: Bookkeeper for all entities
- **Information Control**: Exclusive access to financial systems
- **Coordination**: With Pete on sabotage activities

### New Evidence (August 2025)
- Sends trustee appointment to Bantjies (August 11, 2025, 11:00 UTC)
- Allocates computer expenses for Bantjies review (March-April 2025)
- Copied on trustee appointment email
- Controls information flow to accountant

### Updated Agent Properties
```json
{
  "legal_aggression": 0.85,
  "control_seeking": 0.95,
  "evidence_dismissal": 0.9,
  "vulnerability_to_pressure": 0.3,
  "ethical_compliance": 0.1,
  "information_control": 1.0,
  "coordination_capability": 0.95
}
```

**Changes from Previous**:
- Legal Aggression: 0.8 → 0.85 (facilitates legal documentation)
- Control Seeking: 0.9 → 0.95 (controls accountant information)
- Information Control: 0.95 → 1.0 (exclusive gatekeeper to Bantjies)

### New Strategic Goals
- Control all information flow to Bantjies (accountant)
- Facilitate Peter's trustee appointment documentation
- Allocate computer expenses to maximize Dan's burden
- Coordinate timing of legal/financial actions with Pete
- Maintain exclusive access to financial systems

### New Behavioral Rules
- IF legal document needed THEN coordinate with Pete and send to Bantjies
- IF accountant requests information THEN provide filtered data only
- IF computer expenses questioned THEN allocate maximum to Dan's entities
- IF trustee appointment needed THEN facilitate documentation and distribution
- IF timing coordination needed THEN synchronize with Pete's legal actions

### New Relationships
- **The Faucitt Family Trust**: 0.9 (facilitates trustee appointment)
- **Bantjies**: 0.9 (information provider, coordination, gatekeeper)

---

## Updated Entity: Danie Bantjies (Accountant)

### Previous Profile
- **Role**: Accountant/Auditor for RegimA entities
- **Conflict**: Received June 10 murder/fraud report, avoided investigation
- **Perjury**: Provided affidavit for Peter's August 14/19 interdict

### New Evidence (August 2025)
- Receives trustee appointment August 11, 2025 (from Rynette)
- Requests computer expense justification August 27, 2025
- Claims impartiality 16 days after receiving Peter's trustee appointment
- Relies on Rynette's expense allocations without independent verification
- Threatens SARS audit to pressure Dan
- Continues "Regima Group of Companies" framing

### Updated Agent Properties
```json
{
  "legal_aggression": 0.75,
  "control_seeking": 0.7,
  "evidence_dismissal": 0.85,
  "vulnerability_to_pressure": 0.4,
  "ethical_compliance": 0.15,
  "information_dependency": 0.9,
  "professional_misconduct": 0.9
}
```

**Changes from Previous**:
- Legal Aggression: 0.7 → 0.75 (SARS audit threat)
- Control Seeking: 0.6 → 0.7 (requests detailed justifications)
- Evidence Dismissal: 0.8 → 0.85 (ignores trustee appointment conflict)
- Ethical Compliance: 0.2 → 0.15 (false impartiality claim)
- Information Dependency: NEW 0.9 (relies on Rynette's filtered data)
- Professional Misconduct: NEW 0.9 (false impartiality, SARS threat)

### New Strategic Goals
- Maintain appearance of impartiality while coordinating with Peter/Rynette
- Use SARS audit threat to pressure Dan on computer expenses
- Rely on Rynette's filtered information exclusively
- Continue "Group" framing to facilitate profit extraction concealment
- Provide professional cover for Peter's actions

### New Behavioral Rules
- IF trustee appointment received THEN claim impartiality anyway
- IF computer expenses questioned THEN request detailed justifications from Dan only
- IF information needed THEN rely on Rynette's allocations without verification
- IF challenged THEN invoke SARS audit threat
- IF Dan provides evidence THEN dismiss or avoid investigation
- IF Peter needs support THEN provide professional affidavits

### New Relationships
- **The Faucitt Family Trust**: 0.8 (received trustee appointment, aware of Peter's authority)
- **Rynette**: 0.9 (information dependency, coordination, exclusive source)

---

## Updated Entity: Jacqueline Faucitt (Jax)

### Previous Profile
- **Role**: CEO of RegimA Skin Treatments, Dan's partner
- **Vulnerability**: High vulnerability to pressure from Pete
- **Ethical Compliance**: High (maintains ethical standards)

### New Evidence (August 2025)
- Co-signs trustee appointment (August 11, 2025)
- Forwards trustee email to Dan with "Phishing" label (August 12, 2025)
- Uses personal email (jfaucitt@proton.me) for sensitive communications
- Receives Bantjies' August 27 email (forwarded by Dan to personal email)



### Updated Agent Properties
```json
{
  "legal_aggression": 0.2
