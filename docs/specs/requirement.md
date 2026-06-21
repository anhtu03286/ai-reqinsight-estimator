DETAILED SPECIFICATION AND SYSTEM REQUIREMENTS DOCUMENT (SRS)
PROJECT: AI-POWERED SOFTWARE REQUIREMENTS ANALYSIS & AUTOMATED PROJECT QUOTATION SYSTEM
System Name (Working Title): AI ReqInsight & Estimator

Version: v1.1.0 (Enhanced Update)

Target Audience: Business Analyst (BA), Project Manager (PM), Presales, Tech Lead, QA/QC

1. PROJECT OVERVIEW
1.1. Background & Business Problem
In the bidding and software project initiation process, the phases of Requirement Analysis and Cost & Effort Estimation typically consume a significant amount of time and are prone to errors. Clients often provide input documents in a variety of formats (.pdf, .docx, .md, .txt, .xlsx), with content that is sometimes ambiguous, lacking logical consistency, or containing numerous system gaps. Manual extraction easily leads to missed scope (Scope Creep), creating risk of financial losses during actual implementation.

1.2. Solution Objectives
Build an intelligent platform powered by an AI Engine capable of reading and understanding multi-format documents, automatically extracting and performing in-depth analysis of requirements structure. The system is tasked with identifying ambiguous points requiring validation, warning of technical/operational risks, suggesting resolution approaches, automatically generating draft test scenarios, and exporting a professional commercial quotation file (Scope, Effort, Cost) based on the company's historical data and an automatic risk-factor multiplier mechanism.

2. END-TO-END WORKFLOW
The system operates in a linear and closed-loop manner through the following core steps:

Step 1 - Document Ingestion & Parsing: The user uploads a set of requirements documents. The system extracts text, tables, and diagrams using dedicated pipelines (including OCR).

Step 2 - Contextualization & Delta Analysis: AI extracts the document content by functional module. If the document is an update (v2, v3), the system performs a scope change comparison (Delta Analysis) against the previous version.

Step 3 - Validation & Assessment: AI cross-references a logic matrix to detect ambiguous points, feature gaps (Gaps), and scores risks (Risks).

Step 4 - Suggestions & Collaboration: AI proposes remediation solutions. The project team (BA/PM/Tech Lead) collaboratively interacts, edits, and approves AI findings on the Dashboard screen.

Step 5 - Generation & Integration: The system automatically compiles the data into a professional Excel quotation file with dynamic formulas, and is ready to synchronize the work breakdown structure to project management tools (Jira, Linear).

3. DETAILED INPUT / OUTPUT REQUIREMENTS (INPUT / OUTPUT REQUIREMENTS)
3.1. Input Specification
Multi-format support: Unstructured or semi-structured text including PDF (Scan & Text-searchable), Microsoft Word (.docx, .doc), Markdown (.md), Plain Text (.txt). Structured tabular data including Microsoft Excel (.xlsx, .xls) and CSV (.csv).

Upload mechanism: Supports simultaneous multi-file upload (Multi-file Upload) for the same project and asynchronous processing (Asynchronous Processing).

System limits: Maximum file size per upload is 50MB.

Language detection: Automatically detects and applies the appropriate natural language processing model (prioritizing optimization for English and Vietnamese).

3.2. Output Specification
The system must export and visually display the following 5 groups of in-depth analysis content:

Output Component	Detailed Description of AI Analysis Content	Display / Export Format
1. Clarification Items	Specifically lists qualitative phrases (e.g., "runs fast", "beautiful interface", "absolute security") that lack measurable KPI metrics. Identifies broken business flows that do not complete end-to-end processes.	Displayed as a Table on the Web, tagged with module codes. Allows export to a Word file of survey questions for use with the client.
2. Risks & Gaps Analysis	
• Gaps: Identifies screens/features that are mandatory but not mentioned in the document (e.g., an Order feature exists but there is no Cancel Order or Refund management).


• Risks: Warns of technology risks (legacy API integration), schedule risks, security risks (missing sensitive data encryption mechanism).

Categorized by severity level (High, Medium, Low) with visual color coding (Red, Yellow, Green).
3. Suggestions & Exclusions	Proposes technical solutions, appropriate Tech Stack selections, and standard business processes (Best Practices). Notably: Automatically generates an "Out of Scope" list to protect the company during bidding.	Displayed in parallel (Mapping) directly alongside each corresponding Risk/Gap item for easy cross-referencing.
4. Draft Test Cases	Automatically generates basic test scenarios (Happy Path) and risky edge cases (Edge Cases) from analyzed feature flows to help the QC team estimate testing effort.	Displayed as a separate tab on the report screen, allowing export in CSV/Excel format.
5. AI-Driven Quotation	Automatically decomposes the work breakdown structure WBS (Epics -> User Stories/Tasks). Projects Effort (Man-Day) by complexity and automatically applies a risk contingency buffer (Risk Buffer) corresponding to the ambiguity level of each feature.	Professional Excel (.xlsx) file containing automatic calculation formulas, a cost summary dashboard (Summary Dashboard), and a preliminary schedule breakdown.
4. SYSTEM FUNCTIONAL REQUIREMENTS (FUNCTIONAL REQUIREMENTS)
4.1. Ingestion & Parsing Module
FR-01 (Drag-and-Drop): The system provides an intuitive drag-and-drop interface for uploading project document sets.

FR-02 (OCR Engine): Integrates an optical character recognition tool to process scanned PDF documents or flow diagram images embedded in documents.

FR-03 (Semantic Chunking): Performs intelligent text segmentation by contextual segments, preserving hierarchical structure and table integrity.

4.2. AI Core & Delta Analysis Module
FR-04 (Cross-document Contradiction): AI automatically analyzes cross-document information contradictions when the user uploads multiple documents simultaneously (e.g., the main document specifies one requirement while an appendix specifies another).

FR-05 (Persona-based Analysis): Allows users to configure an "Analysis Perspective" (e.g., Act as Tech Lead to find architectural risks; Act as BA to find business gaps; Act as QA to find testing risks).

FR-06 (Delta Analysis): Supports version comparison of requirements (v1, v2). AI must automatically extract which text segments are newly added, deleted, or have changed scope, and then issue warnings about the impact on the current quotation.

4.3. Collaboration & Review Module
FR-07 (Contextual AI Chatbot): Provides an interactive chat panel directly alongside the document. Users can ask AI questions directly about the document content (e.g., "How does the security mechanism of this project work?").

FR-08 (Interactive Editing): Users have the right to edit, add, and delete analysis results (Gaps, Risks, Clarifications) generated by AI before publishing.

FR-09 (Review & Approval Workflow): Allows different roles (BA, Tech Lead, PM) to approve or reject each AI finding using a state transition mechanism (Pending, Approved, Rejected).

FR-10 (Deep-link Citation): When a user clicks on an item detected by AI, the system must automatically navigate and highlight directly to the specific segment/line of the original document for evidence cross-referencing.

4.4. Estimation & Integration Module
FR-11 (Rate Card Configuration): Allows the administration department to configure and store a personnel rate card by seniority level (Junior, Senior, Lead) and role (Dev, Tester, BA, PM) as the basis for cost calculation.

FR-12 (Historical Learning): AI performs a semantic matching algorithm (Semantic Matching) against the company's database of past completed projects to produce the most realistic effort estimate (Man-Day).

FR-13 (Dynamic Formula Generation): The exported Excel quotation file must contain dynamic mathematical formulas (SUM, PRODUCT...) linked between Tabs; hard-coded numeric values are not permitted.

FR-14 (PM Tools Integration): Provides a one-click synchronization feature (One-click Sync) to convert the approved WBS structure and Task list from the system to Jira, Linear, or ClickUp via API.

5. NON-FUNCTIONAL REQUIREMENTS (NON-FUNCTIONAL REQUIREMENTS)
5.1. Performance
NFR-01 (Response Time): The time for preliminary analysis and delivery of a report for a document set under 50 pages must not exceed 2 minutes.

NFR-02 (Concurrent Processing): The system supports a minimum of 50 simultaneous document processing sessions by users at the same time without degrading the AI Engine's performance.

5.2. Security & Privacy
NFR-03 (Data Encryption): All uploaded requirements documents and quotation information must be encrypted to the AES-256 standard at rest (Data-at-rest) and SSL/TLS 1.3 in transit (Data-in-transit).

NFR-04 (AI Security - Data Isolation): Ensures absolute data isolation between corporate accounts. Client document and quotation data must not be used as training data for public language models. Use of a Private LLM or Enterprise API packages with a privacy security commitment is mandatory.

NFR-05 (Access Control): Applies a Role-Based Access Control (RBAC) model, ensuring personnel can only view projects assigned to them.

5.3. Usability & Scalability
NFR-06 (Pluggable Model Architecture): The system architecture must be designed as a Microservices architecture with an Abstraction API layer for the AI Model. The system must be able to easily replace or swap out large language model versions (e.g., smoothly switching between GPT, Claude, Gemini) without affecting the application's business logic.

NFR-07 (UI Compatibility): The Web Dashboard interface must support smart filtering (Filter), advanced keyword search, clear module grouping, and be user-friendly for non-technical users.

6. APPENDIX: MULTI-LAYER STRUCTURE OF THE EXPORTED QUOTATION FILE (.XLSX)
The Excel quotation file automatically generated by the system must comply with the following 4-tab standard structure:

Tab 1 - Cover & Dashboard: Contains overall project information, total cost, total timeline (expected Timeline), and charts breaking down the cost and effort (Effort) proportion by major module.

Tab 2 - Estimation Sheet (WBS): Detailed work breakdown table. Includes the following columns: Feature Code, Major Module Name, Detailed Feature Name, Scope Description, Complexity Level, Expected Effort (Man-day) broken down by Dev/Tester/BA, Risk Buffer Coefficient, and Estimation Rationale Notes.

Tab 3 - Rate Card & Cost Calculation: Table containing actual configured personnel rates. Uses dynamic formula links to Tab 2 to automatically calculate total personnel costs, management fees, VAT, and total contract value.

Tab 4 - Assumptions & Exclusions: Lists technical assumptions and items outside the implementation scope (Out of Scope) automatically extracted from the risk analysis process to protect the company from disputes with clients.
