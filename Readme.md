# Role-Based Checklist Management System

## Overview

This module defines a role-based system for managing SOP-driven checklists. The system includes three primary roles:

* **Admin**
* **Staff**
* **Auditor**

Each role has specific responsibilities and permissions in the checklist lifecycle.

---

## Roles and Responsibilities

### 1. Admin

The Admin is responsible for configuring and managing the system.

#### Responsibilities:

* Create and manage SOPs
* Generate checklist templates from SOPs
* Manage users (assign roles: Admin, Auditor, Staff)
* Maintain checklist versions

#### Permissions:

* Create / Update / Delete checklist templates
* View all submissions
* Manage user roles

---

### 2. Staff

Staff are responsible for executing tasks and filling out checklists.

#### Responsibilities:

* View assigned checklist templates
* Fill checklist forms
* Provide answers (Yes/No, text, etc.)
* Upload attachments as proof
* Submit completed checklists

#### Permissions:

* Create checklist submissions
* Edit submissions (before submission)
* View their own submissions

---

### 3. Auditor

Auditors are responsible for verifying and approving submitted checklists.

#### Responsibilities:

* Review submitted checklists
* Validate answers and attachments
* Approve or reject submissions
* Provide review comments

#### Permissions:

* View all submitted checklists
* Approve or reject submissions
* Add audit comments

---

## Workflow

1. Admin creates SOP and generates checklist template
2. Staff fills out the checklist and submits it
3. Submission status is set to "Pending"
4. Auditor reviews the submission:

   * Approves → Status becomes "Approved"
   * Rejects → Status becomes "Rejected"
5. Audit details (approvedBy, approvalDate, comments) are recorded

---

## Data Fields

### Checklist Template

* templateId
* title
* version
* sections
* questions

---

### Checklist Submission

* submissionId
* templateId
* filledBy (Staff ID)
* status (Pending / Approved / Rejected)
* dateFilled
* approvedBy (Auditor ID)
* dateApproved
* overallComments

---

### Checklist Answers

* questionId
* answer (boolean/text)
* comment
* attachment (file URL)

---

## Rules and Constraints

* A user with role **Staff** cannot approve a checklist
* A user with role **Auditor** cannot fill a checklist
* The same user cannot be both **filledBy** and **approvedBy**
* A checklist must be submitted before it can be approved
* Attachments may be required for certain answers (optional rule)

---

## Status Flow

* Draft → (optional)
* Pending → (after submission)
* Approved → (after auditor approval)
* Rejected → (if auditor rejects)

---

## Tech Stack Assumptions

* Backend: Node.js (Express)
* Database: MySQL (Sequelize ORM)
* Frontend: React
* File Upload: Local / Cloud Storage

---

## Goal

To build a structured, auditable, and role-based checklist system that ensures:

* Accountability
* Compliance
* Traceability
* Scalability

---
