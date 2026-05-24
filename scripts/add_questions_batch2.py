#!/usr/bin/env python3
"""Batch 2: 20 MATCH/MAMCQ questions for SAA-C03."""
import json, hashlib, os

EXAM = "AWS Certified Solutions Architect - Associate (SAA-C03)"

def qid(stem):
    return hashlib.sha256((EXAM + stem).encode()).hexdigest()

new_questions = [
    # ── Q1: MATCH – ML Text/Vision Services ─────────────────────────────────
    {
        "id": qid("Rekognition Transcribe Textract Comprehend Translate ML services match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A solutions architect is selecting AWS AI/ML services for five separate application "
            "requirements. Match each requirement to the MOST appropriate AWS managed AI service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Rekognition",
            "B": "Amazon Transcribe",
            "C": "Amazon Textract",
            "D": "Amazon Comprehend",
            "E": "Amazon Translate",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A compliance system analyzes millions of customer feedback emails to "
                    "automatically detect sentiment (positive/negative/mixed), extract named "
                    "entities (person, organization, date), identify dominant language, and flag "
                    "any personally identifiable information (PII)."
                ),
                "correct": "D",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A call center platform converts recorded customer service calls to "
                    "searchable text transcripts with speaker diarization (who spoke when) "
                    "and a custom vocabulary for industry-specific terminology."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A content moderation system processes images uploaded by users of a "
                    "social platform, detecting unsafe content, recognizing celebrity faces, "
                    "and identifying objects and scenes — returning confidence scores for each."
                ),
                "correct": "A",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A finance team automates accounts payable by extracting structured data "
                    "(vendor name, invoice number, line items, totals) from scanned PDF invoices "
                    "without pre-defining templates or training a custom model."
                ),
                "correct": "C",
            },
            {
                "id": "sq5",
                "prompt": (
                    "A global e-commerce platform automatically converts English product "
                    "descriptions into 50 other languages in real time when a new listing is "
                    "created, using neural machine translation."
                ),
                "correct": "E",
            },
        ],
        "explanation": (
            "Comprehend is AWS's NLP service for text analysis: sentiment, entity extraction, "
            "key phrases, language detection, and PII redaction. Transcribe converts audio to "
            "text (ASR) with speaker diarization, custom vocabularies, and custom language models. "
            "Rekognition analyzes images and videos for faces, objects, scenes, text, and moderation "
            "labels. Textract extracts structured data (key-value pairs, tables, form fields) from "
            "documents and PDFs without requiring template definitions. Translate provides neural "
            "machine translation supporting 75+ languages."
        ),
        "tags": [
            "Amazon Rekognition",
            "Amazon Transcribe",
            "Amazon Textract",
            "Amazon Comprehend",
            "Amazon Translate",
            "Amazon SageMaker AI",
        ],
    },

    # ── Q2: MAMCQ – Amazon Macie + AWS CloudHSM ───────────────────────────────
    {
        "id": qid("Macie S3 PII CloudHSM FIPS 140-2 Level 3 mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.3",
        "stem": (
            "A financial services company stores sensitive payment card data in Amazon S3. "
            "The security team has two requirements: (1) automatically discover and alert on any "
            "S3 bucket containing unprotected PII or financial data, and (2) encrypt data using "
            "cryptographic keys stored in FIPS 140-2 Level 3 validated hardware where AWS has "
            "NO access to the key material. Which TWO services satisfy these requirements? "
            "(Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Macie — uses ML to automatically discover, classify, and alert on sensitive data (PII, financial records, credentials) stored in S3 buckets",
            "B": "Amazon GuardDuty — detects threats such as unusual S3 API calls and data exfiltration patterns indicative of a breach in progress",
            "C": "AWS CloudHSM — provides single-tenant, FIPS 140-2 Level 3 validated hardware security modules where the customer manages all key material and AWS has zero access to the HSMs",
            "D": "AWS KMS with customer managed keys (CMKs) — encrypts data using FIPS 140-2 Level 2 validated HSMs managed by AWS, where the customer controls the key policy",
            "E": "AWS Secrets Manager — stores and rotates database credentials and API keys, with automatic integration for RDS and Redshift secrets",
        },
        "explanation": (
            "Amazon Macie is purpose-built for discovering and protecting sensitive data in S3: it "
            "uses ML to detect PII, financial data, and credentials, generates findings, and can "
            "alert via EventBridge or Security Hub — exactly what requirement 1 needs. AWS CloudHSM "
            "provides single-tenant, FIPS 140-2 Level 3 validated HSMs where the customer controls "
            "the HSM partition and AWS has no ability to extract key material — satisfying requirement 2. "
            "KMS CMKs use FIPS 140-2 Level 2 HSMs managed by AWS; while very secure, AWS technically "
            "manages the underlying hardware and the key material never leaves KMS-managed HSMs. "
            "GuardDuty detects active threats and anomalies but does not discover stored PII. "
            "Secrets Manager manages credentials, not arbitrary customer-controlled encryption keys."
        ),
        "tags": [
            "Amazon Macie",
            "AWS CloudHSM",
            "Implementing policies for data access, lifecycle, and protection",
            "Data access and governance",
        ],
    },

    # ── Q3: MATCH – Serverless Patterns ──────────────────────────────────────
    {
        "id": qid("Lambda Fargate AppSync SAR serverless patterns match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A solutions architect is selecting serverless AWS services for four different "
            "application patterns. Match each pattern to the MOST appropriate serverless service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Lambda",
            "B": "AWS Fargate",
            "C": "AWS AppSync",
            "D": "AWS Serverless Application Repository (SAR)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A team builds a reusable, pre-tested serverless data-ingestion pipeline "
                    "and wants to publish it so other AWS accounts in the organisation can "
                    "discover and deploy it in one click without writing CloudFormation."
                ),
                "correct": "D",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A mobile app needs real-time data synchronization via GraphQL subscriptions, "
                    "offline data support when the device has no connectivity, and automatic "
                    "conflict resolution — backed by DynamoDB."
                ),
                "correct": "C",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A batch image-processing job runs Docker containers requiring 30 GiB RAM "
                    "and 8 vCPUs per task, takes up to 4 hours to complete, and is triggered "
                    "from an SQS queue — with no EC2 instances to manage."
                ),
                "correct": "B",
            },
            {
                "id": "sq4",
                "prompt": (
                    "An S3 event triggers lightweight JSON transformation and routing logic "
                    "that runs for under 10 seconds and forwards the result to an SNS topic. "
                    "No persistent infrastructure should be provisioned."
                ),
                "correct": "A",
            },
        ],
        "explanation": (
            "SAR is a managed repository for sharing and deploying serverless applications — "
            "publishers upload SAM templates and code, and consumers deploy them with one click "
            "without touching CloudFormation directly. AppSync is a fully managed GraphQL service "
            "with built-in real-time WebSocket subscriptions, DynamoDB resolvers, and offline "
            "sync (via Amplify DataStore), making it ideal for mobile apps. Fargate runs "
            "containerised workloads without managing EC2 instances — it supports large memory "
            "(up to 120 GiB) and long-running tasks (hours) that exceed Lambda's constraints. "
            "Lambda is ideal for short-lived (max 15 minutes), event-driven functions triggered "
            "by S3, SNS, SQS, or API Gateway — with no infrastructure to provision or manage."
        ),
        "tags": [
            "Serverless technologies and patterns (for example, AWS Lambda, Fargate)",
            "AWS AppSync",
            "AWS Serverless Application Repository",
            "AWS Fargate",
            "AWS Lambda",
        ],
    },

    # ── Q4: MAMCQ – AWS Cost and Usage Report + Budgets ───────────────────────
    {
        "id": qid("Cost and Usage Report CUR Budgets Athena QuickSight FinOps mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "4.2",
        "stem": (
            "A FinOps team has two requirements: (1) build custom Amazon Athena queries and "
            "Amazon QuickSight dashboards against the most granular AWS billing data available "
            "(hourly, resource-level, with usage type and tags), and (2) automatically send "
            "an SNS alert when monthly spend for a specific AWS service exceeds a defined "
            "dollar threshold. Which TWO services should they configure? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Cost and Usage Report (CUR) delivered to an S3 bucket in Parquet format, enabling Athena queries with an AWS Glue crawler-generated table for granular resource-level cost analysis",
            "B": "AWS Cost Explorer with CSV export scheduled by a Lambda function, processed by Glue ETL, and loaded into Redshift for visualization",
            "C": "AWS Budgets configured with a Cost budget scoped to a specific AWS service, with an SNS alert action triggered when actual monthly spend exceeds the defined threshold",
            "D": "AWS Trusted Advisor to generate weekly cost-optimization recommendations and automatically email the savings summary to the billing team",
            "E": "Amazon CloudWatch Billing Alarm on the EstimatedCharges metric to notify via SNS when total estimated charges exceed the threshold",
        },
        "explanation": (
            "AWS Cost and Usage Report is the most comprehensive billing dataset AWS offers — it "
            "provides hourly, resource-level cost and usage data with all cost allocation tags, "
            "delivered to S3 in CSV or Parquet format. Pairing CUR with an Athena table (via a "
            "Glue crawler) and QuickSight is the standard AWS FinOps architecture for custom "
            "granular analysis. AWS Budgets supports service-scoped cost budgets with SNS "
            "alert actions — the most direct mechanism for service-specific spend thresholds. "
            "Cost Explorer provides pre-built 13-month visualizations and CSV exports but does "
            "not provide the hourly resource-level granularity needed for custom Athena queries. "
            "Trusted Advisor provides general cost optimization checks, not configurable dollar "
            "thresholds. CloudWatch Billing Alarms monitor estimated total charges and cannot "
            "be filtered to a specific service the way Budgets can."
        ),
        "tags": [
            "AWS Cost and Usage Report",
            "AWS Budgets",
            "AWS Cost Explorer",
            "Implementing visualization strategies",
        ],
    },

    # ── Q5: MATCH – AWS Security Services ─────────────────────────────────────
    {
        "id": qid("GuardDuty Detective Security Hub Inspector security services match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A solutions architect is assigning AWS security services to four operational "
            "scenarios. Match each scenario to the MOST appropriate security service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon GuardDuty",
            "B": "Amazon Detective",
            "C": "AWS Security Hub",
            "D": "Amazon Inspector",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A SOC team receives hundreds of daily findings from GuardDuty, Macie, "
                    "and Inspector across 40 accounts. They need a single aggregated dashboard "
                    "that normalizes all findings to the Amazon Security Finding Format (ASFF), "
                    "prioritizes them by severity, and maps them to compliance frameworks."
                ),
                "correct": "C",
            },
            {
                "id": "sq2",
                "prompt": (
                    "An analyst must investigate a GuardDuty finding about an EC2 instance "
                    "making outbound calls to a known command-and-control server. The analyst "
                    "needs a visual, graph-based timeline of all related API calls, VPC flow "
                    "records, and CloudTrail events over the past 90 days."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A security operations team needs continuous, automated detection of "
                    "anomalous behaviors across the AWS environment: unusual IAM role assumptions, "
                    "EC2 instances communicating with known malicious IPs, and S3 data "
                    "exfiltration patterns — without deploying any agents."
                ),
                "correct": "A",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A DevSecOps team requires continuous assessment of EC2 instances and "
                    "ECR container images for known CVEs (Common Vulnerabilities and Exposures) "
                    "with CVSS-scored findings that integrate into Security Hub for "
                    "centralised tracking."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "Security Hub is the centralised findings aggregation service: it collects findings "
            "from GuardDuty, Macie, Inspector, Firewall Manager, and partner tools; normalizes "
            "them to ASFF; scores them; and maps them to CIS, PCI DSS, and NIST frameworks. "
            "Amazon Detective is the post-incident investigation service: it uses ML and graph "
            "analysis to build interactive visualizations of API call sequences, network flows, "
            "and user sessions — enabling root-cause analysis of security incidents. GuardDuty "
            "is the always-on threat detection service: it analyzes CloudTrail, VPC Flow Logs, "
            "DNS logs, and Kubernetes audit logs for anomalous behavior and known malicious "
            "indicators without requiring agents. Inspector v2 is the vulnerability management "
            "service that continuously scans EC2 (via SSM agent) and ECR images for CVEs."
        ),
        "tags": [
            "Amazon Detective",
            "Amazon Macie",
            "Amazon Inspector",
            "AWS Firewall Manager",
            "Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways)",
        ],
    },

    # ── Q6: MAMCQ – Firewall Manager + WAF ───────────────────────────────────
    {
        "id": qid("Firewall Manager WAF org-wide ALB CloudFront auto-protection mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A company with 35 AWS accounts must enforce consistent AWS WAF web ACL rules "
            "across ALL public-facing Application Load Balancers and Amazon CloudFront "
            "distributions. New ALBs created in any member account must be automatically "
            "protected without requiring the individual account team to take any action. "
            "Which TWO services should the solutions architect configure? (Select TWO.)"
        ),
        "correct": ["A", "B"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS WAF — create web ACLs containing AWS Managed Rules groups (e.g., AWSManagedRulesCommonRuleSet, AWSManagedRulesSQLiRuleSet) that define the actual filtering rules",
            "B": "AWS Firewall Manager — create WAF security policies at the Organisation root that reference the WAF web ACLs and automatically deploy them to all existing and future ALBs and CloudFront distributions in member accounts",
            "C": "Amazon GuardDuty — enable S3 protection and CloudTrail monitoring to detect when an ALB without WAF is created and trigger a Lambda remediation",
            "D": "AWS Network Firewall — deploy a centralised firewall in a dedicated security VPC with Gateway Load Balancer to inspect all HTTP/HTTPS traffic before it reaches ALBs",
            "E": "AWS Config — create a custom rule that checks for ALBs without WAF associations and triggers an SNS notification to alert the account owner to manually attach the WAF",
        },
        "explanation": (
            "AWS WAF defines the web access control lists (web ACLs) and rule groups that "
            "actually inspect and filter HTTP/HTTPS traffic — it is the underlying filtering "
            "engine. AWS Firewall Manager provides centralised policy management across an "
            "AWS Organization: a WAF security policy created in the Firewall Manager account "
            "automatically deploys the specified WAF web ACL to all in-scope ALBs and CloudFront "
            "distributions in member accounts, including resources created in the future. "
            "GuardDuty does not inspect HTTP application traffic or enforce WAF associations. "
            "Network Firewall inspects traffic at the network layer (Layer 3/4) and requires "
            "significant architecture changes; it does not replace WAF for L7 web filtering. "
            "Config can detect non-compliance but the question requires automatic protection, "
            "not manual remediation after alerting."
        ),
        "tags": [
            "AWS Firewall Manager",
            "Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways)",
            "Securing external network connections to and from the AWS Cloud (for example, VPN, AWS Direct Connect)",
        ],
    },

    # ── Q7: MATCH – AWS Directory Service ────────────────────────────────────
    {
        "id": qid("Directory Service Managed AD AD Connector Simple AD match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "1.1",
        "stem": (
            "A solutions architect is recommending AWS Directory Service options for three "
            "organisations. Match each organisation's requirement to the MOST appropriate "
            "AWS Directory Service option. Each option is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Managed Microsoft AD",
            "B": "AD Connector",
            "C": "Simple AD",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A 15,000-employee enterprise has an on-premises Active Directory domain "
                    "and wants to extend it into AWS, enabling two-way trust relationships, "
                    "AWS-managed multi-AZ Domain Controllers in the cloud, MFA via RADIUS, "
                    "and seamless joining of EC2 instances to the domain."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A company wants its existing on-premises AD users to authenticate against "
                    "AWS services (AWS Management Console, Amazon WorkSpaces) using their "
                    "current credentials and password policies, without deploying any AD "
                    "infrastructure inside AWS."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A startup with 300 cloud-only employees needs basic LDAP and Kerberos "
                    "authentication for Linux workstations joining EC2 instances, without "
                    "requiring trust relationships, Group Policy Objects, or advanced AD features "
                    "— at the lowest possible cost."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "AWS Managed Microsoft AD deploys fully featured Microsoft Active Directory managed "
            "by AWS in a multi-AZ configuration, supports trust relationships with on-premises "
            "AD, and enables advanced AD features like Group Policy and RADIUS MFA — ideal for "
            "large enterprises extending existing AD. AD Connector is a directory gateway (proxy) "
            "that forwards authentication requests to an existing on-premises AD without caching "
            "credentials in AWS and without deploying AD infrastructure in the cloud. Simple AD "
            "is a cost-effective, Samba 4 compatible standalone directory for small-to-medium "
            "deployments (up to 5,000 users) that need basic LDAP and Kerberos support but not "
            "advanced AD features, trust relationships, or schema extensions."
        ),
        "tags": [
            "AWS Directory Service",
            "Applying AWS security best practices to IAM users and root users (for example, multi-factor authentication [MFA])",
            "AWS federated access and identity services (for example, IAM, AWS IAM Identity Center)",
        ],
    },

    # ── Q8: MAMCQ – Amazon Kendra + Comprehend Medical ────────────────────────
    {
        "id": qid("Amazon Kendra Comprehend Medical healthcare document NLP search mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A healthcare organization has 600,000 clinical research PDFs and patient notes. "
            "Doctors need to ask natural-language questions ('What is the first-line treatment "
            "for type 2 diabetes in patients over 65?') and receive precise document excerpts "
            "as answers. The compliance team also needs to automatically extract diagnosed "
            "conditions, medications, and dosages from unstructured patient notes at scale. "
            "Which TWO services should the solutions architect recommend? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Kendra — an intelligent enterprise search service that indexes documents and answers natural-language questions by returning precise text excerpts with relevance ranking",
            "B": "Amazon OpenSearch Service configured with keyword search and Kibana dashboards, using BM25 ranking and phrase matching across the indexed document corpus",
            "C": "Amazon Comprehend Medical — purpose-built NLP that extracts medical entities (diagnoses, medications, dosages, anatomy, procedures) and their relationships from unstructured clinical text",
            "D": "Amazon SageMaker to train a custom BERT-based NLP model on the clinical corpus for both document search and entity extraction",
            "E": "Amazon Textract to extract text from all PDFs followed by keyword-based search using Amazon OpenSearch Service for natural-language queries",
        },
        "explanation": (
            "Amazon Kendra uses ML to build a semantic search index over documents: it "
            "understands natural-language questions and returns the specific paragraph that "
            "answers the question (not just a list of matching documents), making it the right "
            "choice for clinical Q&A search. Amazon Comprehend Medical is a specialized NLP "
            "service trained on medical terminology; it extracts medical entities — diagnoses "
            "(ICD-10-CM), medications (RxNorm), dosages, and their relationships — from "
            "unstructured clinical text without any model training required. OpenSearch keyword "
            "search returns documents matching terms but cannot understand the intent of a "
            "natural-language question. Custom SageMaker models require significant ML expertise, "
            "labeled training data, and ongoing maintenance — unnecessary when purpose-built "
            "services already exist. Textract + OpenSearch still results in keyword search, "
            "not natural-language question answering."
        ),
        "tags": [
            "Amazon Kendra",
            "Amazon Comprehend",
            "Amazon SageMaker AI",
            "Amazon Textract",
        ],
    },

    # ── Q9: MATCH – Governance Services ──────────────────────────────────────
    {
        "id": qid("Service Catalog License Manager Artifact Audit Manager governance match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A solutions architect is assigning AWS governance and compliance services to four "
            "organisational scenarios. Match each scenario to the MOST appropriate service. "
            "The answer bank contains more options than needed."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Service Catalog",
            "B": "AWS License Manager",
            "C": "AWS Artifact",
            "D": "AWS Audit Manager",
            "E": "AWS Health Dashboard",
            "F": "AWS Well-Architected Tool",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A platform-engineering team must allow application teams to provision "
                    "pre-approved infrastructure stacks (VPC + EC2 + RDS) through a self-service "
                    "portal without granting them direct CloudFormation or EC2 console access."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A software asset manager must track BYOL (bring-your-own-license) "
                    "Microsoft SQL Server core usage across 2,500 EC2 instances and Dedicated "
                    "Hosts to prevent over-deployment that could trigger a Microsoft audit."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A compliance officer must download official AWS third-party attestation "
                    "reports — including the SOC 2 Type II report and the PCI DSS Attestation "
                    "of Compliance — to demonstrate that the underlying AWS infrastructure "
                    "meets regulatory requirements to external auditors."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A continuous compliance programme must automatically collect evidence "
                    "(CloudTrail logs, Config evaluation results, Security Hub findings) and "
                    "map it to specific PCI DSS and SOC 2 control requirements, generating "
                    "audit-ready assessment reports."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "AWS Service Catalog allows organizations to define approved cloud products "
            "(CloudFormation templates) and present them as a self-service catalog; users "
            "deploy only approved configurations without needing broad IAM permissions. "
            "License Manager tracks software licenses (BYOL, subscription) across EC2, Dedicated "
            "Hosts, and RDS — enforcing license limits to prevent compliance violations. "
            "AWS Artifact is a self-service portal for on-demand access to AWS compliance "
            "reports (SOC, PCI, ISO, FedRAMP) and AWS agreements. AWS Audit Manager continuously "
            "collects evidence from AWS services and pre-builds assessments for common frameworks "
            "(PCI DSS, SOC 2, HIPAA) — automating the evidence-gathering phase of audits. "
            "Health Dashboard and Well-Architected Tool (E, F) are valid AWS services but do "
            "not address the four scenarios above."
        ),
        "tags": [
            "AWS Service Catalog",
            "AWS License Manager",
            "AWS Artifact",
            "AWS Audit Manager",
            "AWS Well-Architected Tool",
            "AWS Health Dashboard",
            "Determining automation strategies to ensure infrastructure integrity",
        ],
    },

    # ── Q10: MAMCQ – AWS Application Migration Service ────────────────────────
    {
        "id": qid("AWS MGN Application Migration Service physical server lift-and-shift mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A company needs to migrate 300 physical on-premises servers to AWS with minimal "
            "downtime, preserving each server's existing OS, applications, and data exactly as-is. "
            "The project manager wants the ability to conduct non-disruptive cutover tests before "
            "the final migration date, and the team must be able to revert to on-premises if a "
            "test reveals issues. Which TWO statements accurately describe how AWS Application "
            "Migration Service (AWS MGN) meets these requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS MGN installs a lightweight replication agent on each source server that continuously replicates block-level data to a staging area in AWS — eliminating the need to convert physical servers to VMs before migration",
            "B": "AWS MGN requires source servers to run on VMware vSphere or Microsoft Hyper-V; physical bare-metal servers must first be converted to VMs using AWS Server Migration Service before MGN can replicate them",
            "C": "AWS MGN supports non-destructive cutover testing: source servers continue running during test cutover events, so if the test environment has issues the team can simply abandon the test and continue using on-premises",
            "D": "AWS MGN performs file-level replication using an NFS mount, which means only changed files after the initial sync are transferred, significantly reducing replication bandwidth for large servers",
            "E": "AWS MGN automatically terminates the source server's replication agent and shuts down on-premises infrastructure as part of the test cutover process, requiring a rollback procedure to restore on-premises operation",
        },
        "explanation": (
            "AWS MGN (Application Migration Service) is the primary AWS lift-and-shift service: "
            "it uses a lightweight agent installed on source servers to continuously replicate "
            "block-level disk data (OS + applications + data) to a staging EC2 environment in "
            "AWS — it works on physical servers, VMs, and cloud instances without requiring "
            "conversion to VMware or Hyper-V first. The non-destructive test cutover feature "
            "launches test EC2 instances from the replicated data while the source server "
            "continues to replicate and operate normally; if the test fails the team simply "
            "continues on-premises with no rollback needed. MGN does not perform file-level "
            "NFS replication (that is DataSync); it performs block-level disk replication. "
            "MGN does not shut down source servers during test cutovers."
        ),
        "tags": [
            "AWS Application Migration Service",
            "Determining automation strategies to ensure infrastructure integrity",
            "Hybrid compute options (for example, AWS Outposts)",
        ],
    },

    # ── Q11: MAMCQ – Amazon Polly + Amazon Translate ──────────────────────────
    {
        "id": qid("Polly Translate multilingual audio TTS pipeline mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A digital-publishing platform wants to automatically generate audio versions of "
            "English-language articles in 20 languages so users can listen while commuting. "
            "The pipeline must convert English text to 19 other languages and then synthesize "
            "natural-sounding speech in each language with no managed server infrastructure. "
            "Which TWO services form the CORE of this pipeline? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Polly — synthesizes natural-sounding speech from text using neural text-to-speech (NTTS) voices in dozens of languages and accents, storing the MP3/OGG output directly in S3",
            "B": "Amazon Transcribe — converts existing audio recordings of articles narrated by human readers into text transcripts that can then be translated",
            "C": "Amazon Translate — provides batch and real-time neural machine translation from English into 75+ target languages with domain-specific customisation via custom terminology",
            "D": "Amazon Comprehend — extracts key phrases, named entities, and sentiment from each article to improve translation accuracy before passing text to Polly",
            "E": "Amazon Lex — provides a conversational AI interface so users can request articles to be read in their preferred language via a chatbot",
        },
        "explanation": (
            "The pipeline requires two steps: translation (English → 19 languages) and "
            "text-to-speech synthesis (translated text → audio). Amazon Translate provides "
            "neural machine translation for 75+ language pairs and can be called asynchronously "
            "for batch translation of article text at scale. Amazon Polly then converts the "
            "translated text to natural-sounding speech using neural TTS voices, with output "
            "stored directly in S3 — the whole pipeline is serverless when triggered by Lambda. "
            "Transcribe converts audio to text (the opposite direction). Comprehend extracts "
            "linguistic features but does not translate or speak. Lex builds chatbots — it "
            "does not translate text or synthesize speech for content delivery."
        ),
        "tags": [
            "Amazon Polly",
            "Amazon Translate",
            "Serverless technologies and patterns (for example, AWS Lambda, Fargate)",
        ],
    },

    # ── Q12: MAMCQ – AWS Client VPN + AWS RAM ─────────────────────────────────
    {
        "id": qid("Client VPN RAM Transit Gateway hub spoke remote employees mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A company uses a hub-and-spoke network with an AWS Transit Gateway connecting 25 "
            "VPCs across multiple accounts. Remote employees need secure private access to "
            "resources in any of these VPCs from their laptops without exposing resources to "
            "the internet. As new accounts join the organisation, they must inherit connectivity "
            "automatically without any re-provisioning. Which TWO services should the architect "
            "implement? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Client VPN — provides a managed OpenVPN-based SSL/TLS VPN endpoint that employees install on their laptops; attach it to the central VPC's Transit Gateway to route authenticated client traffic into the private network",
            "B": "AWS Site-to-Site VPN — establish IPSec tunnels from each employee's home router to a Virtual Private Gateway in each VPC so employees can access all 25 VPCs directly",
            "C": "AWS Resource Access Manager (RAM) — share the Transit Gateway with all AWS Organisation member accounts so new accounts can attach their VPCs to the existing Transit Gateway automatically",
            "D": "AWS PrivateLink — create Interface VPC Endpoints for every internal service in each of the 25 VPCs so remote employees can access each service over a private endpoint",
            "E": "Internet-facing Network Load Balancers with TLS listener certificates in each VPC so employees connect to internal services over encrypted HTTPS without a VPN client",
        },
        "explanation": (
            "AWS Client VPN is the managed remote-access VPN service: employees install the "
            "OpenVPN client and authenticate (via AD, certificate, or SAML); the VPN endpoint "
            "can be attached to a Transit Gateway so that a single VPN connection routes to all "
            "hub-and-spoke VPCs. AWS Resource Access Manager enables sharing of Transit "
            "Gateways (and other resources) across an AWS Organisation: member accounts "
            "automatically receive access to the shared TGW and can attach their VPCs without "
            "any manual coordination — new accounts inherit connectivity immediately. "
            "Site-to-Site VPN is for site-to-site connectivity between network perimeters, "
            "not individual remote employees. PrivateLink exposes specific services through "
            "NLB-backed endpoints and does not provide general VPC routing for remote employees. "
            "Internet-facing NLBs expose resources to the public internet."
        ),
        "tags": [
            "AWS Client VPN",
            "AWS Resource Access Manager (AWS RAM)",
            "Securing external network connections to and from the AWS Cloud (for example, VPN, AWS Direct Connect)",
            "Determining network configurations that can scale to accommodate future needs",
        ],
    },

    # ── Q13: MATCH – Amazon Kinesis Family ───────────────────────────────────
    {
        "id": qid("Kinesis Data Streams Firehose Video Streams Data Analytics match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A solutions architect must choose the correct Amazon Kinesis service for four "
            "streaming data scenarios. Match each scenario to the MOST appropriate service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Kinesis Data Streams",
            "B": "Amazon Data Firehose",
            "C": "Amazon Kinesis Video Streams",
            "D": "Amazon Kinesis Data Analytics (Amazon Managed Service for Apache Flink)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A smart-city platform ingests live video from 20,000 traffic cameras for "
                    "real-time object detection by an ML model. Video must be durably stored "
                    "with time-indexed access for model inference and forensic playback."
                ),
                "correct": "C",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A clickstream pipeline must capture 2 million events per second, retain "
                    "raw events for 7 days for replay, and allow three independent consumer "
                    "applications to read from different shard positions simultaneously."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A DevOps team needs to deliver application logs from EC2 instances to "
                    "Amazon S3 in Apache Parquet format with automatic compression and batching, "
                    "without writing or maintaining any custom consumer code."
                ),
                "correct": "B",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A fraud detection system must run SQL-based sliding-window aggregations "
                    "on a continuous stream of card transactions to flag anomalies in under "
                    "one second before they are written to the transaction database."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "Kinesis Video Streams ingests, durably stores, and indexes live video streams with "
            "APIs for time-based retrieval and integration with Rekognition or custom ML models — "
            "the only Kinesis service designed for binary video data. Kinesis Data Streams is a "
            "real-time, replay-capable stream with configurable retention (1–365 days), ordered "
            "shards, and support for multiple independent consumer applications (Enhanced Fan-Out) "
            "— ideal for high-throughput event pipelines requiring fan-out. Amazon Data Firehose "
            "is a fully managed delivery service that buffers, batches, and optionally converts "
            "data to Parquet/ORC before loading into S3, Redshift, or OpenSearch — zero consumer "
            "code required. Kinesis Data Analytics / Managed Flink enables real-time SQL or Apache "
            "Flink streaming analytics on Kinesis streams with sub-second processing latency."
        ),
        "tags": [
            "Amazon Kinesis",
            "Amazon Kinesis Video Streams",
            "Selecting appropriate configurations for ingestion",
            "Designing data streaming architectures",
        ],
    },

    # ── Q14: MAMCQ – Amazon AppFlow + AWS Data Exchange ───────────────────────
    {
        "id": qid("AppFlow Salesforce S3 Data Exchange third party datasets mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A retail analytics team has two integration requirements: (1) automatically "
            "transfer Salesforce CRM records into Amazon S3 on a daily schedule with field-level "
            "mapping and PII masking — without writing or maintaining custom integration code, "
            "and (2) subscribe to licensed third-party consumer-spending datasets from external "
            "providers and have them delivered directly into their S3 data lake. Which TWO "
            "services address these requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon AppFlow — a fully managed integration service with no-code flows that connect SaaS sources (Salesforce, ServiceNow, Marketo) to AWS destinations (S3, Redshift) on a schedule, with built-in field mapping and data masking",
            "B": "AWS Glue — a serverless ETL service where a developer writes a Python/Scala script to extract records from the Salesforce REST API and load them into S3 in the desired format",
            "C": "AWS Data Exchange — a marketplace service that lets subscribers find, subscribe to, and receive third-party datasets (from providers like Refinitiv, TransUnion) automatically delivered to S3 or Redshift",
            "D": "Amazon Kinesis Data Firehose with a Salesforce source connector to stream CRM updates to S3 in near-real time without a daily batch schedule",
            "E": "AWS Transfer Family with an SFTP endpoint so third-party data providers can push datasets into S3 using their existing SFTP tooling",
        },
        "explanation": (
            "Amazon AppFlow is purpose-built for SaaS-to-AWS data integration: it provides "
            "pre-built connectors for Salesforce, ServiceNow, Marketo, Zendesk, and other SaaS "
            "applications; supports scheduled, event-triggered, or on-demand flows; and includes "
            "field mapping, format conversion, and masking — all without writing code. AWS Data "
            "Exchange is a data marketplace: data providers (Reuters, TransUnion, Dun & "
            "Bradstreet, etc.) publish datasets and subscribers receive automatic S3 delivery "
            "updates under a managed licensing agreement — eliminating manual data procurement "
            "and delivery negotiations. AWS Glue requires writing custom ETL code. Firehose "
            "does not have a Salesforce source connector in the base service. Transfer Family "
            "with SFTP still requires providers to configure and push files — it doesn't "
            "provide a self-service marketplace subscription model."
        ),
        "tags": [
            "Amazon AppFlow",
            "AWS Data Exchange",
            "Selecting appropriate configurations for ingestion",
            "Data ingestion patterns (for example, frequency)",
        ],
    },

    # ── Q15: MATCH – Observability Stack ─────────────────────────────────────
    {
        "id": qid("CloudWatch X-Ray Managed Grafana Managed Prometheus observability match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A platform team is building an observability stack for a large Kubernetes "
            "workload on Amazon EKS and a serverless application on AWS Lambda. Match each "
            "observability requirement to the MOST appropriate AWS managed service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon CloudWatch",
            "B": "AWS X-Ray",
            "C": "Amazon Managed Grafana",
            "D": "Amazon Managed Service for Prometheus",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "The EKS platform team needs to ingest container-level CPU, memory, and "
                    "custom application metrics in OpenMetrics/Prometheus format from 300 pods "
                    "into a long-term, scalable time-series store — without managing Prometheus "
                    "server infrastructure."
                ),
                "correct": "D",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A NOC team wants a single dashboard that correlates metrics from Prometheus, "
                    "CloudWatch, and OpenSearch Service in real time using Grafana panels and "
                    "alert rules — without provisioning or managing Grafana servers."
                ),
                "correct": "C",
            },
            {
                "id": "sq3",
                "prompt": (
                    "An operations team must automatically scale an EKS node group when a "
                    "custom business metric (orders-per-second) published to a specific metric "
                    "namespace exceeds a threshold for 3 consecutive 1-minute evaluation periods."
                ),
                "correct": "A",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A developer must determine which downstream DynamoDB call or Lambda "
                    "invocation within a complex serverless order-processing workflow adds the "
                    "most latency for a specific failing request, identified by trace ID."
                ),
                "correct": "B",
            },
        ],
        "explanation": (
            "Amazon Managed Service for Prometheus is a fully managed Prometheus-compatible "
            "monitoring service that stores time-series metrics from Kubernetes and other "
            "workloads without operating Prometheus servers; it scales automatically and "
            "retains metrics for 150 days. Amazon Managed Grafana provides fully managed "
            "Grafana workspaces with pre-built connectors to Prometheus, CloudWatch, "
            "OpenSearch, and other data sources — no Grafana server to run. CloudWatch handles "
            "custom metric namespaces, alarms, and Auto Scaling integration; it is the "
            "correct service for creating composite alarms that drive Auto Scaling actions. "
            "X-Ray provides per-request distributed tracing with a service map and trace "
            "timeline showing every subsegment (DynamoDB GetItem, Lambda invocation) along "
            "the request path — enabling per-request latency root-cause analysis."
        ),
        "tags": [
            "Workload visibility (for example, AWS X-Ray)",
            "Amazon Managed Grafana",
            "Amazon Managed Service for Prometheus",
            "Implementing visualization strategies",
        ],
    },

    # ── Q16: MAMCQ – Amazon SageMaker AI Serving + Monitoring ─────────────────
    {
        "id": qid("SageMaker AI real-time endpoint Model Monitor data drift mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A data science team has trained a fraud-detection model in Amazon SageMaker AI "
            "and must deploy it for real-time scoring of transactions with p99 latency under "
            "50 ms. After deployment, the team must automatically detect when the statistical "
            "distribution of incoming feature values deviates significantly from the training "
            "baseline — indicating data quality issues upstream. Which TWO SageMaker capabilities "
            "should the architect configure? (Select TWO.)"
        ),
        "correct": ["A", "D"],
        "difficulty": "HARD",
        "answers": {
            "A": "Deploy the model to a SageMaker Real-Time Inference endpoint with auto-scaling configured on the InvocationsPerInstance metric to handle traffic variability while maintaining p99 latency targets",
            "B": "Use SageMaker Batch Transform to score transactions in micro-batches every 30 seconds, storing results in S3 for downstream consumption by the payment processing system",
            "C": "Host the model on AWS Lambda using a Docker container image with an EFS mount for the model artifact, triggered by API Gateway for each transaction scoring request",
            "D": "Enable SageMaker Model Monitor on the endpoint with a baseline created from the training dataset; schedule monitoring jobs to compare live captured data statistics against the baseline and generate alerts on violations",
            "E": "Configure Amazon CloudWatch Logs Insights to query SageMaker endpoint logs for anomalous prediction confidence scores as a proxy for data distribution changes",
        },
        "explanation": (
            "SageMaker Real-Time Inference endpoints provide synchronous, low-latency model "
            "serving with auto-scaling policies (invocation count, custom metrics) — they are "
            "the only SageMaker serving option that delivers sub-50ms p99 latency for "
            "transactional scoring. SageMaker Model Monitor continuously captures live inference "
            "request data, runs scheduled statistical analysis jobs that compare live data "
            "distributions against a training-data baseline, and generates CloudWatch metrics "
            "and findings when features drift beyond configured thresholds — this is purpose-"
            "built for detecting upstream data quality issues. Batch Transform is asynchronous "
            "and adds latency incompatible with real-time fraud scoring. Lambda has memory and "
            "execution constraints (max 10 GB RAM, 15 min execution) that limit large model "
            "hosting, and EFS adds cold-start latency. CloudWatch Logs Insights analyzes log "
            "text but cannot compute feature distribution statistics across inference requests."
        ),
        "tags": [
            "Amazon SageMaker AI",
            "Workload visibility (for example, AWS X-Ray)",
            "Determining automation strategies to ensure infrastructure integrity",
        ],
    },

    # ── Q17: MAMCQ – AWS Amplify + AWS Device Farm ────────────────────────────
    {
        "id": qid("Amplify Device Farm mobile app backend CI CD real devices mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A startup is building a React Native mobile application with an expected release "
            "cadence of weekly App Store updates. The team needs: (1) a managed backend "
            "providing authentication (Cognito), a GraphQL API (AppSync), and file storage (S3) "
            "provisioned from a single CLI command with a CI/CD pipeline, and (2) automated "
            "compatibility testing across 200 real physical iOS and Android device models before "
            "each release — without managing device infrastructure. Which TWO AWS services "
            "satisfy these requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Amplify — provisions and manages a serverless mobile/web backend (Cognito, AppSync, S3, Lambda) through a CLI-driven workflow and deploys a hosted CI/CD pipeline with preview environments for each Git branch",
            "B": "AWS Elastic Beanstalk — deploys the mobile backend as a containerized Node.js API on managed EC2 instances with a load balancer, auto scaling, and RDS, controlled via the AWS console",
            "C": "AWS Device Farm — executes automated test suites (Appium, XCTest, Espresso) on a fleet of real physical iOS and Android devices managed by AWS, providing device logs, screenshots, and performance metrics for each test run",
            "D": "Amazon EC2 Mac instances running Xcode simulators and Android emulators for automated pre-release compatibility testing managed by the team's CI server",
            "E": "AWS CodeBuild — runs unit and integration tests in a Linux Docker container environment as part of the CI/CD pipeline, providing fast feedback before deploying to the App Store",
        },
        "explanation": (
            "AWS Amplify is purpose-built for mobile and web full-stack development: the "
            "Amplify CLI provisions backend services (Cognito for auth, AppSync for GraphQL, "
            "S3 for storage, Lambda for functions) with a single CLI command; Amplify Hosting "
            "provides CI/CD with per-branch preview environments. AWS Device Farm provides a "
            "managed fleet of real physical iOS and Android devices — not emulators — enabling "
            "automated test execution with Appium, XCTest, and Espresso; AWS manages all "
            "device maintenance and provisioning. Elastic Beanstalk adds operational complexity "
            "and is not optimized for serverless mobile backends. EC2 Mac instances use "
            "simulators/emulators (not real physical devices), require the team to manage the "
            "fleet, and cannot replicate the hardware diversity of 200 real device models. "
            "CodeBuild tests run in Linux containers and cannot test on physical mobile devices."
        ),
        "tags": [
            "AWS Amplify",
            "AWS Device Farm",
            "Serverless technologies and patterns (for example, AWS Lambda, Fargate)",
        ],
    },

    # ── Q18: MAMCQ – Elastic Transcoder + Kinesis Video Streams ──────────────
    {
        "id": qid("Elastic Transcoder Kinesis Video Streams live video VOD transcoding mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A sports streaming company has two requirements: (1) ingest live video streams "
            "from 5,000 stadium cameras to AWS in real time for ML-based player tracking and "
            "highlight detection with time-indexed storage, and (2) transcode on-demand replay "
            "files uploaded to S3 into multiple output resolutions (1080p, 720p, 480p) in MP4 "
            "format for delivery via CloudFront — without managing transcoding servers. "
            "Which TWO services directly address these requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Kinesis Video Streams — ingests live video streams from cameras using the producer SDK, stores them with time-indexed frames, and provides APIs for real-time and historical frame retrieval by ML models",
            "B": "AWS Elemental MediaLive — transcodes live video streams for broadcast-quality output to multiple destinations; AWS Elemental MediaPackage packages the output for adaptive bitrate streaming to end users",
            "C": "Amazon Elastic Transcoder — creates managed transcoding pipelines that convert S3-stored video files into multiple output formats and resolutions without provisioning or managing transcoding infrastructure",
            "D": "AWS Lambda with FFmpeg as a Docker container image triggered by S3 upload events to transcode uploaded video files, with output written back to S3 and a CloudFront distribution invalidation triggered",
            "E": "Amazon S3 Event Notifications triggering AWS Batch jobs running FFmpeg on GPU EC2 spot instances for parallel transcoding of VOD content with automatic scaling",
        },
        "explanation": (
            "Amazon Kinesis Video Streams is purpose-built for live video ingestion, storage, "
            "and ML integration: the producer SDK handles camera streams; frames are durably "
            "stored and time-indexed; GetMedia and GetMediaForFragmentList APIs enable ML "
            "model consumption for real-time and historical analysis. Amazon Elastic Transcoder "
            "is a managed VOD transcoding service: administrators define transcoding pipelines "
            "and job presets (MP4/HLS at multiple resolutions), submit jobs via API or S3 "
            "trigger, and Elastic Transcoder handles all transcoding without managing EC2 "
            "instances. AWS Elemental MediaLive and MediaPackage (option B) are out of scope "
            "for the SAA-C03 exam and are not the correct choice for S3-based VOD transcoding. "
            "Lambda with FFmpeg faces execution time limits (15 minutes max) that may not "
            "accommodate large files; Batch+Spot requires managing compute environments."
        ),
        "tags": [
            "Amazon Elastic Transcoder",
            "Amazon Kinesis Video Streams",
            "Sizes and speeds needed to meet business requirements",
        ],
    },

    # ── Q19: MATCH – Aurora vs DynamoDB vs ElastiCache vs Redshift ────────────
    {
        "id": qid("Aurora DynamoDB ElastiCache Redshift database selection use case match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.3",
        "stem": (
            "A solutions architect is selecting the most appropriate AWS database service for "
            "four different workloads. Match each workload to the BEST-FIT service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Aurora (MySQL/PostgreSQL compatible)",
            "B": "Amazon DynamoDB",
            "C": "Amazon ElastiCache for Redis",
            "D": "Amazon Redshift",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A healthcare application runs complex multi-table JOIN queries with ACID "
                    "transactions on patient records. It requires up to 15 Aurora Replicas for "
                    "read scaling, point-in-time recovery, and automatic failover with minimal "
                    "RTO — and must remain fully MySQL-compatible."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A ride-sharing platform stores driver location updates at 1 million writes "
                    "per second with single-digit millisecond latency, uses composite primary "
                    "keys (driverId + timestamp), and scales automatically without capacity "
                    "planning — supporting global active-active replication across 4 Regions."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "An e-commerce application offloads repeated database reads by caching "
                    "serialized product-catalog objects in a sub-millisecond in-memory store, "
                    "reducing RDS load by 90% during flash sales. Cache eviction uses LRU "
                    "policy with TTL-based expiry."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A business intelligence team runs complex analytical queries joining "
                    "500 TB of historical sales, inventory, and customer data. Queries use "
                    "columnar storage, data compression, and massively parallel processing "
                    "to return results in seconds across petabyte-scale datasets."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "Aurora is a MySQL/PostgreSQL-compatible managed relational database with up to "
            "15 read replicas, automatic storage scaling to 128 TiB, sub-10-second failover, "
            "and ACID transactions — the right choice for complex relational workloads requiring "
            "SQL and read scaling. DynamoDB is a serverless key-value/document store with "
            "guaranteed single-digit millisecond performance at any scale and Global Tables "
            "for multi-region active-active replication — optimized for high-throughput, low-"
            "latency access patterns like location tracking. ElastiCache for Redis provides "
            "sub-millisecond in-memory caching with LRU eviction and TTL, reducing load on "
            "relational databases for repeated read patterns. Redshift is a cloud data warehouse "
            "using columnar storage and MPP architecture — purpose-built for analytical "
            "(OLAP) queries over petabyte-scale datasets."
        ),
        "tags": [
            "Database types and services (for example, relational compared with non-relational, Amazon Aurora, Amazon DynamoDB)",
            "Determining an appropriate database type (for example, Amazon Aurora, Amazon DynamoDB)",
            "Amazon Aurora",
            "Amazon DynamoDB",
            "Amazon ElastiCache",
        ],
    },

    # ── Q20: MAMCQ – Route 53 Latency Routing + Health Checks ─────────────────
    {
        "id": qid("Route 53 latency routing health checks multi-Region failover DNS mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A global SaaS application has primary deployments in us-east-1 and eu-west-1. "
            "The requirements are: (1) users must be routed to the nearest Region for lowest "
            "latency during normal operation, (2) if one Region's ALB becomes unhealthy, "
            "ALL traffic must automatically fail over to the healthy Region within two DNS "
            "TTL cycles, and (3) the architecture must detect health proactively so Route 53 "
            "stops returning the unhealthy endpoint before clients receive errors. Which TWO "
            "Route 53 configurations achieve ALL three requirements? (Select TWO.)"
        ),
        "correct": ["A", "B"],
        "difficulty": "HARD",
        "answers": {
            "A": "Configure Amazon Route 53 Latency routing records for both Regional ALBs — Route 53 evaluates network latency from AWS edge locations to each Region and returns the record with the lowest measured latency for each client",
            "B": "Associate active Route 53 health checks (HTTP/HTTPS probing every 30 seconds) with each Latency routing record and set the record TTL to 60 seconds; Route 53 stops returning a record within one or two TTL cycles after its health check begins failing",
            "C": "Use Route 53 Failover routing with us-east-1 as the Primary and eu-west-1 as the Secondary — this ensures that European users are always served by eu-west-1 under normal conditions",
            "D": "Set the DNS TTL to 300 seconds to reduce DNS query volume to Route 53 during high-traffic periods and prevent resolver cache storms on failover",
            "E": "Use Route 53 Geolocation routing to send North American users to us-east-1 and European users to eu-west-1, with a catch-all record pointing to us-east-1 as a fallback",
        },
        "explanation": (
            "Route 53 Latency routing directs each user to the Region with the lowest measured "
            "network latency from their resolver's location to the AWS Region — satisfying "
            "requirement 1. Associating health checks with Latency routing records enables "
            "automatic failover: Route 53 probes each endpoint every 10–30 seconds; when a "
            "health check fails the configured consecutive failure threshold, Route 53 removes "
            "the unhealthy record from DNS responses and returns only the healthy Region. "
            "Setting TTL to 60 seconds ensures that once the record is removed, resolvers "
            "discard the cached response within 60 seconds, completing failover within two "
            "TTL cycles — satisfying requirements 2 and 3. Failover routing designates "
            "explicit primary/secondary — eu-west-1 users would be routed to us-east-1 during "
            "normal operation if us-east-1 is primary, contradicting requirement 1. A 300-second "
            "TTL delays failover by 5 minutes. Geolocation routing routes by user geography, "
            "not network latency, and does not automatically fail over when a Region is "
            "unhealthy (it requires explicit secondary/default records)."
        ),
        "tags": [
            "Disaster recovery (DR) strategies (for example, backup and restore, pilot light, warm standby, active-active failover, recovery point objective [RPO], recovery time objective [RTO])",
            "Network services with appropriate use cases (for example, DNS)",
            "Amazon Route 53",
            "Determining network configurations that can scale to accommodate future needs",
        ],
    },
]

# ── Load, append, write ───────────────────────────────────────────────────────
data_path = os.path.join(os.path.dirname(__file__), "..", "app", "data", "questions.json")
with open(data_path) as f:
    existing = json.load(f)

existing_ids = {q["id"] for q in existing}
added = 0
for q in new_questions:
    if q["id"] not in existing_ids:
        existing.append(q)
        added += 1
    else:
        print(f"  SKIP (duplicate id): {q['id'][:16]}…")

with open(data_path, "w") as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)

print(f"Done. Added {added} questions. Total: {len(existing)}")
