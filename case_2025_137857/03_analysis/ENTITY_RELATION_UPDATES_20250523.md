# Entity Relation Updates - Evidence Package 2025-05-23

## Document Purpose
This document captures new entity relationships, behavioral patterns, and agent model updates identified from the 2025-05-23 evidence package documenting audit trail disappearance and revenue diversion.

## New Entities Identified

### Infrastructure Entities

#### Shopify International Limited
- **Entity Type**: Service Provider / Cloud Platform
- **Entity ID**: `service_shopify_international`
- **Registration**: VAT Number 4820289033
- **Address**: 2nd Floor, 1-2 Victoria Buildings, Haddington Road, Dublin 4, D04 XN32, Ireland
- **Role**: Legitimate cloud-based e-commerce platform provider
- **Relationship to Case**: Platform from which audit trails were diverted
- **Agent Properties**:
  - **legal_aggression**: 0.2 (service provider, not involved in dispute)
  - **control_seeking**: 0.1 (provides platform, doesn't seek control)
  - **evidence_dismissal**: 0.0 (maintains audit trails professionally)
  - **vulnerability_to_pressure**: 0.3 (subject to legal subpoenas)
  - **ethical_compliance**: 0.9 (international service provider with compliance standards)
- **Strategic Goals**:
  - Provide reliable e-commerce platform services
  - Maintain transaction audit trails
  - Comply with legal requests for records
- **Behavioral Rules**:
  - IF subpoenaed THEN provide complete transaction records
  - IF account control disputed THEN require proper authorization
  - IF data breach suspected THEN investigate and report

#### Pastel Accounting System
- **Entity Type**: Software System / Local Infrastructure
- **Entity ID**: `system_pastel_local`
- **Description**: Local accounting system instance on reportedly stolen server
- **Access Control**: Exclusive Rynette access
- **Role**: Repository for diverted audit trails post-May 22, 2025
- **Relationship to Case**: Criminal infrastructure for evidence concealment
- **Agent Properties**:
  - **legal_aggression**: N/A (system, not autonomous)
  - **control_seeking**: N/A (controlled by Rynette)
  - **evidence_dismissal**: N/A (passive repository)
  - **vulnerability_to_pressure**: 1.0 (physical server can be seized)
  - **ethical_compliance**: 0.0 (used for criminal purposes)
- **Strategic Goals**: N/A (passive system)
- **Behavioral Rules**: N/A (controlled by Rynette)
- **State**: Contains diverted audit trails from May 22, 2025 onward

### Payment Card Entities

#### Visa Card ending in 5225
- **Entity Type**: Financial Instrument
- **Entity ID**: `payment_card_5225`
- **Owner**: RegimA Zone (Pty) Ltd / Business entity
- **Status**: Cancelled June 7, 2025
- **Role**: Primary business payment card, systematically cancelled
- **Relationship to Case**: Victim of financial sabotage
- **Impact**: 24 payment failures over 78 days for single Shopify bill

#### Visa Card ending in 3212
- **Entity Type**: Financial Instrument
- **Entity ID**: `payment_card_3212`
- **Owner**: Dan/Jax (personal card)
- **Status**: Active, used for emergency business payments
- **Role**: Backup payment method after business cards cancelled
- **Relationship to Case**: Evidence of forced personal liability for business expenses
- **Impact**: Used to resolve 78-day payment crisis on September 29, 2025

### Shopify Store Entities (RegimA Zone Network)

#### RegimA DST
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_dst`
- **Parent**: RegimA Zone W organization
- **Status**: Audit trail ceased May 22, 2025
- **Revenue Contribution**: Part of R26.4M annual network

#### RegimA Zone SA
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_zone_sa`
- **Parent**: RegimA Zone W organization
- **Status**: Audit trail ceased May 22, 2025
- **Revenue Contribution**: Part of R26.4M annual network

#### RegimA Zone
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_zone`
- **Parent**: RegimA Zone W organization
- **Status**: Audit trail ceased May 22, 2025
- **Revenue Contribution**: Part of R26.4M annual network

#### RegimA ZA-GP-NE
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_gp_ne`
- **Parent**: RegimA Zone W organization
- **Status**: Audit trail ceased May 22, 2025
- **Revenue Contribution**: Part of R26.4M annual network

#### RegimA ZA-NE
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_ne`
- **Parent**: RegimA Zone W organization
- **Status**: Audit trail ceased May 22, 2025
- **Revenue Contribution**: Part of R26.4M annual network

#### RegimA Europe
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_europe`
- **Parent**: RegimA Zone W organization
- **Status**: Audit trail ceased May 22, 2025
- **Revenue Contribution**: Part of R26.4M annual network

#### RegimA WWD
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_wwd`
- **Parent**: RegimA Zone W organization
- **Status**: Audit trail ceased May 22, 2025
- **Revenue Contribution**: Part of R26.4M annual network

### Shopify Store Entities (RegimA SA Network)

#### RegimA ZA-CPT
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_cpt`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

#### RegimA ZA (Alma)
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_alma`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

#### RegimA ZA-WC
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_wc`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

#### RegimA ZA-DBN
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_dbn`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

#### RegimA ZA-EC
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_ec`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

#### RegimA ZA-NL
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_nl`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

#### RegimA ZA (Romy)
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_romy`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

#### RegimA ZA (Debbie)
- **Entity Type**: E-commerce Store
- **Entity ID**: `store_regima_za_debbie`
- **Parent**: RegimA SA organization
- **Status**: Sales ceased June 2025 (R0.00 Jun-Aug)
- **Revenue Contribution**: Part of R8.5M annual network

## Updated Entity Relationships

### Rynette (Bookkeeper) - Enhanced Profile

**Updated Agent Properties**:
- **legal_aggression**: 0.7 → 0.8 (escalated through exclusive system access)
- **control_seeking**: 0.8 → 0.9 (exclusive Pastel access, payment card control)
- **evidence_dismissal**: 0.7 (maintains pattern)
- **vulnerability_to_pressure**: 0.4 (maintains pattern)
- **ethical_compliance**: 0.1 → 0.05 (further evidence of criminal conduct)

**New Strategic Goals**:
- Maintain exclusive access to Pastel instance
- Control all payment card authorizations
- Divert audit trails from cloud to local systems
- Execute systematic service cancellations

**New Behavioral Rules**:
- IF audit trail exists in cloud THEN divert to local Pastel instance
- IF business payment cards active THEN cancel systematically
- IF services accumulate THEN cancel without authorization
- IF questioned about access THEN claim exclusive authority

**New Relationships**:
- **Shopify International**: -0.9 (adversarial - diverted their audit trails)
- **Pastel System**: 1.0 (exclusive control)
- **Payment Card 5225**: 1.0 (cancelled without authorization)
- **All Shopify Stores**: -0.9 (sabotaged operations)

**State Updates**:
- **May 22, 2025**: Diverted Shopify audit trails to local Pastel
- **June 7, 2025**: Cancelled 15 business payment cards
- **June-September 2025**: Maintained exclusive Pastel access
- **Ongoing**: Controls all diverted revenue records

### Peter Andrew Faucitt (Pete) - Enhanced Profile

**Updated Agent Properties**:
- **legal_aggression**: 0.9 (maintains pattern)
- **control_seeking**: 0.9 (maintains pattern)
- **evidence_dismissal**: 0.95 (maintains pattern)
- **vulnerability_to_pressure**: 0.2 (maintains pattern)
- **ethical_compliance**: 0.05 (maintains pattern)

**Updated Strategic Goals**:
- Control all revenue streams (R34.9M+ at risk)
- Eliminate Dan's access to business systems
- Maintain information dependency on Rynette
- Conceal revenue diversion through local Pastel

**Updated Behavioral Rules**:
- IF revenue streams exist in cloud THEN order diversion to local systems (via intermediaries)
- IF Dan has payment access THEN cancel all business cards (via Rynette)
- IF services support Dan's operations THEN cancel systematically (via Rynette)
- IF audit trails exist independently THEN eliminate cloud access (via Rynette)

**New Relationships**:
- **Shopify International**: -0.8 (indirect - ordered diversion via Rynette)
- **Pastel System**: 0.9 (benefits from Rynette's exclusive access)
- **Payment Card 5225**: -0.9 (ordered cancellation via intermediaries)
- **All Shopify Stores**: -0.9 (ordered operations cessation)

**Information Dependency Updates**:
- **Rynette**: 1.0 (complete dependency for financial information)
- **Technical Intermediaries**: 0.8 (dependency for system changes)
- **Banking Intermediaries**: 0.7 (dependency for payment card actions)

**State Updates**:
- **April 22, 2025**: Ordered cloud IT systems removal (via intermediaries)
- **May 22, 2025**: Benefited from audit trail diversion (via Rynette)
- **June 7, 2025**: Ordered payment card cancellations (via Rynette)
- **June-September 2025**: Received filtered information from Rynette

### RegimA Zone (Pty) Ltd - Enhanced Profile

**Updated Agent Properties**:
- **legal_aggression**: 0.1 (victim entity, not aggressive)
- **control_seeking**: 0.0 (under external control)
- **evidence_dismissal**: 0.0 (maintains records)
- **vulnerability_to_pressure**: 1.0 (completely vulnerable to sabotage)
- **ethical_compliance**: 0.9 (legitimate business operations)

**Updated Strategic Goals**:
- ~~Maintain viable e-commerce operations~~ (FAILED - sabotaged)
- ~~Process customer orders through Shopify~~ (FAILED - diverted)
- ~~Maintain payment card access for services~~ (FAILED - cancelled)
- Survive systematic sabotage (ONGOING)

**State Updates**:
- **Pre-May 22, 2025**: Viable business with R26.4M annual revenue
- **May 22, 2025**: Shopify audit trail ceased, operations compromised
- **June 7, 2025**: Payment cards cancelled, 300+ defaulting bills
- **July 10, 2025**: Shopify bill created, 78-day payment failure cascade
- **September 29, 2025**: Forced to use Dan/Jax personal cards for business expenses
- **Current**: Operations severely compromised, revenue diverted

**New Relationships**:
- **Shopify International**: 0.8 (legitimate service relationship, now compromised)
- **Pastel System**: -0.9 (adversarial - holds diverted audit trails)
- **Rynette**: -1.0 (adversarial - executed sabotage)
- **Pete**: -1.0 (adversarial - ordered sabotage)
- **Dan**: 1.0 (owner attempting to maintain operations)

### RegimA SA - Enhanced Profile

**Updated Agent Properties**:
- **legal_aggression**: 0.1 (victim entity, not aggressive)
- **control_seeking**: 0.0 (under external control)
- **evidence_dismissal**: 0.0 (maintains records)
- **vulnerability_to_pressure**: 1.0 (completely vulnerable to sabotage)
- **ethical_compliance**: 0.9 (legitimate business operations)

**Updated Strategic Goals**:
- ~~Maintain viable e-commerce operations~~ (FAILED - completely ceased)
- ~~Process customer orders through Shopify~~ (FAILED - diverted)
- ~~Generate R8.5M annual revenue~~ (FAILED - R0.00 Jun-Aug 2025)
- Survive systematic sabotage (FAILING)

**State Updates**:
- **Pre-May 22, 2025**: Viable business with R8.5M annual revenue
- **May 22, 2025**: Shopify audit trail ceased
- **June 2025**: Sales completely ceased (R0.00)
- **July 2025**: No sales recorded (R0.00)
- **August 2025**: No sales recorded (R0.00)
- **Current**: Business operations completely shut down

**New Relationships**:
- **Shopify International**: 0.8 (legitimate service relationship, now severed)
- **Pastel System**: -0.9 (adversarial - holds diverted audit trails)
- **Rynette**: -1.0 (adversarial - executed sabotage)
- **Pete**: -0.5 (co-owner, but enabled sabotage)
- **Dan**: 0.5 (co-owner attempting to maintain operations)

### Dan (Daniel) - Enhanced Profile

**Updated Agent Properties**:
- **legal_aggression**: 0.2 (maintains defensive posture)
- **control_seeking**: 0.3 (seeking to restore legitimate control)
- **evidence_dismissal**: 0.0 (maintains all evidence)
- **vulnerability_to_pressure**: 0.7 → 0.8 (increased financial pressure from sabotage)
- **ethical_compliance**: 0.95 (maintains pattern)

**Updated Strategic Goals**:
- ~~Maintain business operations~~ (SEVERELY COMPROMISED)
- Document systematic sabotage (SUCCESSFUL - this evidence)
- ~~Preserve audit trails~~ (PARTIALLY FAILED - diverted to Pastel)
- Expose revenue diversion scheme (ONGOING)
- Recover diverted revenue records (PENDING)

**New Behavioral Rules**:
- IF business cards cancelled THEN use personal cards to maintain operations
- IF audit trails diverted THEN document cessation dates and patterns
- IF services cancelled THEN document scale and impact
- IF revenue diverted THEN quantify and preserve evidence

**State Updates**:
- **May 22, 2025**: Discovered Shopify audit trail cessation
- **June 7, 2025**: Experienced 15 payment card cancellations
- **June 8, 2025**: Discovered complete order stoppage
- **July 10-September 29, 2025**: Managed 78-day payment crisis for single bill
- **Ongoing**: Using personal funds for business expenses, documenting sabotage

**New Relationships**:
- **Shopify International**: 0.7 (legitimate service relationship, seeking records)
- **Pastel System**: -0.9 (adversarial - contains diverted records)
- **Payment Card 5225**: 0.8 (victim of cancellation)
- **Payment Card 3212**: 1.0 (personal card used for business rescue)
- **All Shopify Stores**: 1.0 (owner/operator, attempting to restore)

## New Hypergraph Relationships

### Revenue Diversion Network
```
[Rynette] --controls--> [Pastel System]
[Pastel System] --contains--> [Diverted Audit Trails]
[Diverted Audit Trails] --stolen_from--> [Shopify International]
[Shopify International] --legitimate_platform_for--> [All Shopify Stores]
[All Shopify Stores] --owned_by--> [RegimA Zone] OR [RegimA SA]
[RegimA Zone] --owned_by--> [Dan]
[RegimA SA] --co_owned_by--> [Dan, Pete]
[Pete] --instructs--> [Rynette]
[Rynette] --executes--> [Audit Trail Diversion]
```

### Payment Sabotage Network
```
[Pete] --orders--> [Payment Card Cancellation]
[Rynette] --executes--> [Payment Card Cancellation]
[Payment Card Cancellation] --affects--> [15 Business Cards]
[15 Business Cards] --includes--> [Payment Card 5225]
[Payment Card 5225] --used_by--> [RegimA Zone]
[Payment Card Cancellation] --causes--> [300+ Defaulting Bills]
[300+ Defaulting Bills] --includes--> [Shopify Bill #388990813]
[Shopify Bill #388990813] --fails_24_times--> [78 Days]
[78 Days] --resolved_by--> [Payment Card 3212]
[Payment Card 3212] --owned_by--> [Dan/Jax Personal]
[Dan/Jax Personal] --forced_to_cover--> [Business Expenses]
```

### Service Destruction Network
```
[Payment Card Cancellation] --triggers--> [Service Cancellations]
[Service Cancellations] --affects--> [30 Years of Services]
[30 Years of Services] --includes--> [Software Tools]
[Service Cancellations] --causes--> [IP File Destruction]
[IP File Destruction] --destroys--> [100M+ Files]
[100M+ Files] --includes--> [Artwork, Documents, Code]
[IP File Destruction] --duration--> [1-2 Months]
[IP File Destruction] --survivors--> [Dan/Jax Personal Backups]
```

### Business Viability Evidence Network
```
[RegimA Zone] --operates--> [7 Shopify Stores]
[7 Shopify Stores] --generates--> [R26.4M Annual Revenue]
[RegimA SA] --operates--> [8 Shopify Stores]
[8 Shopify Stores] --generates--> [R8.5M Annual Revenue]
[Total Revenue] --equals--> [R34.9M Annually]
[May 22, 2025] --marks--> [Audit Trail Cessation]
[Audit Trail Cessation] --causes--> [Revenue Decline/Cessation]
[Revenue Decline/Cessation] --proves--> [Systematic Sabotage]
```

## Quantified Impact Analysis

### Revenue Impact
- **Total Annual Revenue at Risk**: R34,951,765.30
  - RegimA Zone: R26,447,551.48
  - RegimA SA: R8,504,213.82
- **Post-Sabotage Loss** (3 months, Jun-Aug 2025): ~R8.7M
  - RegimA SA: Complete cessation (R0.00)
  - RegimA Zone: Dramatic decline
- **Annualized Loss Projection**: R34.9M+ if sabotage continues

### Service Disruption Impact
- **Payment Cards Cancelled**: 15 business cards
- **Defaulting Bills**: 300+ across all companies
- **Example Bill Duration**: 78 days (July 10 - September 29, 2025)
- **Payment Failures**: 24 attempts for single bill
- **Services Lost**: 30 years of accumulated software/services
- **Forced Personal Liability**: Dan/Jax personal cards used for business expenses

### IP Destruction Impact
- **Files Destroyed**: 100,000,000+ files
- **Content Types**: Artwork, documents, code
- **Destruction Duration**: 1-2 months
- **Survivors**: Only Dan/Jax personal computer backups
- **Value**: Potentially hundreds of millions in IP assets

### Operational Impact
- **Stores Affected**: 15 Shopify stores
- **POPIA Compliance**: B2B Self-Service Customer Portals compromised
- **Audit Trail Status**: Diverted from cloud to uncontrolled local system
- **Business Continuity**: Severely compromised to completely ceased

## Database Schema Updates Required

### New Tables

#### shopify_stores
```sql
CREATE TABLE shopify_stores (
  store_id VARCHAR PRIMARY KEY,
  store_name VARCHAR NOT NULL,
  parent_organization VARCHAR NOT NULL,
  annual_revenue DECIMAL(15,2),
  audit_trail_status VARCHAR,
  last_audit_entry_date DATE,
  status VARCHAR,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### payment_cards
```sql
CREATE TABLE payment_cards (
  card_id VARCHAR PRIMARY KEY,
  card_last_four VARCHAR(4) NOT NULL,
  card_type VARCHAR,
  owner_entity VARCHAR NOT NULL,
  cancellation_date DATE,
  cancellation_authorized_by VARCHAR,
  status VARCHAR,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### payment_failures
```sql
CREATE TABLE payment_failures (
  failure_id VARCHAR PRIMARY KEY,
  bill_id VARCHAR NOT NULL,
  card_id VARCHAR NOT NULL,
  failure_date DATE NOT NULL,
  amount_usd DECIMAL(10,2),
  amount_zar DECIMAL(10,2),
  resolution_date DATE,
  resolution_card_id VARCHAR,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### audit_trail_diversions
```sql
CREATE TABLE audit_trail_diversions (
  diversion_id VARCHAR PRIMARY KEY,
  source_system VARCHAR NOT NULL,
  destination_system VARCHAR NOT NULL,
  diversion_date DATE NOT NULL,
  stores_affected TEXT[],
  revenue_at_risk DECIMAL(15,2),
  access_controller VARCHAR,
  status VARCHAR,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Updated Tables

#### case_entities
```sql
ALTER TABLE case_entities ADD COLUMN IF NOT EXISTS revenue_annual DECIMAL(15,2);
ALTER TABLE case_entities ADD COLUMN IF NOT EXISTS stores_operated INTEGER;
ALTER TABLE case_entities ADD COLUMN IF NOT EXISTS sabotage_impact_level VARCHAR;
```

#### case_events
```sql
ALTER TABLE case_events ADD COLUMN IF NOT EXISTS revenue_impact DECIMAL(15,2);
ALTER TABLE case_events ADD COLUMN IF NOT EXISTS stores_affected INTEGER;
ALTER TABLE case_events ADD COLUMN IF NOT EXISTS payment_failures_count INTEGER;
```

## Next Actions

1. **Update Entity Database**: Insert new entities (Shopify stores, payment cards, systems)
2. **Update Relationship Database**: Insert new relationships and update existing ones
3. **Update Timeline Database**: Insert May 22, July 10, September 29 events with full details
4. **Update Hypergraph Database**: Insert new network relationships
5. **Synchronize Supabase**: Push all updates to Supabase project
6. **Synchronize Neon**: Push all updates to Neon project
7. **Generate Visualizations**: Create network diagrams showing revenue diversion and payment sabotage
8. **Update Analysis Reports**: Incorporate R34.9M revenue quantification into fraud analysis

---

**Document Created**: 2025-10-11
**Evidence Source**: `evidence_package_20250523`
**Analysis Confidence**: HIGH (primary source documents, specific dates, quantified impacts)
**Database Sync Status**: PENDING

