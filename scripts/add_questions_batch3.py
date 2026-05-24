#!/usr/bin/env python3
"""Batch 3: 20 MATCH/MAMCQ questions for SAA-C03."""
import json, hashlib, os

EXAM = "AWS Certified Solutions Architect - Associate (SAA-C03)"

def qid(stem):
    return hashlib.sha256((EXAM + stem).encode()).hexdigest()

new_questions = [
    # ── Q1: MATCH – S3 Storage Strategies ────────────────────────────────────
    {
        "id": qid("S3 Multipart Transfer Acceleration Batch Operations Presigned URLs match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A solutions architect must recommend the correct Amazon S3 capability for each "
            "data access scenario. Match each scenario to the MOST appropriate S3 feature. "
            "Each feature is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "S3 Multipart Upload",
            "B": "Amazon S3 Transfer Acceleration",
            "C": "Amazon S3 Batch Operations",
            "D": "S3 Pre-signed URLs",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A genomics research lab in Sydney uploads 100 GB sequencing files to an "
                    "S3 bucket in us-east-1. Current upload times exceed 4 hours; the team "
                    "needs dramatically faster transfers without changing the S3 bucket Region "
                    "or modifying their existing storage architecture."
                ),
                "correct": "B",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A compliance team must retroactively apply new lifecycle tags to "
                    "2 billion S3 objects, copy 500 million objects to a Glacier destination, "
                    "and delete 300 million expired objects — all without writing custom "
                    "Lambda code or managing compute infrastructure."
                ),
                "correct": "C",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A media company uploads 80 GB video files from editing workstations. "
                    "Uploads frequently fail midway over unstable WAN links, and each "
                    "failure requires restarting the entire transfer from the beginning."
                ),
                "correct": "A",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A healthcare portal needs to generate temporary download links for "
                    "private patient lab reports stored in a non-public S3 bucket. The links "
                    "must expire after 24 hours and must be usable without AWS credentials."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "S3 Transfer Acceleration routes upload traffic from distant locations through the "
            "nearest CloudFront edge location onto AWS's optimised backbone network, "
            "accelerating geographically distant transfers by 50–500%. S3 Batch Operations "
            "applies S3 operations (Copy, Tag, Restore, Delete, Lambda invocation) to billions "
            "of objects using a manifest without writing custom compute logic. S3 Multipart "
            "Upload splits large objects into independently-uploadable parts (minimum 5 MB "
            "each, recommended for objects > 100 MB): if a part fails, only that part is "
            "retransmitted, enabling reliable resumable uploads. Pre-signed URLs embed "
            "temporary AWS credentials in a URL, granting time-limited access to a specific "
            "private S3 object without requiring the recipient to have AWS credentials."
        ),
        "tags": [
            "Designing appropriate storage strategies (for example, batch uploads to Amazon S3 compared with individual uploads)",
            "Selecting appropriate configurations for ingestion",
            "Amazon S3",
        ],
    },

    # ── Q2: MAMCQ – AWS Backup Centralised + Vault Lock ───────────────────────
    {
        "id": qid("AWS Backup Vault Lock centralized multi-account policy mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "4.1",
        "stem": (
            "A company must implement a centralised backup strategy across EC2 (EBS volumes), "
            "RDS, Amazon EFS, and DynamoDB spanning 25 AWS accounts. Requirements are: "
            "(1) a single backup policy (daily/7-day retention, weekly/1-year retention) "
            "enforced automatically across all accounts and resource types, and "
            "(2) recovery points must be immutable — even account administrators and root "
            "users must not be able to delete backups before the minimum retention period. "
            "Which TWO actions fulfill both requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Enable AWS Backup with an AWS Organizations integration; create a backup plan with daily and weekly rules, tag-based resource assignment, and cross-account backup to a central vault — the plan is automatically enforced in all member accounts",
            "B": "Create individual resource-specific backup schedules in each account: RDS automated backups, EBS DLM policies, EFS backup, and DynamoDB PITR — then audit them monthly using AWS Config",
            "C": "Enable AWS Backup Vault Lock on the backup vault in Compliance mode, specifying a minimum retention period; Compliance mode prevents even the AWS root user from deleting recovery points before the minimum retention expires",
            "D": "Enable Amazon S3 Object Lock on the S3 bucket that stores the backup data in WORM mode with a Compliance retention policy matching the backup schedule",
            "E": "Create IAM permission boundaries in each member account that deny DeleteBackup, DeleteRecoveryPoint, ec2:DeleteSnapshot, and rds:DeleteDBSnapshot actions to prevent any principal from removing backups",
        },
        "explanation": (
            "AWS Backup with AWS Organizations integration allows a central account to create "
            "backup plans and deploy them across all member accounts automatically via service-"
            "managed policies, covering EC2 (EBS), RDS, EFS, DynamoDB, Aurora, and more from "
            "a single policy definition. AWS Backup Vault Lock in Compliance mode is the only "
            "mechanism that makes recovery points truly immutable: once Compliance mode is "
            "activated, no user (including root and AWS Support) can delete recovery points "
            "before the minimum retention period — it cannot be disabled after a grace period. "
            "Separate per-service schedules per account multiply operational overhead "
            "significantly. S3 Object Lock does not protect AWS Backup recovery points stored "
            "in Backup Vaults (Backup Vaults are not S3 buckets). IAM boundaries do not "
            "restrict the root user and can be circumvented by anyone with IAM admin access."
        ),
        "tags": [
            "Designing appropriate backup and retention policies (for example, snapshot frequency)",
            "Implementing data backups and replications",
            "Selecting the appropriate backup and/or archival solution",
            "AWS Backup",
        ],
    },

    # ── Q3: MAMCQ – API Gateway Usage Plans + SQS Throttling ──────────────────
    {
        "id": qid("API Gateway Usage Plans API keys per-customer throttling SQS backend mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A company exposes a processing API via Amazon API Gateway to 500 enterprise "
            "customers. Premium customers are contracted for 1,000 requests per second (RPS); "
            "free-tier customers are limited to 10 RPS. The backend Lambda processes each "
            "request in 5–30 seconds and must not be overwhelmed by traffic bursts — all "
            "in-flight requests must be durably preserved if Lambda concurrency is saturated. "
            "Which TWO architectural components address BOTH the per-customer throttling and "
            "the backend overflow requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "API Gateway Usage Plans with API Keys — assign premium customers a usage plan with throttle rate 1,000 RPS and burst 2,000; free-tier customers get 10 RPS; each API Key enforces its plan independently",
            "B": "API Gateway stage-level default throttling set to 50,000 RPS with a Lambda authorizer that tracks per-customer request counts in DynamoDB and returns a 429 after the limit is exceeded",
            "C": "Amazon SQS standard queue between API Gateway and the processing Lambda — API Gateway sends each accepted request to SQS; Lambda polls the queue with reserved concurrency set to the maximum sustainable backend rate",
            "D": "Enable API Gateway response caching on the stage with a 60-second TTL so that repeated requests from the same customer are served from cache without hitting the backend Lambda",
            "E": "Amazon SNS topic between API Gateway and the processing Lambda — SNS invokes Lambda for each request and automatically throttles delivery to match Lambda's available concurrency",
        },
        "explanation": (
            "API Gateway Usage Plans are the native mechanism for per-client throttling: each "
            "API Key is associated with a Usage Plan that defines a token-bucket throttle rate "
            "(steady-state RPS) and burst limit; requests exceeding the limit receive an HTTP "
            "429 without reaching the backend. Amazon SQS provides durable, elastic queuing "
            "between the API layer and the backend: API Gateway sends accepted requests to "
            "SQS; Lambda's reserved concurrency setting limits simultaneous processing to the "
            "backend's sustainable rate; requests queue safely during bursts and are not "
            "dropped. A Lambda authorizer checking DynamoDB adds per-request latency, "
            "complexity, and race-condition risks. API Gateway caching helps repeated reads "
            "but does not queue mutating or unique processing requests. SNS does NOT queue "
            "durably — it delivers immediately and invokes Lambda directly without buffering; "
            "if Lambda concurrency is exhausted, SNS will drop messages after retry attempts."
        ),
        "tags": [
            "Selecting an appropriate throttling strategy",
            "Serverless technologies and patterns (for example, AWS Lambda, Fargate)",
            "Amazon SQS",
            "Amazon API Gateway",
        ],
    },

    # ── Q4: MATCH – Event-Driven Architecture ────────────────────────────────
    {
        "id": qid("EventBridge SNS SQS Step Functions event-driven patterns match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A solutions architect is designing event-driven components for a microservices "
            "platform. Match each messaging requirement to the MOST appropriate AWS service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon EventBridge",
            "B": "Amazon SNS",
            "C": "Amazon SQS",
            "D": "AWS Step Functions",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A payment pipeline executes a 12-step workflow: validate → charge card → "
                    "reserve inventory → send confirmation → ship → notify → archive. Each step "
                    "calls a different microservice. Failed steps must retry with exponential "
                    "backoff and failed workflows must pause for human review."
                ),
                "correct": "D",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A SaaS integration hub routes events from 40 third-party sources "
                    "(Salesforce, GitHub, PagerDuty) to downstream consumers based on event "
                    "type and content. New event patterns and targets can be added without "
                    "changing producers, using a content-based routing schema registry."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "An 'order placed' event must be simultaneously delivered to three "
                    "independent consumers — inventory, shipping, and analytics — with each "
                    "consumer operating independently. Failure in one consumer must not "
                    "affect delivery to the others."
                ),
                "correct": "B",
            },
            {
                "id": "sq4",
                "prompt": (
                    "An order-processing service experiences unpredictable submission bursts. "
                    "A downstream fulfillment system processes at a fixed rate of 100 orders "
                    "per minute. Burst orders must be durably retained and processed in FIFO "
                    "order without duplication during the catchup period."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "Step Functions orchestrates multi-step workflows with state, retries, error "
            "catching, parallel execution, human approval tasks, and audit history — the right "
            "choice for long-running, stateful business processes. EventBridge is an event bus "
            "with content-based routing rules, SaaS partner event sources, schema discovery, "
            "and the ability to add new targets without touching producers — ideal for "
            "decoupled event routing. SNS provides fan-out pub/sub: one publish delivers to "
            "all subscriptions simultaneously and independently. SQS provides durable queuing "
            "with configurable FIFO ordering and visibility timeouts; combined with dead-letter "
            "queues, it protects against message loss and decouples variable producers from "
            "fixed-rate consumers."
        ),
        "tags": [
            "Queuing and messaging concepts (for example, publish/subscribe)",
            "Serverless technologies and patterns (for example, AWS Lambda, Fargate)",
            "Workflow orchestration (for example, AWS Step Functions)",
            "Amazon SQS",
            "Amazon SNS",
        ],
    },

    # ── Q5: MATCH – Caching Strategies ────────────────────────────────────────
    {
        "id": qid("DAX ElastiCache Redis CloudFront API Gateway caching strategies match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.3",
        "stem": (
            "A solutions architect is adding caching to four different application components "
            "to improve performance and reduce costs. Match each caching requirement to the "
            "MOST appropriate AWS caching service. Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon DynamoDB Accelerator (DAX)",
            "B": "Amazon ElastiCache for Redis",
            "C": "Amazon CloudFront",
            "D": "API Gateway Stage-level Response Caching",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A product-search Lambda function issues 80,000 DynamoDB GetItem calls "
                    "per second. 90% of queries request the same popular items. The team "
                    "wants microsecond cache hits via a DynamoDB-compatible API without "
                    "changing a single line of application code."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A real-time gaming session service needs an in-memory store for sorted "
                    "leaderboard sets, pub/sub messaging between servers, and Lua scripting "
                    "for atomic multi-key operations — shared across 500 application servers "
                    "with optional data persistence to survive restarts."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A global media portal serves the same HTML pages, images, and JavaScript "
                    "bundles to millions of users across 60 countries. The origin web servers "
                    "in us-east-1 are under heavy load from geographically diverse traffic."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A mobile app calls 8 REST endpoints that return mostly static reference "
                    "data (exchange rates, country codes) updated every 10 minutes. The team "
                    "wants to serve cached responses directly from the API layer without "
                    "invoking Lambda for repeated identical requests."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "DAX is a fully managed, DynamoDB-compatible in-memory cache: it intercepts the "
            "same DynamoDB API calls (GetItem, Query, Scan) transparently, requiring zero "
            "application code changes, and returns cache hits in microseconds. ElastiCache "
            "for Redis is a general-purpose in-memory data structure server supporting "
            "complex data types (sorted sets, hashes, streams), pub/sub, Lua scripting, "
            "and optional persistence (AOF, RDB) — purpose-built for session stores, "
            "leaderboards, and inter-service messaging. CloudFront caches content at 450+ "
            "global edge locations, reducing origin load and serving global users with low "
            "latency. API Gateway response caching stores endpoint responses in a managed "
            "cache per stage, eliminating Lambda invocations and backend calls for repeated "
            "identical GET requests within the configured TTL."
        ),
        "tags": [
            "Caching strategies",
            "Amazon DynamoDB",
            "Amazon ElastiCache",
            "Amazon CloudFront",
        ],
    },

    # ── Q6: MAMCQ – NAT Gateway per-AZ + S3 Gateway Endpoint ─────────────────
    {
        "id": qid("NAT Gateway per-AZ S3 Gateway VPC Endpoint cost reduction cross-AZ mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "4.4",
        "stem": (
            "A company's AWS bill shows $22,000/month in networking costs. Traffic analysis "
            "reveals two problems: (1) all three Availability Zones route internet-bound and "
            "S3-bound traffic through a SINGLE NAT Gateway in us-east-1a, generating "
            "$0.01/GB cross-AZ charges for traffic originating in us-east-1b and us-east-1c, "
            "and (2) EC2 instances in private subnets send millions of S3 API calls through "
            "the NAT Gateway, incurring $0.045/GB NAT data processing charges. Which TWO "
            "changes eliminate the MOST cost? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Deploy a dedicated NAT Gateway in EACH Availability Zone so that EC2 instances route internet traffic through their local AZ NAT Gateway, eliminating cross-AZ data transfer charges",
            "B": "Replace all NAT Gateways with NAT instances (EC2 t3.small) to reduce the hourly compute cost; NAT instances can be sized to handle the traffic volume",
            "C": "Create an S3 Gateway VPC Endpoint and add the endpoint route to all private subnet route tables — S3 traffic will route over AWS's internal network at no data processing charge and no cross-AZ transfer charge",
            "D": "Enable S3 Transfer Acceleration on the S3 buckets to reduce the amount of data transferred through the NAT Gateway by optimising TCP connections",
            "E": "Move the EC2 workloads to AWS Lambda to eliminate NAT Gateway dependency; Lambda connects to S3 directly without requiring a NAT Gateway in the VPC",
        },
        "explanation": (
            "Deploying one NAT Gateway per AZ is the standard architecture for eliminating "
            "cross-AZ data transfer charges: traffic from each AZ routes to its local NAT "
            "Gateway ($0.045/GB for data processing) instead of crossing to another AZ "
            "($0.01/GB) first. S3 Gateway VPC Endpoints route S3 traffic entirely within "
            "AWS's internal network: they are free (no hourly charge, no per-GB charge) and "
            "completely eliminate NAT Gateway data processing charges for S3 traffic — often "
            "the largest single line item in NAT cost breakdowns. NAT instances are cheaper "
            "per hour but require patching, custom high-availability setups, and don't "
            "eliminate per-GB data processing costs; for data-heavy S3 workloads, the "
            "Gateway Endpoint saves far more. Transfer Acceleration optimises upload paths "
            "but does not eliminate NAT processing. Lambda without a VPC can access S3 "
            "directly, but migrating workloads to Lambda is a major re-architecture, not "
            "a networking configuration change."
        ),
        "tags": [
            "Reviewing existing workloads for network optimizations",
            "NAT gateways (for example, NAT instance costs compared with NAT gateway costs)",
            "Configuring appropriate network routes to minimize network transfer costs (for example, Region to Region, Availability Zone to Availability Zone, private to public, AWS Global Accelerator, VPC endpoints)",
            "Amazon VPC",
        ],
    },

    # ── Q7: MATCH – Auto Scaling Policies ─────────────────────────────────────
    {
        "id": qid("Target Tracking Step Scaling Scheduled Scaling EC2 Auto Scaling match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.2",
        "stem": (
            "A solutions architect is configuring EC2 Auto Scaling for three different workload "
            "patterns. Match each workload to the MOST appropriate Auto Scaling policy type. "
            "Each policy type is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Target Tracking Scaling",
            "B": "Step Scaling",
            "C": "Scheduled Scaling",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A stock exchange application scales based on trading volume. At 9:30 AM "
                    "EST, markets open and trading volume jumps 10×; at 4:00 PM EST markets "
                    "close and volume drops immediately. The team wants to pre-provision "
                    "additional capacity 10 minutes before market open each weekday."
                ),
                "correct": "C",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A web API tier should maintain 60% average CPU utilization across the "
                    "fleet. The Auto Scaling group should add or remove instances "
                    "automatically to keep CPU near 60% without requiring the team to define "
                    "specific step sizes for each alarm threshold."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A media transcoding fleet has erratic CPU spikes. At 70% CPU, add "
                    "2 instances; at 85% CPU, add 4 instances; at 95% CPU, add 8 instances "
                    "immediately. Each alarm threshold requires a different scaling magnitude "
                    "to maintain throughput SLAs."
                ),
                "correct": "B",
            },
        ],
        "explanation": (
            "Scheduled Scaling changes capacity at specific times based on a recurring "
            "schedule (cron or fixed date/time) — ideal for predictable, time-based traffic "
            "patterns like market open/close where demand shifts are known in advance. "
            "Target Tracking Scaling continuously adjusts the Auto Scaling group to maintain "
            "a specified metric at a target value (e.g., CPU at 60%); the policy calculates "
            "the required scaling action automatically without defining alarm thresholds. "
            "Step Scaling triggers different scaling actions at different alarm thresholds "
            "with configurable step adjustments — suitable for workloads where the magnitude "
            "of the scaling response should vary with the severity of the metric breach."
        ),
        "tags": [
            "Determining appropriate scaling methods and strategies for elastic workloads (for example, horizontal compared with vertical, EC2 hibernation)",
            "Scalability capabilities with appropriate use cases (for example, Amazon EC2 Auto Scaling, AWS Auto Scaling)",
            "Amazon EC2 Auto Scaling",
        ],
    },

    # ── Q8: MAMCQ – CloudFront (static) + Global Accelerator (dynamic) ─────────
    {
        "id": qid("CloudFront static Global Accelerator dynamic non-cacheable API mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.4",
        "stem": (
            "A global fintech application serves two traffic types from AWS: (1) static assets "
            "(JavaScript, CSS, images) that should be edge-cached globally for lowest latency, "
            "and (2) real-time transaction API calls that are unique per request (cannot be "
            "cached) but require consistent, low-jitter network performance and must not "
            "traverse unreliable public internet paths between clients and the ALB. Which TWO "
            "services address these two distinct requirements? (Select TWO.)"
        ),
        "correct": ["B", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon CloudFront with a cache behavior TTL of 0 for all transaction API paths — CloudFront passes all API requests through to the origin ALB while caching static assets under a separate cache behavior with long TTL",
            "B": "AWS Global Accelerator — provides two static anycast IP addresses that route client requests over the AWS global backbone network to the nearest Regional ALB endpoint, reducing jitter and packet loss for latency-sensitive dynamic traffic",
            "C": "Amazon CloudFront with Origin Access Control and cache behaviors configured for long TTL for static assets (/*.js, /*.css, /images/*) — content is served from 450+ edge PoPs worldwide with no origin round-trip for cached objects",
            "D": "Amazon Route 53 Latency routing — directs each API request to the nearest AWS Region based on DNS resolver latency; traffic still traverses the public internet from the client to the Regional ALB",
            "E": "AWS Direct Connect — provides a private, dedicated connection from end-user devices worldwide to AWS for both static and dynamic traffic, eliminating public internet transit",
        },
        "explanation": (
            "AWS Global Accelerator uses anycast IP addresses that route client traffic onto "
            "the AWS global backbone at the nearest edge location, avoiding the congestion "
            "and unpredictability of the public internet for the entire path to the origin "
            "ALB — providing consistent low-jitter performance for non-cacheable dynamic "
            "traffic. Amazon CloudFront caches content (static assets) at 450+ PoPs worldwide: "
            "JavaScript, CSS, and images served from the nearest edge location have near-zero "
            "latency and do not require an origin round-trip for cache hits. CloudFront with "
            "TTL=0 (option A) can forward dynamic requests but traffic still traverses the "
            "public internet between the client and the CloudFront PoP edge before entering "
            "the AWS backbone; Global Accelerator's anycast routing achieves edge ingress at "
            "the first PoP and routes the full client-to-ALB path over the AWS backbone. "
            "Route 53 latency routing directs DNS resolution but does not change how traffic "
            "travels across the internet. Direct Connect is a site-to-site physical circuit, "
            "not a solution for global end-user devices."
        ),
        "tags": [
            "Edge networking services with appropriate use cases (for example, Amazon CloudFront, AWS Global Accelerator)",
            "Determining the appropriate placement of resources to meet business requirements",
            "Determining high-performing and/or scalable network architectures",
            "Amazon CloudFront",
            "AWS Global Accelerator",
        ],
    },

    # ── Q9: MAMCQ – VPC Gateway vs Interface Endpoints ────────────────────────
    {
        "id": qid("VPC Gateway Endpoint S3 free Interface Endpoint Kinesis PrivateLink mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A company's private EC2 instances in a VPC without internet access must: "
            "(1) access Amazon S3 without any per-GB data processing charges or hourly "
            "endpoint charges, and (2) access Amazon Kinesis Data Streams using the private "
            "DNS name (kinesis.us-east-1.amazonaws.com) resolving to a private IP inside "
            "the VPC. Which TWO VPC endpoint configurations are required? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "S3 Gateway VPC Endpoint — add the endpoint route to private subnet route tables; S3 traffic routes over the AWS private network with no hourly charge and no data processing charge; the endpoint requires no security group",
            "B": "S3 Interface Endpoint (powered by AWS PrivateLink) — creates a private IP in the VPC subnet for S3 access; incurs hourly charges per AZ and per-GB data processing charges",
            "C": "Kinesis Data Streams Interface Endpoint — creates a private ENI in the subnet with a security group allowing HTTPS from EC2 instances; enables private DNS so the standard Kinesis endpoint hostname resolves to the private IP",
            "D": "Kinesis Data Streams Gateway Endpoint — configured in the VPC route table using the same pattern as S3 and DynamoDB Gateway Endpoints, with no hourly or per-GB charge",
            "E": "Configure a custom DNS resolver in the VPC that forwards kinesis.us-east-1.amazonaws.com queries to a NAT Gateway, enabling private resolution without an Interface Endpoint",
        },
        "explanation": (
            "Gateway VPC Endpoints exist only for Amazon S3 and Amazon DynamoDB: they add "
            "a route to the VPC route table directing traffic to the service over AWS's "
            "private network with zero hourly or data-processing charges — the most cost-"
            "effective option for S3 access from private subnets. Kinesis Data Streams does "
            "NOT have a Gateway Endpoint; it uses Interface Endpoints powered by PrivateLink. "
            "A Kinesis Interface Endpoint creates a private ENI in the subnet with its own "
            "private IP; when private DNS is enabled, the standard Kinesis hostname resolves "
            "to the private IP — existing application code needs no changes. Interface "
            "Endpoints incur hourly charges per AZ and per-GB processing charges. "
            "Using a NAT Gateway for DNS forwarding does not create a private endpoint and "
            "still routes traffic through NAT, incurring data processing charges."
        ),
        "tags": [
            "Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways)",
            "Reviewing existing workloads for network optimizations",
            "Configuring appropriate network routes to minimize network transfer costs (for example, Region to Region, Availability Zone to Availability Zone, private to public, AWS Global Accelerator, VPC endpoints)",
            "AWS PrivateLink",
        ],
    },

    # ── Q10: MATCH – Backup Strategies per Service ───────────────────────────
    {
        "id": qid("AWS Backup RDS Automated DLM S3 Versioning backup per service match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "4.1",
        "stem": (
            "A solutions architect must select the correct AWS service to meet each backup "
            "requirement. Match each requirement to the MOST appropriate backup mechanism. "
            "Each mechanism is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Backup with a centralised backup plan",
            "B": "Amazon RDS Automated Backups",
            "C": "Amazon EBS Data Lifecycle Manager (DLM)",
            "D": "Amazon S3 Versioning with lifecycle transitions",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A compliance officer needs point-in-time recovery for an RDS PostgreSQL "
                    "database to any specific second within the last 35 days, including "
                    "restoration of individual transactions using transaction log replay."
                ),
                "correct": "B",
            },
            {
                "id": "sq2",
                "prompt": (
                    "An operations team must snapshot the EBS volumes attached to production "
                    "EC2 instances every 6 hours, retain 7 daily snapshots, retain 4 weekly "
                    "snapshots, and copy the weekly snapshots to a DR Region — all without "
                    "writing Lambda code or running cron jobs."
                ),
                "correct": "C",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A development team's S3 bucket stores application configuration files "
                    "that change frequently. Every version of every configuration file must "
                    "be preserved indefinitely so any prior version can be restored on demand."
                ),
                "correct": "D",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A platform team must enforce a consistent backup policy (daily with "
                    "30-day retention; monthly with 7-year retention) across EC2 EBS, RDS, "
                    "EFS, DynamoDB, and Aurora across 20 AWS accounts with a single policy."
                ),
                "correct": "A",
            },
        ],
        "explanation": (
            "RDS Automated Backups enable point-in-time recovery (PITR) to any second within "
            "the retention window (up to 35 days) by combining daily snapshots with "
            "continuous transaction log shipping — the only RDS feature that supports "
            "second-level PITR. Amazon EBS Data Lifecycle Manager (DLM) automates EBS "
            "snapshot creation, retention, and cross-Region copy using policy-based schedules "
            "without any custom code. S3 Versioning preserves every version of every object "
            "in a bucket; enabling it and adding lifecycle rules to transition or expire "
            "non-current versions provides long-term version retention. AWS Backup provides "
            "a single control plane for multi-service, multi-account backup management with "
            "Organisation-wide policy deployment."
        ),
        "tags": [
            "Designing appropriate backup and retention policies (for example, snapshot frequency)",
            "Selecting the appropriate backup and/or archival solution",
            "Implementing data backups and replications",
            "AWS Backup",
            "Amazon EBS",
            "Amazon S3",
        ],
    },

    # ── Q11: MATCH – Workflow Orchestration Patterns ──────────────────────────
    {
        "id": qid("Step Functions Standard Express EventBridge Scheduler SQS Lambda workflow match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A solutions architect is selecting orchestration and scheduling mechanisms for "
            "four serverless workloads. Match each workload pattern to the MOST appropriate "
            "AWS service. Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Step Functions Standard Workflows",
            "B": "AWS Step Functions Express Workflows",
            "C": "Amazon EventBridge Scheduler",
            "D": "Amazon SQS with Lambda event source mapping (DLQ enabled)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A financial settlement job executes a 15-step workflow spanning multiple "
                    "AWS services. Each run can take up to 8 hours. Failed steps must pause "
                    "and await human approval before retrying. Every state transition must "
                    "be logged for audit and exactly-once execution is required."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A real-time IoT telemetry pipeline orchestrates 2 million lightweight "
                    "micro-workflows per second, each completing in under 5 seconds. Cost "
                    "per state transition is the primary concern; execution history is "
                    "not required after completion."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A weekly compliance report must be triggered at 6 AM UTC every Monday "
                    "to invoke a Lambda function that aggregates audit data from S3 and "
                    "emails a PDF to executives — with no application server to host a "
                    "scheduler."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "An image processing service receives JPEGs via SQS. A Lambda function "
                    "resizes and watermarks each image, writing output to S3. If processing "
                    "fails, the message must retry 3 times before moving to a dead-letter "
                    "queue for investigation — with no orchestration state to manage."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "Step Functions Standard Workflows provide exactly-once execution semantics, "
            "full audit history in the console, duration up to 1 year, human task tokens for "
            "manual approval steps, and state persistence across failures — essential for "
            "compliance-sensitive, long-running financial workflows. Express Workflows are "
            "optimised for high-throughput, short-duration workflows (up to 5 minutes): "
            "they use at-least-once semantics, have no built-in execution history storage, "
            "and are priced per request + duration — far cheaper for millions of micro-"
            "orchestrations per second. EventBridge Scheduler is a serverless cron and "
            "one-time scheduler that invokes Lambda, SQS, Step Functions, or 200+ AWS API "
            "targets on a schedule without managing EC2 or containers. SQS with Lambda "
            "event source mapping provides a managed polling mechanism with configurable "
            "batch size, concurrency limits, retry count, and built-in DLQ support — ideal "
            "for simple queue-driven, stateless processing."
        ),
        "tags": [
            "Workflow orchestration (for example, AWS Step Functions)",
            "Serverless technologies and patterns (for example, AWS Lambda, Fargate)",
            "Queuing and messaging concepts (for example, publish/subscribe)",
        ],
    },

    # ── Q12: MAMCQ – EC2 Placement Groups ─────────────────────────────────────
    {
        "id": qid("Cluster Partition Placement Group HPC fault tolerant large fleet mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.2",
        "stem": (
            "A solutions architect must select EC2 placement strategies for two workloads: "
            "(1) an MPI-based weather simulation requiring the lowest possible network latency "
            "and highest bisection bandwidth between 64 EC2 P4d instances in a single "
            "Availability Zone — instances must be physically co-located, and (2) a fault-"
            "tolerant Hadoop cluster with 300 nodes where a single hardware rack failure "
            "must not take down more than ~10% of the cluster. Which TWO Placement Group "
            "strategies should the architect use for these two workloads respectively? "
            "(Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Cluster Placement Group for the HPC simulation — places all 64 instances on the same high-bandwidth network segment (and often the same physical rack), enabling 10/25/100 Gbps enhanced networking with the lowest inter-node latency",
            "B": "Spread Placement Group for the HPC simulation — distributes instances across distinct underlying hardware to maximize network path diversity between nodes",
            "C": "Partition Placement Group for the Hadoop cluster — divides 300 instances across logical partitions (each backed by independent rack infrastructure), so a rack failure only affects instances within one partition",
            "D": "Cluster Placement Group for the Hadoop cluster — places all 300 nodes on the same physical infrastructure for maximum intra-cluster bandwidth",
            "E": "Spread Placement Group for the Hadoop cluster — guarantees each instance is on a completely separate rack; supports up to 7 instances per AZ per group",
        },
        "explanation": (
            "Cluster Placement Groups co-locate instances within the same Availability Zone "
            "on a low-latency, high-bandwidth network segment (10/25/100 Gbps enhanced "
            "networking where supported) — the correct choice for tightly-coupled HPC and "
            "MPI workloads that require inter-node bandwidth and latency equivalent to a "
            "physical supercomputer rack. Partition Placement Groups divide instances into "
            "user-specified partitions (2–7 per AZ) where each partition's hardware (racks, "
            "switches, power) is isolated from other partitions; a rack failure in one "
            "partition does not affect others, limiting blast radius for large distributed "
            "workloads like Hadoop or Cassandra. Spread Placement Groups are limited to 7 "
            "instances per AZ per group — far too few for a 300-node Hadoop cluster. "
            "Placing a Hadoop cluster in a Cluster Placement Group concentrates all nodes "
            "on shared rack infrastructure, making a single hardware failure catastrophic."
        ),
        "tags": [
            "Determining appropriate scaling methods and strategies for elastic workloads (for example, horizontal compared with vertical, EC2 hibernation)",
            "Sizes and speeds needed to meet business requirements",
            "Amazon EC2",
        ],
    },

    # ── Q13: MAMCQ – DynamoDB On-Demand + DAX ────────────────────────────────
    {
        "id": qid("DynamoDB On-Demand DAX leaderboard spike cache RCU cost mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.3",
        "stem": (
            "A gaming platform uses Amazon DynamoDB Provisioned capacity for its leaderboard. "
            "During tournaments (unpredictable timing), read traffic spikes 200× within "
            "seconds — the current provisioned capacity causes ProvisionedThroughputExceeded "
            "errors. Traffic analysis shows 95% of reads request the same top-20 leaderboard "
            "entries. Between tournaments traffic is very low. Which TWO changes minimise "
            "throttling AND reduce DynamoDB read cost? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Switch DynamoDB from Provisioned to On-Demand capacity mode — the table scales instantly to handle 200× traffic spikes without pre-provisioning, eliminating ProvisionedThroughputExceeded errors",
            "B": "Enable DynamoDB Auto Scaling on Provisioned capacity with a target utilization of 70% and a maximum of 200× baseline — Auto Scaling adjusts capacity in response to sustained load",
            "C": "Deploy Amazon DynamoDB Accelerator (DAX) in front of the DynamoDB table — the 95% repeated top-20 leaderboard reads become DAX cache hits (microsecond latency, zero DynamoDB RCU consumption), dramatically reducing DynamoDB read cost",
            "D": "Enable DynamoDB Streams and replicate the top-20 leaderboard to an ElastiCache for Redis sorted set — application code reads the leaderboard from Redis instead of DynamoDB during tournaments",
            "E": "Increase DynamoDB item size by consolidating all 20 leaderboard entries into a single large item to reduce the read request count and stay within provisioned limits",
        },
        "explanation": (
            "DynamoDB On-Demand capacity mode scales immediately to accommodate any traffic "
            "level without pre-provisioning — it handles sudden spikes without throttling, "
            "paying per request rather than for reserved capacity; ideal for unpredictable "
            "burst patterns where over-provisioning provisioned RCUs is wasteful between "
            "tournaments. DAX is a fully managed DynamoDB-compatible in-memory cache with "
            "microsecond read latency: cache hits consume zero DynamoDB RCUs, so when 95% "
            "of reads hit the same 20 items, the RCU cost drops by 95% and latency reaches "
            "microseconds. DynamoDB Auto Scaling responds to sustained CloudWatch metric "
            "alarms over 1–2 minute windows — too slow to prevent throttling during an "
            "instantaneous 200× spike. DynamoDB Streams + ElastiCache works but requires "
            "significant application code changes; DAX requires no code changes. Consolidating "
            "items increases item size and potentially write costs without solving the "
            "fundamental capacity limitation."
        ),
        "tags": [
            "Caching strategies and services (for example, Amazon ElastiCache)",
            "Database capacity planning (for example, capacity units, instance types, Provisioned IOPS)",
            "Determining an appropriate database type (for example, Amazon Aurora, Amazon DynamoDB)",
            "Amazon DynamoDB",
        ],
    },

    # ── Q14: MAMCQ – S3 Multipart + Transfer Acceleration ────────────────────
    {
        "id": qid("S3 Multipart Upload Transfer Acceleration large files distributed locations mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A genomics company receives 200 GB compressed dataset files from partner labs "
            "in Japan, Germany, and Brazil. Current uploads to an S3 bucket in us-east-1 "
            "take 6+ hours and frequently fail mid-transfer due to transient internet "
            "outages, requiring full retransmission. The company needs faster and more "
            "reliable uploads without changing the S3 bucket Region. Which TWO S3 "
            "capabilities should be enabled? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon S3 Multipart Upload — the SDK splits each 200 GB file into parallel parts; if a part fails only that part retransmits; all parts upload concurrently, maximising available bandwidth",
            "B": "Amazon S3 Versioning — preserves multiple versions of each file so a failed overwrite can be recovered from the previous version without restarting the upload",
            "C": "Amazon S3 Transfer Acceleration — routes upload traffic from labs in Japan, Germany, and Brazil through the nearest CloudFront edge location onto AWS's optimised backbone, significantly reducing upload latency from distant locations",
            "D": "Amazon S3 Intelligent-Tiering — automatically moves uploaded objects between storage classes based on access patterns, optimising storage cost after the file is uploaded",
            "E": "S3 Requester Pays — requires the labs (requesters) to pay for data transfer costs, redistributing upload cost away from the company's AWS account",
        },
        "explanation": (
            "S3 Multipart Upload is recommended for objects larger than 100 MB and required "
            "for objects over 5 GB: it splits the file into independently-uploadable parts "
            "(minimum 5 MB each), uploads them in parallel to maximise throughput, and only "
            "retransmits failed parts on retry — solving the reliability problem without "
            "restarting from scratch. S3 Transfer Acceleration routes upload traffic from "
            "the partner labs through the nearest CloudFront Point of Presence and then onto "
            "AWS's global backbone network, bypassing the congested public internet for the "
            "majority of the path — typically reducing upload time by 50–500% from distant "
            "locations like Asia, Europe, and South America. Versioning preserves object "
            "versions after upload but does not improve upload speed or reliability. "
            "Intelligent-Tiering operates post-upload to optimise storage cost, not upload "
            "performance. Requester Pays shifts billing but does not change network performance."
        ),
        "tags": [
            "Designing appropriate storage strategies (for example, batch uploads to Amazon S3 compared with individual uploads)",
            "Sizes and speeds needed to meet business requirements",
            "Amazon S3",
        ],
    },

    # ── Q15: MATCH – Network Topology by Scale ───────────────────────────────
    {
        "id": qid("VPC Peering Transit Gateway PrivateLink network topology scale match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.4",
        "stem": (
            "A solutions architect must design private connectivity for three different "
            "organisational scales. Match each connectivity scenario to the MOST appropriate "
            "AWS networking service. Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "VPC Peering",
            "B": "AWS Transit Gateway",
            "C": "AWS PrivateLink",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A startup has 3 VPCs in the same Region. All three must communicate "
                    "privately with each other. CIDR blocks do not overlap. No centralised "
                    "inspection or routing is needed, and the company expects no more than "
                    "5 VPCs total."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "An enterprise has 400 VPCs across 30 AWS accounts and needs any-to-any "
                    "routing with centralised routing tables, multi-Region inter-VPC "
                    "connectivity, and the ability to attach new VPCs without creating a "
                    "full mesh of peering connections."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A SaaS provider hosts an analytics API in their VPC and wants to sell "
                    "private access to 10,000 enterprise customers in different AWS accounts "
                    "without peering their VPCs, advertising CIDR routes, or exposing the "
                    "API to the public internet."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "VPC Peering creates a direct private connection between two VPCs with no "
            "bandwidth bottlenecks; for 3 VPCs requiring any-to-any connectivity, 3 peering "
            "connections are needed — manageable at small scale. VPC Peering does NOT support "
            "transitive routing, so it does not scale to hundreds of VPCs. Transit Gateway "
            "is a hub-and-spoke network transit service that scales to thousands of VPC "
            "attachments with centralised routing, inter-Region peering, and support for "
            "on-premises connections — eliminating the O(n²) peering mesh problem. "
            "PrivateLink exposes specific services via Network Load Balancer-backed "
            "endpoints: consumers access the service through an Interface VPC Endpoint "
            "without needing peering, route tables, or CIDR management — ideal for "
            "multi-tenant SaaS service exposure at massive scale."
        ),
        "tags": [
            "Network routing, topology, and peering (for example, AWS Transit Gateway, VPC peering)",
            "Determining network configurations that can scale to accommodate future needs",
            "Reviewing existing workloads for network optimizations",
        ],
    },

    # ── Q16: MAMCQ – S3 Gateway Endpoint + SSM Session Manager ───────────────
    {
        "id": qid("S3 Gateway Endpoint SSM Session Manager network cost bastion host mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "4.4",
        "stem": (
            "A solutions architect reviews a $20,000/month AWS networking bill and identifies "
            "two cost drivers: (1) EC2 instances in private subnets route all S3 traffic "
            "through a NAT Gateway, generating $0.045/GB data processing charges on terabytes "
            "of daily S3 access, and (2) a public-facing EC2 bastion host in a public subnet "
            "incurs EC2 hourly charges and internet data transfer costs for SSH sessions. "
            "Which TWO changes eliminate MOST of the excess cost? (Select TWO.)"
        ),
        "correct": ["A", "D"],
        "difficulty": "HARD",
        "answers": {
            "A": "Create an S3 Gateway VPC Endpoint and add the endpoint route to all private subnet route tables — S3 traffic bypasses the NAT Gateway entirely, routing over AWS's free internal network with zero data-processing charge",
            "B": "Replace the NAT Gateway with a self-managed NAT instance (EC2 t3.medium) — reduces hourly NAT costs but still incurs per-GB data processing charges for all traffic including S3",
            "C": "Enable Amazon S3 Intelligent-Tiering on all buckets so the smaller footprint of accessed data reduces the volume of S3 API calls routed through the NAT Gateway",
            "D": "Terminate the bastion host EC2 instance and use AWS Systems Manager Session Manager for shell access to private EC2 instances — SSM Session Manager requires no inbound internet ports, no bastion host, and incurs no additional EC2 or data transfer charges",
            "E": "Migrate all EC2 workloads to AWS Lambda functions to eliminate the need for NAT Gateway routing to S3; Lambda functions in a VPC can use Gateway Endpoints, and functions outside a VPC access S3 natively",
        },
        "explanation": (
            "S3 Gateway VPC Endpoints are free (no hourly charge, no per-GB processing "
            "charge) and route S3 API traffic entirely within AWS's internal network, "
            "bypassing the NAT Gateway completely — for terabytes of daily S3 access, this "
            "can eliminate thousands of dollars per month in NAT processing charges. AWS "
            "Systems Manager Session Manager provides browser-based or CLI shell access to "
            "EC2 instances (including private instances) using the SSM agent and IAM "
            "authentication — no bastion host, no open inbound SSH port (port 22), no "
            "internet-facing EC2 instance, and no additional hourly EC2 cost. NAT instances "
            "reduce hourly compute cost but retain per-GB data processing fees. Intelligent-"
            "Tiering changes the storage class but not the number of S3 API calls or NAT "
            "data processing charges. Migrating to Lambda is a major re-architecture and "
            "does not directly solve the immediate cost problem."
        ),
        "tags": [
            "Reviewing existing workloads for network optimizations",
            "Configuring appropriate network routes to minimize network transfer costs (for example, Region to Region, Availability Zone to Availability Zone, private to public, AWS Global Accelerator, VPC endpoints)",
            "NAT gateways (for example, NAT instance costs compared with NAT gateway costs)",
            "AWS Systems Manager",
        ],
    },

    # ── Q17: MATCH – Edge Deployment Options ──────────────────────────────────
    {
        "id": qid("Outposts Local Zones Wavelength edge deployment on-premises match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.4",
        "stem": (
            "A solutions architect must recommend the appropriate AWS infrastructure extension "
            "for three different edge deployment requirements. Match each requirement to the "
            "MOST appropriate AWS service. Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Outposts",
            "B": "AWS Local Zones",
            "C": "AWS Wavelength",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A manufacturing plant runs real-time robotics control systems that require "
                    "sub-millisecond round-trip latency and must process sensitive sensor data "
                    "on-premises due to data sovereignty regulations that prohibit sending raw "
                    "telemetry to a public cloud Region."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A media production company in Los Angeles needs GPU-accelerated EC2 "
                    "instances (g4dn) for real-time 4K video rendering workflows. The company "
                    "wants cloud-managed infrastructure within single-digit milliseconds of "
                    "its LA studio without deploying on-premises hardware."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A mobile game publisher needs to serve sub-10ms game state updates to "
                    "players using 5G smartphones. The compute must run at the mobile network "
                    "operator's infrastructure edge to take advantage of 5G ultra-low latency "
                    "without data traversing the operator's core network."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "AWS Outposts deploys fully managed AWS rack hardware (compute, storage, "
            "networking) on the customer's premises, providing the same AWS APIs and services "
            "locally — enabling low-latency on-premises workloads and data-residency "
            "compliance without sending data to a public Region. AWS Local Zones are "
            "extensions of AWS Regions to specific metropolitan areas (Los Angeles, Chicago, "
            "Miami, etc.), offering a subset of AWS services (EC2, EBS, ECS, EKS, RDS) with "
            "single-digit millisecond latency to local users without on-premises hardware. "
            "AWS Wavelength embeds AWS compute and storage inside 5G telecommunications "
            "carriers' edge infrastructure (Verizon, SK Telecom, Vodafone), enabling "
            "applications to be reached directly from 5G devices without traffic traversing "
            "the operator's core network — achieving ultra-low latency for 5G use cases."
        ),
        "tags": [
            "Hybrid compute options (for example, AWS Outposts)",
            "Distributed computing concepts supported by AWS global infrastructure and edge services",
            "Determining the appropriate placement of resources to meet business requirements",
        ],
    },

    # ── Q18: MAMCQ – Data Access Policy + SSE-C ──────────────────────────────
    {
        "id": qid("SSE-C customer provided keys S3 bucket policy data access protection mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.3",
        "stem": (
            "A healthcare company stores PHI (Protected Health Information) in Amazon S3. "
            "The CISO mandates: (1) all objects must be encrypted with keys whose material "
            "is generated, stored, and controlled entirely outside AWS — AWS must never "
            "have access to or store the key material, and (2) any PutObject request that "
            "does NOT include the customer's key material must be automatically rejected "
            "by S3 before the object is written. Which TWO configurations enforce both "
            "requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Use S3 Server-Side Encryption with Customer-Provided Keys (SSE-C) — the application provides the 256-bit AES key in every PUT request header; S3 encrypts the object, discards the key immediately, and never stores it; the same key must be provided on every GET request",
            "B": "Enable S3 default encryption with SSE-KMS using a customer managed KMS key (CMK) — the customer controls the key policy in AWS KMS; AWS KMS stores and manages the key material in its own FIPS 140-2 Level 2 HSMs",
            "C": "Add an S3 bucket policy with a Deny statement on s3:PutObject for all requests where the condition key 's3:x-amz-server-side-encryption' is absent or does not equal 'aws:sse-c', rejecting any upload that does not include SSE-C encryption headers",
            "D": "Enable Amazon Macie on the S3 bucket to detect unencrypted PHI objects and trigger a Lambda function to re-encrypt them with the company's key material after upload",
            "E": "Configure an AWS Config managed rule (s3-bucket-server-side-encryption-enabled) and automatic remediation to call a Lambda function that re-encrypts non-compliant objects within 1 hour of upload",
        },
        "explanation": (
            "SSE-C (Server-Side Encryption with Customer-Provided Keys) is the only S3 "
            "encryption mode where the customer generates and retains the key material outside "
            "of AWS: the encryption key bytes are sent in the request header, used by S3 to "
            "encrypt/decrypt the object, and then immediately discarded — AWS never stores "
            "the key. An S3 bucket policy Deny on s3:PutObject with a condition on the "
            "encryption header enforces SSE-C at the API level: requests without the "
            "required SSE-C header are rejected before S3 writes any data, satisfying "
            "requirement 2 proactively. SSE-KMS with a CMK (option B) stores the key "
            "material in AWS KMS's HSMs — AWS manages the key infrastructure; the customer "
            "controls the key policy but does not retain key material outside AWS. Macie and "
            "Config + Lambda remediation detect and fix after upload — they cannot prevent "
            "the initial unencrypted write that requirement 2 prohibits."
        ),
        "tags": [
            "Implementing policies for data access, lifecycle, and protection",
            "Encryption and appropriate key management",
            "Data access and governance",
            "Amazon S3",
            "AWS KMS",
        ],
    },

    # ── Q19: MAMCQ – Hybrid Storage DR (Volume Gateway + Transfer Family) ──────
    {
        "id": qid("Volume Gateway Cached iSCSI Transfer Family SFTP hybrid storage DR mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.1",
        "stem": (
            "A company's primary workloads run on-premises. It needs AWS as a disaster "
            "recovery target with two requirements: (1) on-premises servers must access block "
            "storage volumes via iSCSI with locally cached hot data, while all primary data "
            "is durably stored as EBS snapshots in AWS for recovery, and (2) the company's "
            "SFTP-based file exchange with external partners must be migrated to a managed "
            "cloud service without requiring any partner-side SFTP client reconfiguration. "
            "Which TWO services satisfy BOTH requirements? (Select TWO.)"
        ),
        "correct": ["A", "D"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Storage Gateway — Volume Gateway in Cached mode: presents iSCSI block volumes to on-premises servers with frequently accessed data cached locally; all volume data is stored durably as EBS snapshots in AWS for recovery",
            "B": "AWS Storage Gateway — File Gateway: presents NFS and SMB file shares to on-premises workstations, backed by Amazon S3 objects — provides file access, not iSCSI block volumes",
            "C": "AWS DataSync: transfers on-premises NFS/SMB file data to Amazon EFS or S3 on a schedule for DR; does not provide on-premises iSCSI block storage access",
            "D": "AWS Transfer Family with an SFTP-enabled endpoint in Amazon S3: external partners connect to the same SFTP hostname and credentials as before; the endpoint is now managed by AWS and stores files directly in S3",
            "E": "Amazon S3 Glacier with a direct SFTP interface: archives all on-premises data in Glacier with SFTP upload support, providing lowest-cost DR storage with SFTP compatibility",
        },
        "explanation": (
            "AWS Storage Gateway Volume Gateway (Cached mode) is the exact fit for "
            "requirement 1: it presents standard iSCSI volumes to on-premises servers, "
            "caches frequently accessed data locally for low-latency reads, and stores all "
            "volume data as EBS snapshots in AWS — enabling EC2-based recovery from any "
            "snapshot on a DR event. AWS Transfer Family with SFTP support is the exact "
            "fit for requirement 2: it provides a managed SFTP endpoint that maps to S3 "
            "or EFS buckets; existing partners connect to the same endpoint using their "
            "existing SFTP clients and credentials — no partner-side reconfiguration. "
            "File Gateway provides NFS/SMB shares (not iSCSI block volumes). DataSync is "
            "for migration and one-way file transfer, not ongoing block volume access. "
            "Amazon S3 Glacier has no native SFTP interface."
        ),
        "tags": [
            "Hybrid storage options (for example, AWS DataSync, AWS Transfer Family, AWS Storage Gateway)",
            "Implementing data backups and replications",
            "Selecting the appropriate backup and/or archival solution",
            "AWS Storage Gateway",
            "AWS Transfer Family",
        ],
    },

    # ── Q20: MAMCQ – Amazon MSK Kafka Compatibility ───────────────────────────
    {
        "id": qid("Amazon MSK Kafka protocol exactly-once Kinesis comparison mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A company runs a real-time event streaming platform using self-managed Apache "
            "Kafka on EC2. They want to migrate to a managed AWS streaming service that: "
            "(1) allows existing Kafka producer and consumer applications to connect with "
            "NO code changes, and (2) supports the Kafka Transactions API for exactly-once "
            "semantics in their stream-processing consumers. Which TWO statements correctly "
            "explain why Amazon MSK satisfies these requirements compared to Amazon Kinesis "
            "Data Streams? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon MSK is Apache Kafka — it runs fully managed Kafka brokers; existing Kafka clients (Java, Python, Go) using the Kafka protocol connect to MSK clusters using the same producer and consumer APIs with no code changes",
            "B": "Amazon MSK automatically translates incoming Kafka protocol messages into Kinesis Data Streams shard format, enabling Kafka applications to target MSK while benefiting from Kinesis's management plane",
            "C": "Amazon MSK supports the full Apache Kafka Transactions API: producers can begin, commit, and abort transactions; consumers using isolation.level=read_committed consume only committed records, enabling exactly-once stream processing",
            "D": "Amazon Kinesis Data Streams supports the Kafka producer/consumer wire protocol so existing Kafka applications can target Kinesis endpoints without any code changes, similar to how MSK works",
            "E": "Amazon MSK Serverless provides built-in exactly-once delivery by deduplicating messages using SHA-256 checksums at the broker level, without requiring Kafka Transactions API configuration in consumer code",
        },
        "explanation": (
            "Amazon MSK (Managed Streaming for Apache Kafka) is a fully managed service "
            "running actual Apache Kafka: the same Kafka client libraries, topic/partition "
            "abstractions, consumer group protocol, and all Kafka APIs work unchanged against "
            "an MSK cluster — existing applications require zero code modifications. MSK "
            "supports the complete Kafka Transactions API (beginTransaction, "
            "commitTransaction, abortTransaction) and idempotent producers, enabling "
            "exactly-once semantics for read-process-write Kafka Streams and consumer "
            "applications using isolation.level=read_committed. Amazon Kinesis Data Streams "
            "does NOT implement the Kafka protocol — Kafka clients cannot connect to Kinesis "
            "without code changes; Kinesis uses its own shard/sequence-number model and "
            "AWS SDK APIs. MSK does not translate Kafka to Kinesis. MSK Serverless does "
            "not use SHA-256 message deduplication; exactly-once delivery is achieved "
            "through the standard Kafka Transactions API."
        ),
        "tags": [
            "Selecting appropriate configurations for ingestion",
            "Amazon Managed Streaming for Apache Kafka (Amazon MSK)",
            "Designing data streaming architectures",
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
