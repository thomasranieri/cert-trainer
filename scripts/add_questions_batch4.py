#!/usr/bin/env python3
"""Batch 4: 20 MATCH/MAMCQ questions for SAA-C03."""
import json, hashlib, os

EXAM = "AWS Certified Solutions Architect - Associate (SAA-C03)"

def qid(stem):
    return hashlib.sha256((EXAM + stem).encode()).hexdigest()

new_questions = [
    # ── Q1: MATCH – S3 Storage Classes ───────────────────────────────────────
    {
        "id": qid("S3 storage classes Standard IA One Zone Glacier Instant Deep Archive match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "4.1",
        "stem": (
            "A solutions architect is selecting S3 storage classes for five workloads based "
            "on access frequency, durability, and retrieval requirements. Match each workload "
            "to the MOST cost-effective storage class that meets its requirements. "
            "Each class is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "S3 Standard",
            "B": "S3 Standard-IA (Infrequent Access)",
            "C": "S3 One Zone-IA",
            "D": "S3 Glacier Instant Retrieval",
            "E": "S3 Glacier Deep Archive",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A streaming platform serves video thumbnails to millions of users "
                    "globally every minute. Objects are read hundreds of thousands of times "
                    "per day with no tolerance for per-retrieval fees or retrieval delays."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A company stores monthly financial report PDFs that external auditors "
                    "access 2–3 times per year. The objects must survive an Availability Zone "
                    "failure. A per-GB retrieval fee is acceptable given the low access rate."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A development pipeline generates reproducible build artifacts (test "
                    "results, Docker layer caches) that are accessed infrequently. If data "
                    "in one AZ were lost the artifacts could be regenerated from source control. "
                    "Maximum cost savings on storage is the priority."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A media studio archives legacy footage accessed approximately once per "
                    "quarter. When retrieved, playback must begin within milliseconds. A "
                    "90-day minimum storage commitment and a per-GB retrieval fee are acceptable."
                ),
                "correct": "D",
            },
            {
                "id": "sq5",
                "prompt": (
                    "A legal firm retains case files for 7 years to satisfy regulatory "
                    "obligations. Files are effectively never accessed in normal operations "
                    "but must be retrievable within 12 hours if subpoenaed. Minimum storage "
                    "cost across the 7-year retention is paramount."
                ),
                "correct": "E",
            },
        ],
        "explanation": (
            "S3 Standard is designed for frequently accessed data with no retrieval fees "
            "or minimum storage duration. Standard-IA reduces storage cost by ~58% but adds "
            "a per-GB retrieval fee and a 30-day minimum duration — ideal for monthly "
            "reports. One Zone-IA stores data in a single AZ (~20% cheaper than Standard-IA) "
            "and is suitable for reproducible, non-critical data where single-AZ durability "
            "is acceptable. Glacier Instant Retrieval stores data at Glacier pricing "
            "($0.004/GB) but provides millisecond-latency retrieval — designed for archives "
            "requiring immediate access on rare occasions. Glacier Deep Archive "
            "($0.00099/GB) is the lowest-cost S3 class with 12-hour standard retrieval, "
            "suitable for long-term compliance data that is essentially never accessed."
        ),
        "tags": [
            "Storage tiering (for example, cold tiering for object storage)",
            "Selecting the appropriate backup and/or archival solution",
            "Determining the correct storage size for a workload",
            "Amazon S3",
            "Amazon S3 Glacier",
        ],
    },

    # ── Q2: MAMCQ – RDS Proxy + Aurora Serverless v2 ──────────────────────────
    {
        "id": qid("RDS Proxy Aurora Serverless v2 Lambda connections auto-scale mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.3",
        "stem": (
            "A serverless application uses hundreds of Lambda functions that open short-lived "
            "connections to an Amazon Aurora MySQL database. During peak traffic the database "
            "receives thousands of simultaneous connection requests causing "
            "Too many connections errors. The team also needs database compute capacity "
            "to scale automatically based on actual workload without manual capacity "
            "planning. Which TWO services directly address BOTH problems? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon RDS Proxy — maintains a pool of persistent connections to Aurora and multiplexes thousands of Lambda connection requests through the pool, dramatically reducing the number of simultaneous open database connections",
            "B": "Amazon Aurora Multi-AZ deployment — adds a synchronous standby replica in a second AZ that absorbs read connection requests from Lambda functions during peak traffic",
            "C": "Amazon Aurora Serverless v2 — automatically scales database compute capacity in Aurora Capacity Unit (ACU) increments based on actual workload demand, eliminating manual instance resizing",
            "D": "AWS Lambda reserved concurrency set to 10 — limits simultaneous Lambda invocations to reduce peak database connection demand without modifying the database or application",
            "E": "Amazon ElastiCache for Redis — caches Aurora query results in memory so repeated Lambda reads do not open new database connections",
        },
        "explanation": (
            "RDS Proxy is the connection pooling solution for Aurora (and RDS): it maintains "
            "a warm pool of persistent database connections and multiplexes Lambda ephemeral "
            "connections through the pool. A function invoking 1,000 concurrent Lambdas may "
            "translate to only tens of actual database connections — eliminating "
            "'Too many connections' errors without changing application code. Aurora Serverless "
            "v2 automatically scales compute in fine-grained ACU increments (0.5 ACU steps) "
            "based on database load, scaling up for peak traffic and down during quiet periods "
            "without any manual instance resizing or scheduling. Aurora Multi-AZ standby does "
            "not accept read connections during normal operation. Limiting Lambda concurrency "
            "artificially throttles the application. ElastiCache reduces query frequency but "
            "does not solve the connection-count problem for uncached requests."
        ),
        "tags": [
            "Database connections and proxies",
            "Database types and services (for example, serverless, relational compared with non-relational, in-memory)",
            "Serverless technologies and patterns (for example, AWS Lambda, Fargate)",
            "Amazon Aurora",
        ],
    },

    # ── Q3: MATCH – IAM Security Tools ────────────────────────────────────────
    {
        "id": qid("IAM Access Analyzer Permission Boundaries ABAC SCPs security tools match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "1.1",
        "stem": (
            "A solutions architect is selecting IAM security tools for four governance "
            "scenarios. Match each scenario to the MOST appropriate IAM or Organizations "
            "capability. Each capability is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "IAM Access Analyzer",
            "B": "IAM Permission Boundaries",
            "C": "Attribute-Based Access Control (ABAC) with IAM condition keys and resource tags",
            "D": "AWS Organizations Service Control Policies (SCPs)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A security team needs a continuous report of all IAM roles, S3 bucket "
                    "policies, KMS key policies, and Lambda function policies that allow "
                    "access FROM external AWS accounts or public — identifying any unintended "
                    "cross-account or public resource exposure."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A company allows team leads to create IAM roles for their projects. "
                    "The security team must ensure that team-created roles can never grant "
                    "more permissions than the team lead who created them — preventing "
                    "privilege escalation through role creation."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A company wants a single IAM policy that automatically grants each "
                    "developer read/write access to S3 prefixes, DynamoDB items, and SSM "
                    "parameters tagged with the same ProjectCode as the developer's "
                    "IAM principal tag — without maintaining one policy per project."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "An organization administrator must ensure that member accounts cannot "
                    "enable specific high-risk services (e.g., ec2:RunInstances in specific "
                    "Regions) regardless of what IAM policies the member account administrator "
                    "grants to IAM users and roles in those accounts."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "IAM Access Analyzer continuously analyzes resource-based policies (S3 buckets, "
            "IAM roles, KMS keys, Lambda functions, SQS queues, Secrets Manager secrets) "
            "to identify resources reachable from outside the account or Organization trust "
            "zone — providing automated external access audit. Permission Boundaries set the "
            "maximum permissions an IAM entity can have: even if a developer attaches "
            "AdministratorAccess to a role they create, the boundary limits effective "
            "permissions to the intersection of the attached policies and the boundary — "
            "preventing privilege escalation. ABAC uses IAM condition keys (aws:ResourceTag, "
            "aws:PrincipalTag) to write dynamic policies that grant access based on matching "
            "attributes rather than explicit resource ARNs — scales without per-project "
            "policy management. SCPs are Organization-level guardrails applied to all "
            "principals in member accounts (except the management account root), overriding "
            "any IAM permission in those accounts regardless of who granted it."
        ),
        "tags": [
            "Applying AWS security best practices to IAM users and root users (for example, multi-factor authentication [MFA])",
            "Designing a flexible authorization model that includes IAM users, groups, roles, and policies",
            "Designing a security strategy for multiple AWS accounts (for example, AWS Control Tower, service control policies [SCPs])",
            "IAM",
        ],
    },

    # ── Q4: MAMCQ – AWS Lake Formation + Glue Crawlers ────────────────────────
    {
        "id": qid("Lake Formation column row access control Glue Crawler Data Catalog mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A company is building a data lake on Amazon S3. Requirements are: (1) different "
            "analyst teams must see only specific columns of a shared dataset — the PII team "
            "must be blocked from columns containing names and SSNs when querying through "
            "Amazon Athena, and (2) new data sources (RDS MySQL databases, S3 prefixes with "
            "CSV files) must be automatically discovered, schema-inferred, and registered "
            "into a central searchable catalog without writing custom code. Which TWO services "
            "address both requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Lake Formation — provides fine-grained table, column, row-filter, and cell-level access control on the AWS Glue Data Catalog, enforced transparently for queries from Athena, Redshift Spectrum, and EMR",
            "B": "Amazon Macie — automatically discovers PII columns in S3 objects and applies S3 bucket policies to restrict access to sensitive prefixes, replacing the need for column-level access control",
            "C": "AWS Glue Crawlers — automatically connect to S3 prefixes and JDBC sources (RDS, Redshift), infer schemas and partition structures, and populate table metadata into the AWS Glue Data Catalog on a configurable schedule",
            "D": "Amazon Athena workgroup IAM policies — restrict which columns specific IAM groups can SELECT in Athena queries by defining column-level conditions in workgroup configuration",
            "E": "AWS Glue DataBrew — visually profiles data quality in S3 and automatically applies masking transformations to PII columns, replacing column-level access control with data transformation",
        },
        "explanation": (
            "AWS Lake Formation is the governance layer for data lakes: it wraps the Glue "
            "Data Catalog with fine-grained permissions (table, column, row-filter, cell-"
            "level) that are enforced transparently when Athena, Redshift Spectrum, or EMR "
            "queries the catalog — analysts see only the columns and rows their Lake Formation "
            "permissions allow, with no S3 bucket policy changes required. AWS Glue Crawlers "
            "are the catalog population mechanism: they automatically crawl S3 prefixes, "
            "JDBC sources, and DynamoDB tables; infer schemas (including partition projection "
            "for partitioned data); and register or update table definitions in the Glue Data "
            "Catalog — eliminating manual DDL. Macie discovers PII but cannot enforce Athena "
            "column-level access. Athena workgroups control query execution but have no "
            "column-level access control. DataBrew masks data at transformation time, "
            "not at query time."
        ),
        "tags": [
            "Data access and governance",
            "Building and securing data lakes",
            "AWS Lake Formation",
            "AWS Glue",
            "Amazon Athena",
        ],
    },

    # ── Q5: MATCH – EC2 Purchasing Options ────────────────────────────────────
    {
        "id": qid("On-Demand Standard Reserved Convertible Reserved Spot Savings Plan EC2 match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "4.2",
        "stem": (
            "A solutions architect is recommending EC2 purchasing options for five workloads. "
            "Match each workload to the purchasing option that minimises cost while meeting "
            "its requirements. Each option is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "On-Demand Instances",
            "B": "Standard Reserved Instances (1- or 3-year)",
            "C": "Convertible Reserved Instances (1- or 3-year)",
            "D": "Spot Instances",
            "E": "Compute Savings Plan (1- or 3-year)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A machine learning training job runs on GPU instances for 6-hour bursts "
                    "with no fixed schedule. Jobs checkpoint every 30 minutes to S3 and can "
                    "tolerate interruptions. Maximum cost savings is the priority."
                ),
                "correct": "D",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A production database server on a specific EC2 instance family (R6i.4xlarge) "
                    "in us-east-1 has run 24/7 for 2 years with a stable workload. The team "
                    "is committed to the same instance family for 3 more years and wants the "
                    "maximum possible discount."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A company's workload requires committed pricing savings but the engineering "
                    "team anticipates migrating from the current M5 instance family to the "
                    "newer M7i or switching from Linux to Windows OS within the next 2 years."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A startup deploys a proof-of-concept for 10 days to evaluate feasibility. "
                    "The workload has unknown resource requirements and may need to be terminated "
                    "or resized at any time."
                ),
                "correct": "A",
            },
            {
                "id": "sq5",
                "prompt": (
                    "A company wants a single commitment that automatically applies savings "
                    "to AWS Lambda, AWS Fargate, AND EC2 instances across any instance family, "
                    "size, Region, or OS — without managing separate Reserved Instance purchases "
                    "for each service."
                ),
                "correct": "E",
            },
        ],
        "explanation": (
            "Spot Instances (up to 90% discount) are ideal for interruption-tolerant, "
            "checkpointable workloads like ML training. Standard Reserved Instances provide "
            "the highest discount (up to 72% on 3-year All Upfront) for a specific instance "
            "family/size/Region/OS commitment. Convertible Reserved Instances offer a lower "
            "discount (~54% max) but can be exchanged for different instance types, families, "
            "or OSes during the commitment term — right for workloads where requirements may "
            "change. On-Demand has no commitment or discount — suitable for unpredictable, "
            "short-term, or variable workloads. Compute Savings Plans (up to 66% discount) "
            "apply automatically to any EC2 instance (regardless of family/size/Region/OS), "
            "Fargate, and Lambda usage up to the committed $/hour amount — the most "
            "flexible committed pricing option."
        ),
        "tags": [
            "AWS purchasing options (for example, Spot Instances, Reserved Instances, Savings Plans)",
            "Determining cost-effective AWS compute services with appropriate use cases (for example, AWS Lambda, Amazon EC2, AWS Fargate)",
            "Determining appropriate scaling methods and strategies for elastic workloads (for example, horizontal compared with vertical, EC2 hibernation)",
        ],
    },

    # ── Q6: MAMCQ – CloudTrail + EventBridge Automated Remediation ────────────
    {
        "id": qid("CloudTrail EventBridge Lambda remediation SSH 0.0.0.0 root login mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A security team requires automated responses to two events within seconds of "
            "their occurrence in an AWS account: (1) any security group modification that "
            "allows inbound SSH (port 22) from 0.0.0.0/0 must be immediately revoked by "
            "calling RevokeSecurityGroupIngress, and (2) any AWS Management Console login by "
            "the root user must trigger an immediate SNS notification to the security team. "
            "Which TWO components form the correct event-driven remediation architecture?"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "An Amazon EventBridge rule matching CloudTrail EC2 API events (AuthorizeSecurityGroupIngress) with a condition checking for port 22 and 0.0.0.0/0 CIDR — the rule targets a Lambda function that evaluates and revokes the offending rule",
            "B": "An AWS Config managed rule (restricted-ssh) with a periodic 24-hour evaluation schedule to detect security groups allowing 0.0.0.0/0 on port 22, with SNS notification triggered when violations are found",
            "C": "An Amazon EventBridge rule matching CloudTrail ConsoleLogin events where userIdentity.type is 'Root' — the rule targets an Amazon SNS topic that immediately notifies the security team",
            "D": "Amazon GuardDuty with the EC2 threat detection feature to flag security groups with 0.0.0.0/0 SSH rules and root login events as high-severity findings sent to Security Hub for triage",
            "E": "A CloudWatch Metric Filter on the CloudTrail log group matching root login patterns, with a CloudWatch Alarm set to evaluate over a 5-minute period and notify via SNS",
        },
        "explanation": (
            "Amazon EventBridge continuously processes CloudTrail API events in near-real-"
            "time: an EventBridge rule matching AuthorizeSecurityGroupIngress events can "
            "inspect the request parameters for port 22 and 0.0.0.0/0 CIDR and invoke a "
            "Lambda function within seconds to call RevokeSecurityGroupIngress — achieving "
            "immediate automated remediation. A separate EventBridge rule matching "
            "ConsoleLogin events with userIdentity.type=Root routes to SNS and fires within "
            "seconds of the login. AWS Config periodic evaluations run every 24 hours or "
            "on configuration change — too slow for 'within seconds' response. GuardDuty "
            "produces findings but they are threat intelligence results, not event-driven "
            "rule triggers, and have processing delays. CloudWatch Metric Filters with a "
            "5-minute alarm evaluation period are too slow for immediate response to root "
            "login events."
        ),
        "tags": [
            "Determining automation strategies to ensure infrastructure integrity",
            "Applying AWS security best practices to IAM users and root users (for example, multi-factor authentication [MFA])",
            "Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways)",
            "Amazon EventBridge",
            "AWS CloudTrail",
        ],
    },

    # ── Q7: MATCH – CloudWatch Feature Set ────────────────────────────────────
    {
        "id": qid("CloudWatch Logs Insights Contributor Insights Metric Streams App Insights match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A platform team needs different Amazon CloudWatch capabilities for four "
            "observability use cases. Match each use case to the MOST appropriate "
            "CloudWatch feature. Each feature is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon CloudWatch Logs Insights",
            "B": "Amazon CloudWatch Contributor Insights",
            "C": "Amazon CloudWatch Metric Streams",
            "D": "Amazon CloudWatch Application Insights",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "During a live incident, an engineer needs to run ad-hoc SQL-like queries "
                    "against Lambda function JSON logs to filter on error codes, sum request "
                    "counts by customerId, and extract fields from nested JSON — in real time."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "An operations team wants to automatically identify the top-10 API "
                    "Gateway resource paths generating the most 5XX errors per hour, "
                    "surfacing the highest-impact contributors without writing custom "
                    "analytics queries or maintaining aggregation pipelines."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A FinOps team wants to continuously export all CloudWatch metrics "
                    "from production EC2 instances and RDS databases in real time to an "
                    "Amazon Kinesis Firehose delivery stream for ingestion into a "
                    "third-party observability platform (Datadog, Splunk)."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A .NET application team needs CloudWatch to automatically detect "
                    "application components, map dependencies between EC2, RDS, and ELB, "
                    "recommend a baseline set of metrics and alarms for their stack, and "
                    "surface anomalies with correlated log events — without manual setup."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "CloudWatch Logs Insights provides an interactive query language (similar to "
            "SQL) for analyzing log data in real time: it supports field extraction, "
            "filtering, aggregation, sorting, and time-series visualization directly "
            "in the CloudWatch console — ideal for live incident investigation. "
            "Contributor Insights applies rule-based analysis to logs to automatically "
            "identify the top-N contributors to a metric (e.g., highest-error API paths, "
            "most-expensive customers) using rolling time windows — no custom analytics "
            "code required. Metric Streams continuously send CloudWatch metric data to "
            "Kinesis Firehose (and from there to S3, Redshift, or HTTP endpoints) in near-"
            "real time with low latency — enabling third-party platform integration. "
            "Application Insights auto-discovers .NET, Java, and database application "
            "topologies, recommends key metrics and alarms based on AWS and community "
            "best practices, and correlates metrics with log patterns to surface root causes."
        ),
        "tags": [
            "Workload visibility (for example, AWS X-Ray)",
            "Implementing visualization strategies",
            "Amazon CloudWatch",
        ],
    },

    # ── Q8: MAMCQ – S3 CRR + S3 Object Lock (Compliance Mode) ─────────────────
    {
        "id": qid("S3 CRR Cross-Region Replication Object Lock Compliance 7-year immutable mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.3",
        "stem": (
            "A financial services company stores trade confirmations in Amazon S3 in "
            "us-east-1. Regulations require: (1) an automated copy in a different AWS "
            "Region (eu-west-1) that is created within minutes of the original write without "
            "manual processes, and (2) ALL copies (source and destination) must be "
            "immutable for exactly 7 years — even the AWS account root user must be "
            "unable to delete or overwrite any object during this period. Which TWO "
            "configurations achieve both requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Enable S3 Cross-Region Replication (CRR) on the us-east-1 source bucket with a replication rule targeting the eu-west-1 destination bucket — new objects are replicated automatically within minutes using S3-managed replication",
            "B": "Schedule an AWS DataSync task to copy new S3 objects from us-east-1 to eu-west-1 every 15 minutes using an automated CloudWatch Events trigger",
            "C": "Enable S3 Object Lock in Compliance mode on both the source and destination buckets with a retention period of 7 years — Compliance mode prevents any user or process, including the AWS root user, from deleting or overwriting locked objects before the retention date",
            "D": "Enable S3 Versioning on both buckets and configure lifecycle rules to transition non-current object versions to Glacier after 30 days, retaining all versions for 7 years through the lifecycle policy",
            "E": "Enable S3 MFA Delete on both buckets requiring the root user's MFA device for all object deletions, creating a two-factor authorization gate for any delete operation",
        },
        "explanation": (
            "S3 Cross-Region Replication (CRR) automatically replicates new object writes "
            "(and optionally updates and deletes) from the source bucket to a destination "
            "bucket in a different Region using asynchronous replication — typically completing "
            "within minutes. CRR requires S3 Versioning on both buckets. S3 Object Lock in "
            "Compliance mode makes individual object versions write-once-read-many (WORM) "
            "for the specified retention period: NO user or AWS process — including the "
            "account root user — can delete or shorten the retention on a Compliance-mode "
            "locked object once set; the mode cannot be changed or removed during retention. "
            "DataSync copies on a schedule (minimum 15-minute batches) rather than "
            "automatically on each write. Versioning + lifecycle policies preserve versions "
            "but don't prevent deletion (versions can still be permanently deleted). MFA "
            "Delete requires MFA for delete-marker creation but the root user with MFA "
            "device can still delete — Compliance mode provides stronger guarantees."
        ),
        "tags": [
            "Implementing data backups and replications",
            "Implementing policies for data access, lifecycle, and protection",
            "Storage options and characteristics (for example, durability, replication)",
            "Amazon S3",
        ],
    },

    # ── Q9: MATCH – AWS Glue Components ──────────────────────────────────────
    {
        "id": qid("Glue Crawler ETL Job Data Catalog DataBrew components match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A solutions architect is selecting the correct AWS Glue component for four "
            "data engineering tasks. Match each task to the MOST appropriate Glue component. "
            "Each component is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Glue Crawler",
            "B": "AWS Glue ETL Job",
            "C": "AWS Glue Data Catalog",
            "D": "AWS Glue DataBrew",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A data engineering team needs a serverless metadata repository that "
                    "stores table schemas, partition information, and data locations, making "
                    "data in S3 and RDS discoverable by Amazon Athena, Amazon Redshift "
                    "Spectrum, and Amazon EMR — all via a single unified metadata API."
                ),
                "correct": "C",
            },
            {
                "id": "sq2",
                "prompt": (
                    "The same team needs to automatically scan new S3 prefixes daily, "
                    "detect schemas for CSV, JSON, Parquet, and Avro formats, identify "
                    "partitions, and register or update table definitions in the central "
                    "metadata store — without writing any schema-inference code."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A daily pipeline must join clickstream data from S3 with customer "
                    "records from Amazon RDS, apply custom aggregation logic in Apache "
                    "Spark, deduplicate records, and write the result as Parquet files "
                    "to a new S3 prefix on a managed Spark cluster."
                ),
                "correct": "B",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A data analyst (non-engineer) needs to interactively profile 200 GB "
                    "of messy CSV files, visualise data quality statistics, fix date "
                    "format inconsistencies, remove duplicate rows, and standardise "
                    "column values using a visual point-and-click interface — without "
                    "writing Python or Spark code."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "The Glue Data Catalog is the centralised, persistent, serverless metadata "
            "repository: it stores table definitions (column names, types, partitions, "
            "locations) and is natively integrated with Athena, Redshift Spectrum, and EMR "
            "as their default metastore. Glue Crawlers are the auto-discovery agents: "
            "they connect to data stores, infer schemas (including nested types and "
            "partitions), and populate or update Catalog table definitions on a schedule. "
            "Glue ETL Jobs are managed Apache Spark environments for complex data "
            "transformations: they support Python shell and Spark scripts, DynamicFrame "
            "APIs, and job bookmarks for incremental processing. AWS Glue DataBrew is a "
            "visual data preparation tool: analysts profile datasets (null counts, "
            "distributions, patterns), apply 250+ built-in transformations through a "
            "point-and-click interface, and publish recipes without writing code."
        ),
        "tags": [
            "AWS Glue",
            "Data transformation services with appropriate use cases (for example, AWS Glue)",
            "Building and securing data lakes",
        ],
    },

    # ── Q10: MAMCQ – ECS vs EKS Platform Selection ────────────────────────────
    {
        "id": qid("ECS EKS platform selection Kubernetes operators Kubeflow CRD mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A company must choose between Amazon ECS and Amazon EKS for two workloads. "
            "Workload A is a new cloud-native microservices application whose small team "
            "has no Kubernetes expertise and wants AWS-native integration with minimal "
            "operational complexity. Workload B is an ML team's existing Kubeflow-based "
            "MLOps pipeline that relies on Kubernetes Operators, custom resource definitions "
            "(CRDs), Helm chart deployments, and GPU scheduling. Which TWO statements "
            "correctly guide the platform decision? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon ECS with the Fargate launch type is the lower-overhead choice for Workload A — it uses AWS-native constructs (task definitions, services, clusters) without a Kubernetes control plane, and integrates natively with ALB, IAM, CloudWatch, and Service Discovery",
            "B": "Amazon ECS supports Kubernetes Operators and custom resource definitions through the AWS ECS CRD Bridge — allowing Kubeflow pipelines to be run on ECS without modifications",
            "C": "Amazon EKS is the correct platform for Workload B — it runs fully managed Kubernetes and natively supports Kubeflow Operators, Helm charts, custom CRDs, GPU node scheduling (with EC2 launch type using p4d/g5 instances), and the full Kubernetes ecosystem",
            "D": "Amazon EKS fully manages the Kubernetes control plane AND worker node scaling, patching, and OS updates — customers have no operational responsibility for any Kubernetes infrastructure",
            "E": "Amazon ECS and Amazon EKS have equivalent operational complexity; the primary selection criterion should be whether the team prefers JSON task definitions or YAML pod specs",
        },
        "explanation": (
            "Amazon ECS is a native AWS container orchestration service using task definitions, "
            "services, and clusters — integrating deeply with ALB (for HTTP routing), IAM "
            "(for task roles), CloudWatch, and App Mesh. Teams without Kubernetes experience "
            "can deploy and operate ECS with minimal learning curve. Amazon EKS is managed "
            "Kubernetes: AWS manages the control plane (API server, etcd, scheduler) but "
            "customers manage worker nodes (EC2 or Fargate) and Kubernetes resources. EKS "
            "fully supports the standard Kubernetes ecosystem: CRDs, Operators, Helm, "
            "Kubeflow, GPU scheduling (via device plugins on EC2 nodes), and any CNCF "
            "tooling — making it the only viable choice for Kubeflow-based MLOps. ECS has "
            "no concept of Kubernetes Operators or CRDs. EKS customers are responsible for "
            "worker node patching and upgrades even though the control plane is managed — "
            "using managed node groups reduces but does not eliminate node operational tasks."
        ),
        "tags": [
            "The orchestration of containers (for example, Amazon ECS, Amazon EKS)",
            "Determining when to use containers",
            "Amazon ECS",
            "Amazon EKS",
        ],
    },

    # ── Q11: MATCH – RDS Multi-AZ vs Read Replicas vs Aurora Global ───────────
    {
        "id": qid("RDS Multi-AZ Read Replicas Aurora Global Database HA DR match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A solutions architect is recommending Amazon RDS and Aurora capabilities for "
            "three different availability and scaling requirements. Match each requirement "
            "to the MOST appropriate database feature. Each feature is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon RDS Multi-AZ deployment",
            "B": "Amazon RDS Read Replicas",
            "C": "Amazon Aurora Global Database",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A web application's read workload has grown to 20× the write workload. "
                    "The team needs to distribute SELECT queries across multiple database "
                    "endpoints to reduce load on the primary instance — accepting slightly "
                    "stale reads due to asynchronous replication lag."
                ),
                "correct": "B",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A business-critical application requires automatic database failover "
                    "within 60–120 seconds when the primary AZ becomes unavailable, with "
                    "synchronous replication guaranteeing zero data loss at failover and "
                    "no changes to the application's connection string."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A global banking application requires an Aurora database that serves "
                    "low-latency reads from three secondary Regions, achieves near-zero RPO "
                    "using storage-level replication with typical lag under 1 second, and "
                    "can complete a managed cross-Region failover in under 1 minute."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "RDS Read Replicas use asynchronous replication to scale read-heavy workloads: "
            "up to 15 replicas for Aurora (5 for other engines) each provide their own "
            "connection endpoint; replicas may have slight replication lag, making them "
            "unsuitable for strongly consistent reads. RDS Multi-AZ uses synchronous "
            "replication to a standby in a second AZ; AWS automatically fails over to the "
            "standby (DNS endpoint unchanged) within 60–120 seconds without data loss — "
            "the standby does NOT serve read traffic during normal operation. Aurora Global "
            "Database uses physical storage-level replication to propagate changes to up to "
            "5 secondary Regions with sub-second lag (typically <1s); secondary clusters "
            "serve local reads; managed cross-Region failover completes in under 1 minute "
            "with near-zero RPO — designed for globally distributed applications and "
            "multi-Region DR."
        ),
        "tags": [
            "Database replication (for example, read replicas)",
            "Disaster recovery (DR) strategies (for example, backup and restore, pilot light, warm standby, active-active failover, recovery point objective [RPO], recovery time objective [RTO])",
            "Amazon Aurora",
        ],
    },

    # ── Q12: MAMCQ – CloudFront Signed URLs + Geo Restriction ─────────────────
    {
        "id": qid("CloudFront Signed URLs geo restriction content protection mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A premium video streaming service distributes licensed content through Amazon "
            "CloudFront. Two requirements must be enforced at the CDN edge: (1) only "
            "authenticated subscribers with a time-limited token may access individual video "
            "files — unauthenticated requests must receive 403 Forbidden, and (2) users in "
            "countries where the content is not licensed must be blocked at CloudFront before "
            "the request reaches the origin. Which TWO CloudFront features should the "
            "architect configure? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "CloudFront Signed URLs — each video URL is signed with an RSA private key, embedding a policy with an expiration time and (optionally) allowed IP range; CloudFront validates the signature at the edge and returns 403 for invalid or expired requests",
            "B": "AWS WAF rate limiting rules attached to the CloudFront distribution — limits the number of requests per IP address per minute, preventing unauthenticated bulk access to video files",
            "C": "CloudFront Geo Restriction (geographic restrictions) — blocks content delivery to specified countries based on the viewer's IP geolocation determined at the CloudFront edge, before the request reaches the origin",
            "D": "AWS Shield Advanced applied to the CloudFront distribution — automatically detects and mitigates volumetric DDoS attacks targeting the video delivery infrastructure from restricted countries",
            "E": "Lambda@Edge on the Origin Request trigger to call an authentication microservice for every cache miss, validating the subscriber's session token before fetching content from the S3 origin",
        },
        "explanation": (
            "CloudFront Signed URLs embed a cryptographic signature (using an RSA key pair) "
            "and an access policy (expiration, allowed IPs, allowed paths) directly in the "
            "URL: CloudFront edge servers verify the signature and policy before serving any "
            "content, returning 403 for invalid, expired, or tampered URLs. This is the "
            "canonical solution for per-subscriber, time-limited content authorization. "
            "CloudFront Geo Restriction uses MaxMind IP geolocation to determine the viewer's "
            "country at the edge and blocks or allows delivery based on a configurable "
            "allowlist or blocklist — with no origin round-trip for blocked countries. "
            "WAF rate limiting prevents scraping but does not authenticate individual "
            "subscribers or provide time-limited access. Shield Advanced protects against "
            "volumetric DDoS, not unauthorized subscriber access. Lambda@Edge for "
            "authentication works but adds latency and cost compared to the built-in "
            "Signed URL mechanism."
        ),
        "tags": [
            "Implementing policies for data access, lifecycle, and protection",
            "Securing external network connections to and from the AWS Cloud (for example, VPN, AWS Direct Connect)",
            "Amazon CloudFront",
        ],
    },

    # ── Q13: MATCH – AWS Organizations Policy Types ───────────────────────────
    {
        "id": qid("SCPs Tag Policies Backup Policies AI Services Opt-out Organizations match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "1.1",
        "stem": (
            "A solutions architect is assigning AWS Organizations policy types to four "
            "governance scenarios. Match each scenario to the MOST appropriate "
            "Organizations policy type. Each type is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Service Control Policies (SCPs)",
            "B": "Tag Policies",
            "C": "Backup Policies",
            "D": "AI Services Opt-out Policies",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A data residency policy requires that no EC2 instance can be launched "
                    "in the ap-southeast-1 (Singapore) Region across any member account. "
                    "Even if an account administrator grants RunInstances permission in IAM, "
                    "the launch must be denied."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A FinOps team wants to enforce that all new resources in every member "
                    "account carry the tags 'Environment' (values: prod, staging, dev) and "
                    "'CostCenter' (values: a valid 4-digit code) — flagging non-compliant "
                    "resources for remediation."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A compliance officer wants daily backup plans (30-day retention) and "
                    "monthly backup plans (7-year retention) automatically deployed via AWS "
                    "Backup to all EC2 EBS volumes and RDS instances in all member accounts "
                    "without any per-account action."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A privacy counsel must ensure that Amazon Comprehend, Amazon Rekognition, "
                    "Amazon Textract, and Amazon Translate never use the organisation's "
                    "content to improve AWS's AI/ML models — across all current and future "
                    "member accounts."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "SCPs are guardrails that restrict what actions principals in member accounts "
            "can perform — a Deny SCP on ec2:RunInstances with a region condition prevents "
            "launches in the restricted Region regardless of IAM permissions. Tag Policies "
            "define tag key naming conventions and allowed values; AWS enforces them across "
            "member accounts and reports non-compliant resources through the Organizations "
            "console. Backup Policies deploy AWS Backup backup plans to member accounts via "
            "Organizations, automatically applying backup schedules and retention rules "
            "without per-account configuration. AI Services Opt-out Policies allow an "
            "organization to opt all member accounts out of having their content used by "
            "AWS for AI model improvement — a single policy covers all listed AI services "
            "for current and future accounts."
        ),
        "tags": [
            "Designing a security strategy for multiple AWS accounts (for example, AWS Control Tower, service control policies [SCPs])",
            "Determining automation strategies to ensure infrastructure integrity",
            "AWS Organizations",
            "Designing appropriate backup and retention policies (for example, snapshot frequency)",
        ],
    },

    # ── Q14: MAMCQ – Amazon OpenSearch Service ────────────────────────────────
    {
        "id": qid("OpenSearch full-text search Dashboards Kibana product catalog log analytics mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "An e-commerce company needs two capabilities: (1) a product-catalog search "
            "backend supporting full-text queries with fuzzy matching, relevance scoring, "
            "and autocomplete suggestions, and (2) real-time operational dashboards showing "
            "error-rate trends, p99 latency, and user-activity patterns from application "
            "logs shipped from Amazon EC2 instances. Which TWO Amazon OpenSearch Service "
            "capabilities directly address these requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "OpenSearch's Lucene-based full-text search engine with custom analyzers, fuzzy matching (Levenshtein edit distance), BM25 relevance scoring, and completion suggester for product-catalog autocomplete",
            "B": "OpenSearch Serverless — automatically scales search capacity to zero between product searches, eliminating idle search costs for low-traffic windows",
            "C": "OpenSearch Dashboards — provides Kibana-compatible visualizations (line charts, heatmaps, data tables), saved searches, index-pattern discovery, and alerting for real-time operational log analytics dashboards",
            "D": "Amazon Kinesis Data Firehose delivery stream with OpenSearch as the destination — ships logs from EC2 instances to OpenSearch with automatic index creation, satisfying both search and analytics requirements without additional services",
            "E": "OpenSearch Machine Learning Commons — automatically classifies product queries using built-in NLP models for relevance re-ranking without requiring Comprehend or SageMaker",
        },
        "explanation": (
            "Amazon OpenSearch Service's core full-text search engine (based on Lucene) "
            "supports custom analyzers, fuzzy queries, BM25 relevance, autocomplete "
            "(completion suggester), and phrase-matching — purpose-built for product "
            "catalog search. OpenSearch Dashboards (the managed Kibana equivalent) provides "
            "interactive visualizations, index-pattern management, Discover (log browsing), "
            "Visualize (charts), and Dashboard (multi-panel views) — the standard AWS tool "
            "for real-time log analytics. These two capabilities address both requirements "
            "within a single managed service. OpenSearch Serverless does not scale to zero; "
            "it has a minimum capacity OCU cost even when idle. Kinesis Firehose can deliver "
            "logs to OpenSearch (requirement 2) but does not address product-catalog search "
            "(requirement 1). ML Commons is an advanced feature not central to the stated "
            "requirements."
        ),
        "tags": [
            "Data analytics and visualization services with appropriate use cases (for example, Amazon Athena, AWS Lake Formation, Amazon QuickSuite)",
            "Implementing visualization strategies",
            "Amazon OpenSearch Service",
        ],
    },

    # ── Q15: MATCH – Route 53 Routing Policies ────────────────────────────────
    {
        "id": qid("Route 53 Weighted Geolocation Geoproximity Multivalue routing policies match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A solutions architect is configuring Amazon Route 53 routing policies for four "
            "use cases. Match each use case to the MOST appropriate Route 53 routing policy. "
            "Each policy is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Weighted routing",
            "B": "Geolocation routing",
            "C": "Geoproximity routing (Route 53 Traffic Flow)",
            "D": "Multivalue Answer routing",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A team is performing a canary release of a new API version. Initially "
                    "5% of traffic should reach the new version; after validation the weight "
                    "shifts to 50%, then 100% — all using the same DNS name with no "
                    "changes to client configuration."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A legal firm's SaaS application must route EU users exclusively to "
                    "servers in eu-west-1 and North American users to us-east-1, regardless "
                    "of measured network latency, to comply with GDPR data residency "
                    "requirements."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A startup runs servers in us-east-1 and eu-central-1. After adding a "
                    "new location in us-west-2, the team wants to gradually expand the "
                    "geographic catchment area of us-west-2 by adjusting a bias value, "
                    "without hard-coding geographic boundaries. Route 53 Traffic Flow is "
                    "already in use."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A small application runs on 6 web servers (no load balancer). The team "
                    "wants Route 53 to return up to 8 healthy server IP addresses per DNS "
                    "query so clients can select from multiple IPs — providing simple "
                    "client-side load distribution with health-check filtering."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "Weighted routing assigns a numeric weight to each record and distributes queries "
            "proportionally — ideal for canary or blue/green deployments where a precise "
            "traffic split percentage is required. Geolocation routing maps user locations "
            "(continent, country, subdivision) to specific records regardless of latency — "
            "ensuring data residency compliance by routing EU users to EU endpoints. "
            "Geoproximity routing (available through Route 53 Traffic Flow) routes traffic "
            "based on the geographic location of resources and users, with an adjustable "
            "bias value that expands or shrinks the geographic area a resource attracts — "
            "providing fine-grained geographic load shifting. Multivalue Answer routing "
            "returns up to 8 healthy records per query (filtered by health checks) in random "
            "order, allowing clients to use any returned IP — providing basic load "
            "distribution without requiring a load balancer."
        ),
        "tags": [
            "Network services with appropriate use cases (for example, DNS)",
            "Disaster recovery (DR) strategies (for example, backup and restore, pilot light, warm standby, active-active failover, recovery point objective [RPO], recovery time objective [RTO])",
            "Amazon Route 53",
        ],
    },

    # ── Q16: MAMCQ – Amazon Redshift Serverless + Spectrum ────────────────────
    {
        "id": qid("Redshift Serverless Spectrum S3 data lake analytics ad-hoc mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.3",
        "stem": (
            "A company stores 10 TB of structured sales data in Amazon RDS MySQL where "
            "complex analytical queries take 30+ minutes. An analytics team also has 500 TB "
            "of semi-structured historical data in Amazon S3 (Parquet format) that they need "
            "to join with the structured data without running ETL jobs. The team runs "
            "unpredictable ad-hoc queries with no consistent workload pattern. Which TWO "
            "Amazon Redshift capabilities should the architect recommend? (Select TWO.)"
        ),
        "correct": ["B", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Redshift RA3 nodes — separate storage and compute, automatically archiving cold data to S3 with AQUA acceleration for sub-second query performance on the 10 TB structured dataset",
            "B": "Amazon Redshift Serverless — automatically provisions and scales Redshift compute for ad-hoc query workloads without managing clusters; billed per Redshift Processing Unit (RPU) second consumed",
            "C": "Amazon Redshift Spectrum — allows Redshift queries to scan data directly from S3 (Parquet, ORC, CSV) at query time, enabling JOINs between Redshift tables and S3-based external tables without ETL ingestion",
            "D": "Amazon Redshift cross-Region snapshot copy — replicates the Redshift data warehouse to eu-west-1 for disaster recovery, improving query performance through data locality for European analysts",
            "E": "Amazon Redshift Concurrency Scaling — automatically adds transient clusters to serve concurrent read queries when the main cluster queue is full, improving performance for spikes in simultaneous users",
        },
        "explanation": (
            "Amazon Redshift Serverless eliminates cluster management for ad-hoc workloads: "
            "it automatically provisions capacity when queries arrive and scales to zero "
            "between queries — paying only per RPU-second consumed rather than for "
            "continuously running cluster nodes. This is the ideal choice when query patterns "
            "are unpredictable. Amazon Redshift Spectrum extends Redshift SQL queries to "
            "data stored in S3: by defining external tables in the Glue Data Catalog, "
            "analysts can JOIN Redshift tables with S3 Parquet files in a single query, "
            "with the query engine pushing down predicates to S3 — no ETL required to "
            "ingest the 500 TB of historical data. RA3 nodes are best for steady, "
            "predictable workloads requiring cluster management. Cross-Region snapshots are "
            "for DR, not query performance. Concurrency Scaling handles simultaneous user "
            "bursts on a managed cluster, not unpredictable ad-hoc workloads."
        ),
        "tags": [
            "Database types and services (for example, serverless, relational compared with non-relational, in-memory)",
            "Data analytics and visualization services with appropriate use cases (for example, Amazon Athena, AWS Lake Formation, Amazon QuickSuite)",
            "Amazon Redshift",
        ],
    },

    # ── Q17: MATCH – AWS Config Rule Types ────────────────────────────────────
    {
        "id": qid("Config managed rules custom Lambda rules conformance packs proactive rules match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A solutions architect is implementing AWS Config compliance capabilities. "
            "Match each compliance requirement to the MOST appropriate AWS Config "
            "capability. Each capability is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Config managed rules",
            "B": "AWS Config custom Lambda rules",
            "C": "AWS Config conformance packs",
            "D": "AWS Config proactive evaluation",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A security team needs out-of-the-box compliance checks for common "
                    "misconfigurations: S3 buckets with public ACLs, EC2 instances without "
                    "VPC, and EBS volumes that are unencrypted — using AWS-provided rule "
                    "definitions without writing any evaluation code."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A governance team must enforce a company-specific policy: EC2 instances "
                    "must have an 'Approved' tag with a value from a list stored in AWS SSM "
                    "Parameter Store. No AWS managed rule supports this dynamic lookup logic."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A compliance officer needs to deploy a complete PCI DSS compliance "
                    "assessment (containing 28 Config rules mapped to PCI DSS controls) "
                    "across all 25 accounts in the AWS Organisation using a single "
                    "policy document and track aggregate compliance status."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A DevSecOps team wants AWS Config to evaluate whether a new "
                    "CloudFormation resource change will violate security policies BEFORE "
                    "CloudFormation deploys the change — preventing non-compliant resources "
                    "from being created in the first place."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "AWS Config managed rules are pre-built compliance checks written by AWS (e.g., "
            "s3-bucket-public-read-prohibited, encrypted-volumes, ec2-instance-in-vpc) "
            "that evaluate resources against AWS best practices and compliance frameworks — "
            "no code required. Custom Lambda rules evaluate resources against organisation-"
            "specific logic written in Lambda functions; the Lambda receives configuration "
            "item data and returns compliant/non-compliant — required for dynamic policy "
            "lookups. Conformance packs bundle multiple Config rules and remediation actions "
            "into a YAML template deployable across an Organisation via StackSets, with "
            "aggregate compliance reporting across accounts. Proactive evaluation integrates "
            "AWS Config with CloudFormation hooks: rules are evaluated against the planned "
            "resource configuration before deployment, blocking non-compliant changes."
        ),
        "tags": [
            "Determining automation strategies to ensure infrastructure integrity",
            "AWS Config",
            "AWS CloudFormation",
        ],
    },

    # ── Q18: MAMCQ – Transit Gateway + Network Firewall Inspection ────────────
    {
        "id": qid("Transit Gateway Network Firewall centralised inspection VPC east-west mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A large enterprise uses AWS Transit Gateway to connect 200 VPCs across multiple "
            "accounts and on-premises networks. The security team requires ALL east-west "
            "traffic between VPCs to pass through a centralised intrusion detection and "
            "prevention system (IDPS) transparently — without making changes to individual "
            "VPC routing or application configuration. Which TWO services form the correct "
            "centralised inspection architecture? (Select TWO.)"
        ),
        "correct": ["A", "B"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Transit Gateway with a dedicated inspection VPC attachment and Transit Gateway route tables configured so all inter-VPC traffic is directed to the inspection VPC's appliance subnet before continuing to its destination",
            "B": "AWS Network Firewall deployed in the inspection VPC — provides stateful Layer 3-7 packet inspection, Suricata-compatible intrusion detection and prevention rules, and domain-based traffic filtering for all transiting east-west flows",
            "C": "AWS WAF attached directly to the Transit Gateway as a transit policy to inspect Layer 7 HTTP/HTTPS traffic between VPCs without requiring a dedicated inspection VPC",
            "D": "Amazon GuardDuty with VPC Flow Log analysis to detect suspicious east-west traffic patterns and automatically update security group deny rules to block suspicious flows between VPCs",
            "E": "Inter-VPC security groups referencing each other across all 200 VPCs to restrict which VPCs can communicate with which other VPCs, replacing the need for inline IDPS inspection",
        },
        "explanation": (
            "The centralised inspection architecture for Transit Gateway works by configuring "
            "TGW route tables to 'hairpin' all east-west VPC-to-VPC traffic through an "
            "inspection VPC: pre-inspection routes send all traffic to the inspection VPC "
            "attachment; post-inspection routes return traffic to the destination VPC. This "
            "creates transparent inline inspection without modifying individual VPCs. AWS "
            "Network Firewall is deployed in the inspection VPC: it provides stateful and "
            "stateless packet inspection at Layers 3–7, Suricata-compatible IDS/IPS rule "
            "groups, and domain/IP filtering — satisfying the IDPS requirement. AWS WAF "
            "operates at Layer 7 (HTTP/HTTPS) and is attached to ALBs, CloudFront, or API "
            "Gateway — not to Transit Gateway. GuardDuty provides threat intelligence but "
            "is not an inline IDPS and security group modifications are too slow for real-"
            "time traffic blocking. Security groups control connectivity but do not inspect "
            "packet content."
        ),
        "tags": [
            "Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways)",
            "Network routing, topology, and peering (for example, AWS Transit Gateway, VPC peering)",
            "AWS Network Firewall",
        ],
    },

    # ── Q19: MATCH – Amazon FSx Options ──────────────────────────────────────
    {
        "id": qid("FSx Windows File Server Lustre NetApp ONTAP file system match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.1",
        "stem": (
            "A solutions architect is selecting Amazon FSx file system options for three "
            "workloads with distinct requirements. Match each workload to the MOST "
            "appropriate FSx file system. Each option is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon FSx for Windows File Server",
            "B": "Amazon FSx for Lustre",
            "C": "Amazon FSx for NetApp ONTAP",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A company running Windows-based EC2 instances needs a shared SMB file "
                    "share with full Active Directory integration, DFS Namespace support, "
                    "Windows shadow copies, and NTFS ACL compatibility for a Microsoft "
                    "SQL Server log shipping target."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A genomics HPC cluster running on AWS uses Slurm to schedule "
                    "parallel compute jobs. The shared storage must deliver millions of "
                    "IOPS with sub-millisecond latency, be POSIX-compatible, support "
                    "striped layouts, and link directly to an S3 data repository for "
                    "importing input files and exporting results."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "An enterprise is migrating a NetApp storage environment to AWS and "
                    "needs a managed file system that simultaneously supports NFS, SMB, "
                    "and iSCSI protocols, provides native ONTAP features (SnapMirror "
                    "replication, FlexClone, deduplication), and can tier cold data "
                    "automatically to Amazon S3."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "FSx for Windows File Server is a fully managed Windows-native file system: "
            "it provides SMB protocol, Active Directory authentication, DFS namespaces, "
            "shadow copies (point-in-time snapshots visible via Windows), and full NTFS "
            "ACLs — the correct choice for Windows workloads and SQL Server integration. "
            "FSx for Lustre is a fully managed, high-performance parallel file system "
            "optimised for HPC: it delivers sub-millisecond latency and hundreds of GB/s "
            "throughput; it is POSIX-compatible and directly links to S3 buckets as a "
            "persistent repository, enabling automatic import/export of data between "
            "Lustre and S3 — ideal for genomics and ML workloads. FSx for NetApp ONTAP "
            "is a fully managed ONTAP service offering native multi-protocol access "
            "(NFS, SMB, iSCSI), all ONTAP data management capabilities (SnapMirror, "
            "FlexClone, deduplication, compression), and automatic S3 tiering — "
            "designed for enterprise storage migrations."
        ),
        "tags": [
            "Storage options and characteristics (for example, durability, replication)",
            "Hybrid storage options (for example, AWS DataSync, AWS Transfer Family, AWS Storage Gateway)",
            "Amazon FSx (for all types)",
        ],
    },

    # ── Q20: MAMCQ – IAM Permission Boundaries + IAM Access Analyzer ──────────
    {
        "id": qid("IAM Permission Boundaries Access Analyzer developer role creation privilege escalation mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.1",
        "stem": (
            "A company grants developers the ability to create IAM roles for their Lambda "
            "functions. The security team has two concerns: (1) developers must not be able "
            "to create Lambda execution roles with permissions exceeding their own IAM "
            "permissions — preventing privilege escalation through role creation, and "
            "(2) team-created roles that grant unintended cross-account access to S3 buckets "
            "or other resources must be automatically detected. Which TWO IAM capabilities "
            "address both concerns? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "IAM Permission Boundaries attached to developer IAM roles — the boundary defines the MAXIMUM permissions any role the developer creates can have; even if the developer attaches AdministratorAccess to a Lambda role, effective permissions are the intersection of the attached policies and the boundary",
            "B": "AWS Organizations SCPs denying iam:CreateRole and iam:AttachRolePolicy in developer accounts — prevents all role creation, ensuring developers cannot create any execution roles",
            "C": "IAM Access Analyzer with the account or Organization as the zone of trust — continuously analyzes IAM role policies, S3 bucket policies, and KMS key policies to automatically generate findings for any resource or role accessible from outside the trust boundary",
            "D": "AWS Config managed rule (iam-no-inline-policy) with automatic remediation that detaches inline IAM policies from Lambda execution roles — ensuring no custom permissions are attached",
            "E": "Amazon CloudTrail with a CloudWatch Metric Filter that alerts when iam:CreateRole is called — providing a notification to the security team within 5 minutes so they can manually review the newly created role",
        },
        "explanation": (
            "IAM Permission Boundaries are the correct mechanism for delegated administration: "
            "a developer's IAM role has a permission boundary that limits what maximum "
            "permissions any role they create can have. Even if the developer explicitly "
            "attaches AdministratorAccess to a new Lambda role, the effective permissions "
            "are intersected with the boundary — the Lambda role cannot exceed the developer's "
            "own ceiling. IAM Access Analyzer continuously monitors resource-based policies "
            "using automated reasoning to identify any principal from outside the zone of "
            "trust (account or Organisation) that can access resources — generating findings "
            "for cross-account role trust policies, S3 bucket policies, and KMS key grants "
            "with external access. Denying all role creation breaks the developer workflow. "
            "Config's iam-no-inline-policy detaches inline policies but doesn't prevent "
            "overly permissive managed policy attachments. CloudTrail alerting is reactive "
            "and manual, not automated detection of cross-account access."
        ),
        "tags": [
            "Designing a role-based access control strategy (for example, AWS STS, role switching, cross-account access)",
            "Designing a flexible authorization model that includes IAM users, groups, roles, and policies",
            "IAM",
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
