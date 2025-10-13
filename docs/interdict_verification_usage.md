# Interdict Verification System - Usage Guide (REVISED)

## Overview

The Interdict Verification System has been **upgraded** to detect not only fraudulent interdicts but also the **criminal abuse of legal processes**, including **malicious prosecution** and **witness intimidation**.

## NEW: Detecting Litigation Abuse

The system now identifies patterns of retaliatory litigation. The primary pattern detected in Case 2025-137857 is:

1.  **Crime Reported**: A party reports a serious crime (e.g., murder, fraud).
2.  **Retaliation 1 (Perjury)**: The suspect files a fraudulent interdict based on perjury to gain control and silence the reporter.
3.  **Exposure**: The initial fraud is exposed (e.g., by legal counsel withdrawing).
4.  **Retaliation 2 (Intimidation)**: The suspect files a **second, malicious interdict** with fabricated claims to harass, discredit, and intimidate the witness.

This pattern transforms the case from a civil dispute into a **continuing criminal enterprise** to obstruct justice.

## System Components (REVISED)

### 1. Core Verification Engine (`interdict_verification_system.py`)
-   **New Feature**: Now includes `assess_for_malicious_prosecution()` to flag claims that are contradicted by high-reliability evidence.
-   **New Feature**: `identify_abuse_pattern()` method to detect the retaliatory litigation pattern described above.

### 2. Litigation Abuse Tracker (`verification_tracker.py`)
-   **New Feature**: Tracks a sequence of legal filings to identify retaliatory patterns.
-   **New Output**: Generates a `LITIGATION_ABUSE_SUMMARY.md` for prosecutors.

### 3. Prosecution Memos
-   The system now automatically generates prosecution memos (`PROSECUTION_MEMO.md` and `LITIGATION_ABUSE_SUMMARY.md`) when it detects these criminal patterns.

## Usage Instructions (REVISED)

### Running the Analysis

1.  **Update the `verification_tracker.py` script** with the sequence of events (crime report, first interdict, second interdict).
2.  **Run the script**:
    ```bash
    python3 tools/verification_tracker.py
    ```
3.  **Review the output**: Check the generated `LITIGATION_ABUSE_SUMMARY.md` file.

## Interpreting Results (REVISED)

### New Verification Level: 🚨 MALICIOUS
-   This status is assigned to a legal claim that is not only false but is being pursued with the clear intent to harass, defraud, or intimidate.
-   **Indicator**: The claim is directly contradicted by high-reliability evidence (e.g., bank statements disproving financial allegations).

## Case 2025-137857 Findings (UPDATED)

### Current Status: ACTIVE WITNESS INTIMIDATION

The system has detected a clear pattern of malicious prosecution. The second interdict is not a legitimate legal action; it is an act of witness intimidation designed to interfere with a murder investigation.

### Critical Action Required

-   **Immediate Prosecution**: The generated prosecution memos should be submitted to the Hawks immediately.
-   **Emergency Court Action**: An emergency application must be filed to dismiss the second interdict as an abuse of process.

---

**Document Control**
- **Updated**: 2025-10-06
- **System Version**: 2.0
- **Focus**: Malicious Prosecution and Witness Intimidation

