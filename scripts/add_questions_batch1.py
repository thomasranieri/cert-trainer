#!/usr/bin/env python3
"""Batch 1: 20 MATCH/MAMCQ questions for SAA-C03."""
import json, hashlib, sys, os

EXAM = "AWS Certified Solutions Architect - Associate (SAA-C03)"

def qid(stem):
    return hashlib.sha256((EXAM + stem).encode()).hexdigest()

new_questions = [
    # ── Q1: MATCH – VPC Security Components ──────────────────────────────────
    {
        "id": qid("VPC security components SG NACL RouteTable match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A solutions architect is auditing a three-tier VPC design. "
            "Match each behavioral statement to the VPC security component it BEST describes. "
            "Each component is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Security Group",
            "B": "Network ACL (NACL)",
            "C": "Route Table",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "Operates at the subnet boundary, evaluates rules in ascending numeric order "
                    "(first match applies), and supports explicit DENY rules — enabling a blanket "
                    "block of a specific IP range before any ALLOW rule can match it."
                ),
                "correct": "B",
            },
            {
                "id": "sq2",
                "prompt": (
                    "Is stateful: once an inbound connection passes the inbound rule, all "
                    "corresponding return traffic is automatically allowed without requiring a "
                    "matching outbound rule."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "Associates destination CIDR blocks with specific targets (internet gateway, "
                    "NAT gateway, transit gateway attachment) and determines how packets exiting "
                    "a subnet are forwarded toward their destination."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "Rules are evaluated simultaneously (no ordering), only ALLOW rules exist, "
                    "and another instance of the same resource type can be cited as a "
                    "source/destination — enabling dynamic group-based access within a VPC."
                ),
                "correct": "A",
            },
        ],
        "explanation": (
            "NACLs are stateless and subnet-level: numbered rules are evaluated in order; the "
            "first match wins; both ALLOW and DENY are supported — making them the right tool "
            "for explicit IP-range blocks. Security Groups are stateful and ENI-level: they track "
            "connection state so return traffic is implicitly allowed; rules are evaluated "
            "simultaneously (all rules, not first-match); only ALLOW is supported; and other "
            "security group IDs can be used as sources/destinations. Route Tables control packet "
            "forwarding out of a subnet by mapping destination CIDRs to gateway targets."
        ),
        "tags": [
            "Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways)",
            "Basic networking concepts (for example, route tables)",
            "Amazon VPC",
        ],
    },

    # ── Q2: MAMCQ – Direct Connect + DX Gateway ──────────────────────────────
    {
        "id": qid("Direct Connect Gateway multi-VPC multi-Region 10Gbps mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "An enterprise must establish a private 10 Gbps connection from its on-premises "
            "data center to six Amazon VPCs spread across three AWS Regions. The connection "
            "must never traverse the public internet, and ALL six VPCs must be reachable over "
            "a SINGLE physical AWS port simultaneously. Which TWO services are REQUIRED to "
            "satisfy these requirements? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Direct Connect with a dedicated connection (10 Gbps port speed)",
            "B": "AWS Site-to-Site VPN with BGP routing configured on a Virtual Private Gateway",
            "C": "AWS Direct Connect Gateway associated with a Virtual Private Gateway in each target VPC",
            "D": "AWS Transit Gateway deployed in each Region with an SD-WAN attachment for on-premises routing",
            "E": "AWS PrivateLink endpoint services created in each VPC for private IP access",
        },
        "explanation": (
            "A Direct Connect dedicated connection (1, 10, or 100 Gbps) provides the private "
            "physical circuit between on-premises and AWS without traversing the internet. "
            "A Direct Connect Gateway enables a single Direct Connect connection to reach VPCs "
            "in multiple AWS Regions simultaneously through their associated Virtual Private "
            "Gateways — eliminating the need for separate connections per Region. "
            "Site-to-Site VPN travels over the public internet and offers at most 1.25 Gbps per "
            "tunnel. PrivateLink exposes specific services, not general VPC connectivity. "
            "Transit Gateway adds flexibility but is not strictly required to meet the stated "
            "requirements and adds cost."
        ),
        "tags": [
            "Securing external network connections to and from the AWS Cloud (for example, VPN, AWS Direct Connect)",
            "Determining network configurations that can scale to accommodate future needs",
            "Selecting the appropriate bandwidth allocation for a network device (for example, a single VPN compared with multiple VPNs, Direct Connect speed)",
            "AWS Direct Connect",
        ],
    },

    # ── Q3: MATCH – EBS Volume Types ─────────────────────────────────────────
    {
        "id": qid("EBS volume types gp3 io2 st1 sc1 workload match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.1",
        "stem": (
            "A solutions architect must select the most cost-effective Amazon EBS volume type "
            "for each workload without sacrificing required performance. "
            "Match each workload to the BEST-FIT EBS volume type. Each type is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "gp3 (General Purpose SSD)",
            "B": "io2 Block Express",
            "C": "st1 (Throughput Optimized HDD)",
            "D": "sc1 (Cold HDD)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A SAP HANA in-memory database requiring 64,000 IOPS, sub-millisecond "
                    "latency, 99.999% durability, and the ability to provision IOPS completely "
                    "independently of volume size up to 256,000 IOPS."
                ),
                "correct": "B",
            },
            {
                "id": "sq2",
                "prompt": (
                    "An application server boot volume (200 GiB) that needs a consistent "
                    "4,000 IOPS baseline. The team wants to set IOPS independently of size "
                    "to avoid over-provisioning while keeping the lowest-cost SSD tier."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A Hadoop cluster performing large sequential reads of multi-hundred-GiB "
                    "log files daily. Throughput of up to 500 MiB/s is needed; random IOPS "
                    "requirements are minimal."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A compliance archive storing 50 TB of audit logs accessed fewer than twice "
                    "per year. The lowest per-GB monthly block-storage cost is the primary "
                    "requirement; retrieval latency is not a concern."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "io2 Block Express supports up to 256,000 IOPS, 4,000 MiB/s throughput, "
            "sub-millisecond latency, and 99.999% durability — the only EBS type suitable for "
            "mission-critical databases like SAP HANA. gp3 lets you configure IOPS (up to "
            "16,000) and throughput independently of volume size, making it cost-effective for "
            "general workloads without gp2's implicit IOPS-per-GiB coupling. st1 is a "
            "Throughput Optimized HDD designed for frequently accessed sequential workloads "
            "(Hadoop, ETL) with up to 500 MiB/s — cost-effective for big sequential reads. "
            "sc1 (Cold HDD) offers the lowest per-GB EBS price and suits infrequently accessed "
            "sequential data where throughput can be as low as 80–250 MiB/s."
        ),
        "tags": [
            "Block storage options (for example, hard disk drive [HDD] volume types, solid state drive [SSD] volume types)",
            "Storage options and characteristics (for example, durability, replication)",
            "Determining the correct storage size for a workload",
            "Amazon EBS",
        ],
    },

    # ── Q4: MAMCQ – Multi-tier Architecture ──────────────────────────────────
    {
        "id": qid("Multi-tier SQS decoupling RDS Multi-AZ architecture mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A company is architecting a three-tier e-commerce application. The web tier must "
            "absorb sudden traffic spikes without dropping requests. The application tier performs "
            "variable-duration order-processing tasks and must scale independently of the web "
            "tier. The database tier must survive an Availability Zone failure with automatic "
            "failover and no data loss. Which TWO design choices BEST address ALL three "
            "requirements? (Select TWO.)"
        ),
        "correct": ["B", "D"],
        "difficulty": "HARD",
        "answers": {
            "A": "Front the web tier with an Application Load Balancer; configure the application tier to poll ALB access logs stored in S3 to determine current load and scale accordingly",
            "B": "Insert Amazon SQS between the web and application tiers so the web tier enqueues order requests and the application tier polls the queue, enabling each tier to scale and fail independently",
            "C": "Deploy the application tier as a single xl instance type to reduce inter-tier networking and eliminate the need for a queue by processing requests faster",
            "D": "Deploy Amazon RDS for MySQL with Multi-AZ enabled; the synchronous standby in a second AZ promotes automatically within 60–120 seconds if the primary fails",
            "E": "Deploy cross-AZ Amazon RDS Read Replicas and configure the application to promote a read replica to primary manually when the primary instance becomes unavailable",
        },
        "explanation": (
            "SQS durably buffers requests between tiers: the web tier enqueues at any rate, "
            "the application tier polls at its own pace, and no requests are dropped during "
            "spikes — this is the canonical AWS loose-coupling pattern for multi-tier "
            "architectures. RDS Multi-AZ uses synchronous replication to a standby replica in "
            "a different AZ; AWS orchestrates automatic failover with no manual intervention, "
            "and the synchronous replication ensures zero data loss. Polling ALB access logs "
            "from S3 introduces unacceptable lag (logs are delivered every 5 minutes). A single "
            "large instance is a single point of failure and cannot scale elastically. Read "
            "Replicas use asynchronous replication (possible data loss) and require manual "
            "promotion — they do not provide automatic failover."
        ),
        "tags": [
            "Multi-tier architectures",
            "Queuing and messaging concepts (for example, publish/subscribe)",
            "Amazon SQS",
            "Database types and services (for example, serverless, relational compared with non-relational, in-memory)",
        ],
    },

    # ── Q5: MATCH – Specialty Database Services ───────────────────────────────
    {
        "id": qid("Neptune Keyspaces DocumentDB DynamoDB specialty database match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.3",
        "stem": (
            "A solutions architect is selecting AWS managed database services for four new "
            "applications. Match each requirement to the MOST appropriate database service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon Neptune",
            "B": "Amazon Keyspaces (for Apache Cassandra)",
            "C": "Amazon DocumentDB (with MongoDB compatibility)",
            "D": "Amazon DynamoDB",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A fraud-detection platform must traverse billions of relationship edges "
                    "between accounts, devices, and IP addresses using graph traversal queries "
                    "(Gremlin/SPARQL) to surface suspicious patterns in milliseconds."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "An IoT fleet platform currently runs Apache Cassandra on-premises with "
                    "wide-column tables and CQL-based queries. The team wants a fully managed "
                    "cloud migration with minimal application code changes."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A product catalog service stores deeply nested JSON documents and requires "
                    "MongoDB-compatible aggregation pipelines, ACID transactions, and flexible "
                    "schema evolution without re-platforming to a new query language."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A mobile gaming leaderboard needs guaranteed single-digit millisecond "
                    "latency at millions of reads per second, a serverless On-Demand capacity "
                    "mode to eliminate capacity planning, and multi-region active-active "
                    "replication via Global Tables."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "Neptune is AWS's managed graph database (Gremlin and SPARQL), optimised for "
            "traversing dense relationship networks — the correct choice for fraud detection "
            "graph queries. Keyspaces is a serverless Cassandra-compatible service: CQL queries "
            "work unchanged, enabling lift-and-shift migrations. DocumentDB provides MongoDB "
            "wire-protocol compatibility with ACID transactions and rich aggregation support — "
            "ideal for MongoDB migrations. DynamoDB delivers guaranteed single-digit millisecond "
            "performance at any scale, a serverless On-Demand mode, and Global Tables for "
            "multi-region active-active replication."
        ),
        "tags": [
            "Database types and services (for example, serverless, relational compared with non-relational, in-memory)",
            "Determining an appropriate database type (for example, Amazon Aurora, Amazon DynamoDB)",
            "Amazon Neptune",
            "Amazon Keyspaces",
            "Amazon DocumentDB",
            "Amazon DynamoDB",
        ],
    },

    # ── Q6: MAMCQ – AWS X-Ray ─────────────────────────────────────────────────
    {
        "id": qid("X-Ray distributed tracing API Gateway Lambda ECS sidecar mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A team is troubleshooting intermittent latency spikes in a distributed application "
            "spanning Amazon API Gateway, AWS Lambda, and containerized microservices on Amazon "
            "ECS. They need end-to-end request traces, service dependency maps, and the ability "
            "to pinpoint which downstream component is responsible for the added latency. Which "
            "TWO actions should the solutions architect take to enable this capability? "
            "(Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Enable X-Ray active tracing on the API Gateway stage and set the Lambda function tracing mode to Active so that X-Ray captures traces for every invocation",
            "B": "Create a CloudWatch dashboard with p99 latency metrics from API Gateway, Lambda, and ECS to identify the slowest service tier in aggregate",
            "C": "Add the X-Ray daemon as a sidecar container in each ECS task definition and instrument the application code with the X-Ray SDK to emit subsegments for each downstream service call",
            "D": "Enable AWS CloudTrail data event logging for Lambda invocations and use Amazon Athena to parse trace IDs from CloudTrail logs and reconstruct call chains",
            "E": "Configure Amazon CloudWatch Contributor Insights on Lambda logs to rank function invocations by duration and correlate high-duration entries across services by request ID",
        },
        "explanation": (
            "Enabling X-Ray active tracing on API Gateway propagates the trace header "
            "downstream; setting Lambda tracing mode to Active records traces for every "
            "invocation automatically. For ECS, the X-Ray daemon must run as a sidecar "
            "container (sharing the task's network namespace on UDP port 2000) to receive "
            "trace segments emitted by the X-Ray SDK in application code — producing the "
            "subsegments and annotations needed for per-request service maps and latency "
            "breakdowns. CloudWatch metrics show aggregate percentiles but not per-request "
            "causality across service boundaries. CloudTrail records API call metadata, not "
            "performance traces. Contributor Insights ranks log entries but cannot stitch "
            "cross-service call chains into a dependency map."
        ),
        "tags": [
            "Workload visibility (for example, AWS X-Ray)",
            "AWS X-Ray",
            "Multi-tier architectures",
        ],
    },

    # ── Q7: MATCH – Disaster Recovery Strategies ──────────────────────────────
    {
        "id": qid("DR strategies backup restore pilot light warm standby active-active match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A business-continuity team must assign a disaster recovery strategy to each "
            "application based on recovery objectives and budget. Match each application profile "
            "to the DR strategy that meets its RTO/RPO at the LOWEST cost. Each strategy is "
            "used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Backup and Restore",
            "B": "Pilot Light",
            "C": "Warm Standby",
            "D": "Multi-site Active-Active",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "An internal reporting tool with an RTO of 48 hours and RPO of 24 hours. "
                    "Nightly database snapshots and AMIs are copied to a secondary Region; no "
                    "infrastructure runs there normally."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A customer-facing REST API with RTO of 4 hours and RPO of 1 hour. The "
                    "production database replicates continuously to a DR Region, but no "
                    "application servers are running there."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "An order-management system with RTO of 15 minutes and RPO of 5 minutes. "
                    "A scaled-down but fully operational environment (25% of production "
                    "capacity) runs continuously in a DR Region and can be rapidly scaled out "
                    "on failover."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A global payment platform with RTO of seconds and RPO of zero. Live "
                    "traffic is distributed across two Regions simultaneously using Route 53 "
                    "latency routing; data is synchronously replicated between Regions."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "Backup and Restore has the highest RTO/RPO tolerance (hours to days) and lowest "
            "cost — infrastructure is recreated entirely from snapshots on failover. Pilot Light "
            "keeps only the most critical core (typically the database) running in the DR "
            "Region; application servers are launched only when needed, achieving an RTO of "
            "hours. Warm Standby runs a fully functional but scaled-down replica continuously, "
            "reducing failover to minutes by scaling out rather than provisioning from scratch. "
            "Multi-site Active-Active distributes production traffic across all Regions "
            "simultaneously, providing near-zero RTO/RPO at the highest cost."
        ),
        "tags": [
            "Disaster recovery (DR) strategies (for example, backup and restore, pilot light, warm standby, active-active failover, recovery point objective [RPO], recovery time objective [RTO])",
            "Determining the required availability for different classes of workloads (for example, production workloads, non-production workloads)",
        ],
    },

    # ── Q8: MAMCQ – KMS Rotation + ACM Renewal ────────────────────────────────
    {
        "id": qid("KMS automatic rotation ACM certificate renewal ALB zero downtime mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.3",
        "stem": (
            "A security team must ensure that the AWS KMS customer managed key (CMK) used for "
            "data encryption and the TLS certificate on an Application Load Balancer are both "
            "rotated automatically with zero service interruption and no manual steps. Which "
            "TWO actions achieve this? (Select TWO.)"
        ),
        "correct": ["B", "D"],
        "difficulty": "HARD",
        "answers": {
            "A": "Export the ACM public certificate and private key, store the key in AWS Secrets Manager with a rotation Lambda, and configure the ALB listener to retrieve the certificate from Secrets Manager on each TLS handshake",
            "B": "Enable automatic key rotation on the CMK; AWS rotates the backing key material annually while preserving the key ID, ARN, and aliases — all existing ciphertexts remain decryptable without re-encryption",
            "C": "Write a scheduled Lambda function that calls the KMS GenerateDataKey API monthly to produce a new data key, stores it in S3, and updates the application configuration with the new key ARN",
            "D": "Use AWS Certificate Manager to request a public TLS certificate, associate it with the ALB HTTPS listener, and rely on ACM's fully managed renewal — ACM renews and redeploys the certificate before expiration without downtime",
            "E": "Use AWS Certificate Manager Private CA to issue a certificate for the public ALB listener so the security team retains full control over the renewal schedule and can rotate on demand",
        },
        "explanation": (
            "KMS automatic rotation rotates the underlying backing key material on a yearly "
            "schedule. The key ID, ARN, and all aliases remain unchanged, so applications need "
            "no configuration updates; KMS tracks which key version encrypted each ciphertext "
            "and uses the correct version for decryption automatically — zero re-encryption "
            "and zero downtime. ACM manages the complete lifecycle of public TLS certificates: "
            "it provisions, deploys to ALB listeners, and renews certificates automatically "
            "60 days before expiration with no service interruption. ACM public certificates "
            "cannot have their private keys exported; the ALB integrates with ACM directly "
            "without Secrets Manager. Generating data keys manually does not rotate the CMK. "
            "Private CA is for internal/private PKI use cases, not public-facing load balancers."
        ),
        "tags": [
            "Rotating encryption keys and renewing certificates",
            "Encrypting data in transit (for example, AWS Certificate Manager [ACM] using TLS)",
            "Implementing data backups and replications",
            "AWS KMS",
            "AWS Certificate Manager (ACM)",
        ],
    },

    # ── Q9: MATCH – Scaling Strategies ────────────────────────────────────────
    {
        "id": qid("Horizontal vertical EC2 hibernation scaling strategies match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.2",
        "stem": (
            "A solutions architect is recommending EC2 scaling strategies for three different "
            "workloads. Match each workload to the MOST appropriate scaling strategy. "
            "Each strategy is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Horizontal scaling (EC2 Auto Scaling group adding or removing instances)",
            "B": "Vertical scaling (moving to a larger EC2 instance type)",
            "C": "EC2 Hibernation",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A stateless web API stores all session state in Amazon ElastiCache and "
                    "experiences 10× traffic spikes on weekday mornings. Cost must be minimised "
                    "during overnight low-traffic periods."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A legacy Oracle database runs on a single EC2 instance with a per-instance "
                    "license. The application cannot be distributed across nodes but is hitting "
                    "CPU and memory ceilings as the dataset grows."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A developer's build server takes 25 minutes to warm up an in-memory "
                    "compilation cache after a cold start. The team stops the instance overnight "
                    "and wants it to resume instantly each morning with all in-memory state "
                    "intact, without a full OS boot."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "Horizontal scaling (Auto Scaling) is ideal for stateless workloads where any "
            "instance can serve any request — session state in ElastiCache means no affinity "
            "is required, so instances can be added or removed freely. Vertical scaling "
            "(instance resize) is the only option for workloads that cannot be distributed — "
            "such as single-node licensed databases — though it requires a stop/start cycle. "
            "EC2 Hibernation saves the full RAM contents to the encrypted EBS root volume on "
            "stop; on restart, memory is restored and the process resumes exactly where it "
            "left off — eliminating cold-start initialisation costs."
        ),
        "tags": [
            "Determining appropriate scaling methods and strategies for elastic workloads (for example, horizontal compared with vertical, EC2 hibernation)",
            "Sizes and speeds needed to meet business requirements",
            "Amazon EC2",
        ],
    },

    # ── Q10: MAMCQ – S3 Lifecycle ─────────────────────────────────────────────
    {
        "id": qid("S3 lifecycle Intelligent-Tiering Glacier Deep Archive HIPAA mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "4.1",
        "stem": (
            "A healthcare company stores patient scan files in Amazon S3. Scans are actively "
            "accessed for the first 30 days, then accessed occasionally and unpredictably "
            "between 31 and 90 days, then rarely after 90 days. After 365 days, files must be "
            "retained for 6 additional years for HIPAA compliance and will never be accessed "
            "in normal operations — though retrieval within 12 hours must be possible when "
            "required. The company wants to minimise S3 costs. Which TWO lifecycle actions "
            "should the architect configure? (Select TWO.)"
        ),
        "correct": ["B", "E"],
        "difficulty": "HARD",
        "answers": {
            "A": "Transition objects to S3 Glacier Instant Retrieval at 30 days to immediately reduce costs for the unpredictable access window",
            "B": "Transition objects to S3 Intelligent-Tiering at 30 days so AWS automatically moves files between Frequent and Infrequent Access tiers based on actual usage patterns",
            "C": "Transition objects to S3 One Zone-IA at 90 days to minimise storage costs while still supporting occasional retrieval",
            "D": "Set an S3 expiration action to delete objects after 365 days to avoid long-term archive costs",
            "E": "Transition objects to S3 Glacier Deep Archive at 365 days, which provides the lowest per-GB storage cost and supports standard retrieval within 12 hours",
        },
        "explanation": (
            "S3 Intelligent-Tiering automatically moves objects between Frequent Access and "
            "Infrequent Access tiers (and optionally Archive tiers) based on access patterns, "
            "making it optimal for the 31–90 day window where access is occasional and "
            "unpredictable — no retrieval fees for monitored tiers. S3 Glacier Deep Archive "
            "($0.00099/GB-month) is the lowest-cost S3 storage class; it supports standard "
            "retrieval in 12 hours, satisfying the compliance retrieval requirement. "
            "Glacier Instant Retrieval has a 90-day minimum storage duration charge and "
            "per-retrieval costs, making it poorly suited to occasional access at 30 days. "
            "S3 One Zone-IA stores data in only one Availability Zone (99.5% availability, "
            "99.999999999% durability on paper but AZ loss risks data), which is inappropriate "
            "for medical records requiring high durability. Expiring objects after 365 days "
            "would violate the 7-year HIPAA retention requirement."
        ),
        "tags": [
            "Designing appropriate storage strategies (for example, batch uploads to Amazon S3 compared with individual uploads)",
            "Selecting the appropriate backup and/or archival solution",
            "Implementing policies for data access, lifecycle, and protection",
            "Determining when storage auto scaling is required",
            "Amazon S3",
            "Amazon S3 Glacier",
        ],
    },

    # ── Q11: MATCH – Load Balancer Types ──────────────────────────────────────
    {
        "id": qid("ALB NLB Gateway Load Balancer types match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.1",
        "stem": (
            "A solutions architect is selecting the appropriate load balancer for each "
            "architectural scenario. Match each scenario to the correct AWS load balancer type. "
            "Each type is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Application Load Balancer (ALB)",
            "B": "Network Load Balancer (NLB)",
            "C": "Gateway Load Balancer (GWLB)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A microservices platform routes HTTP/HTTPS requests to different backend "
                    "services based on the URL path (/orders/* → Order Service, /catalog/* → "
                    "Catalog Service) and must terminate TLS at the load balancer."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A financial trading application handles millions of concurrent TCP "
                    "connections and requires static IP addresses per Availability Zone for "
                    "firewall whitelisting, ultra-low latency, and the ability to preserve "
                    "client IP addresses at the transport layer."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A security team must route ALL ingress and egress VPC traffic through a "
                    "fleet of third-party virtual firewall appliances for deep packet inspection "
                    "before any traffic reaches its final destination, without changing IP "
                    "addresses or requiring application changes."
                ),
                "correct": "C",
            },
        ],
        "explanation": (
            "ALB operates at Layer 7 (HTTP/HTTPS), supporting content-based routing rules "
            "(path, host, header, query string), WebSocket, and TLS termination — the standard "
            "choice for web applications and microservices. NLB operates at Layer 4 "
            "(TCP/UDP/TLS), provides static Elastic IP addresses per AZ (suitable for firewall "
            "whitelisting), preserves source IP, and handles millions of connections with "
            "microsecond latency. Gateway Load Balancer operates at Layer 3 and uses the "
            "GENEVE protocol to transparently bump-in-the-wire traffic through third-party "
            "security appliance fleets, making it the purpose-built choice for inline network "
            "security inspection."
        ),
        "tags": [
            "Load balancing concepts (for example, Application Load Balancer [ALB])",
            "Multi-tier architectures",
            "Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways)",
        ],
    },

    # ── Q12: MAMCQ – IAM MFA Security ────────────────────────────────────────
    {
        "id": qid("IAM MFA root account enforcement SCP deny mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.1",
        "stem": (
            "A security audit reveals that the AWS root account has no MFA configured and that "
            "IAM users in member accounts can perform any API action from the console without "
            "MFA. The security team must immediately enforce MFA for both root and IAM user "
            "activity with the least operational overhead. Which TWO actions should the "
            "solutions architect take FIRST? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Immediately enable a virtual or hardware MFA device on the AWS management account root user and store the recovery codes in a physical secure location",
            "B": "Create new root account access keys and share them only with trusted administrators who have their own MFA devices, then delete the old keys",
            "C": "Attach an IAM managed policy to all IAM groups that includes a Deny on all actions ('*') when the condition 'aws:MultiFactorAuthPresent' is false, while exempting MFA-enrollment actions so users can self-enroll",
            "D": "Deploy Amazon GuardDuty in all accounts to detect and alert on console logins performed without MFA, then use EventBridge to trigger a Lambda that disables the offending IAM user",
            "E": "Rotate all existing IAM user passwords immediately to force re-authentication, then rely on the identity provider's MFA enforcement for subsequent logins",
        },
        "explanation": (
            "The root account MFA gap is the most critical vulnerability — enabling MFA on the "
            "root user (virtual authenticator or hardware device) directly closes the highest-"
            "risk attack surface. A deny-based IAM policy conditioned on "
            "'aws:MultiFactorAuthPresent: false' is the standard pattern to enforce MFA for "
            "IAM user console and API access; attaching it to groups ensures coverage without "
            "per-user management, and carving out iam:CreateVirtualMFADevice and "
            "iam:EnableMFADevice lets users self-enroll. Root account access keys should never "
            "exist (create or distribute them); GuardDuty detects threats but does not prevent "
            "non-MFA logins; password rotation does not enforce MFA for subsequent logins."
        ),
        "tags": [
            "Applying AWS security best practices to IAM users and root users (for example, multi-factor authentication [MFA])",
            "AWS security best practices (for example, the principle of least privilege)",
            "IAM",
        ],
    },

    # ── Q13: MATCH – Data Migration Services ──────────────────────────────────
    {
        "id": qid("DataSync DMS Snow Transfer Family data migration services match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.5",
        "stem": (
            "A solutions architect must recommend the appropriate AWS service for each data "
            "migration scenario. Match each scenario to the MOST appropriate service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS DataSync",
            "B": "AWS Database Migration Service (AWS DMS)",
            "C": "AWS Snow Family (Snowball Edge)",
            "D": "AWS Transfer Family",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A company must migrate 3 PB of on-premises NAS file data to Amazon S3. "
                    "Its internet connection is 200 Mbps, meaning an online transfer would take "
                    "over a year. The migration must complete within 8 weeks."
                ),
                "correct": "C",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A team must migrate a production Oracle database to Amazon Aurora "
                    "PostgreSQL while keeping both systems in sync during a 2-week parallel-run "
                    "window, using change data capture (CDC) to minimise cutover downtime."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "An analytics team needs to copy 50 TB of NFS file shares from on-premises "
                    "to Amazon EFS over the network, with automatic bandwidth throttling, "
                    "per-file checksum verification, and a configurable schedule."
                ),
                "correct": "A",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A financial institution's external partners deliver daily settlement files "
                    "using SFTP clients. The institution wants to receive these files directly "
                    "into Amazon S3 without changing partner-side tooling or credentials."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "AWS Snow Family (Snowball Edge) is the appropriate choice when the data volume "
            "makes online transfer impractical — physical devices are shipped to the customer, "
            "loaded offline, then shipped back to AWS. AWS DMS supports homogeneous and "
            "heterogeneous database migrations with CDC, keeping source and target in sync "
            "during cutover windows. AWS DataSync is a managed online file-transfer service "
            "that accelerates NFS/SMB/S3/EFS migrations with scheduling, checksums, and "
            "bandwidth throttling. AWS Transfer Family provides fully managed SFTP/FTPS/FTP "
            "endpoints backed by S3 or EFS, so external partners continue to use their "
            "existing SFTP workflows without any client-side changes."
        ),
        "tags": [
            "Selecting the appropriate service for data migration to storage services",
            "Hybrid storage options (for example, AWS DataSync, AWS Transfer Family, AWS Storage Gateway)",
            "AWS DataSync",
            "AWS Transfer Family",
            "AWS DMS",
            "AWS Snow Family",
        ],
    },

    # ── Q14: MAMCQ – CloudFormation + Config Infrastructure Integrity ──────────
    {
        "id": qid("CloudFormation StackSets Config remediation infrastructure integrity mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A platform team manages infrastructure across 60 AWS accounts in an AWS "
            "Organisation. They must ensure identical VPC configurations (subnets, NACLs, "
            "security groups) are deployed in every account and that any out-of-band manual "
            "changes to those resources are automatically detected and reverted. Which TWO "
            "actions should the solutions architect implement? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Use AWS CloudFormation StackSets with service-managed permissions to deploy and maintain the VPC stack across all Organisation member accounts automatically, including accounts added in future",
            "B": "Run CloudFormation drift detection on each stack daily via a scheduled Lambda and send SNS email notifications to administrators whenever drift is detected",
            "C": "Enable AWS Config with relevant managed rules (e.g. vpc-sg-open-only-to-authorized-ports) and configure automatic remediation using AWS Systems Manager Automation documents to revert unauthorised changes",
            "D": "Attach IAM deny policies in each account that block all VPC modification API calls (ec2:ModifyVpcAttribute, ec2:DeleteSubnet, etc.) to prevent manual changes entirely",
            "E": "Use AWS Service Catalog to create a VPC portfolio product and require all teams to provision VPCs exclusively through the catalog, preventing direct console creation",
        },
        "explanation": (
            "CloudFormation StackSets with service-managed permissions integrates with AWS "
            "Organisations to automatically deploy stacks to existing and future member "
            "accounts, ensuring consistent baseline configurations at scale. AWS Config "
            "continuously evaluates resource configurations against defined rules; pairing "
            "rules with SSM Automation remediation documents creates a detect-and-remediate "
            "loop that automatically reverts unauthorised changes — this is the canonical "
            "pattern for enforcing infrastructure integrity. Drift detection alone only "
            "notifies; it does not revert changes. Blanket IAM deny policies break legitimate "
            "operational workflows. Service Catalog governs provisioning but does not "
            "prevent or remediate out-of-band changes made directly via the console or API."
        ),
        "tags": [
            "Determining automation strategies to ensure infrastructure integrity",
            "AWS CloudFormation",
            "AWS Config",
            "AWS Systems Manager",
        ],
    },

    # ── Q15: MATCH – Network Connectivity Options ──────────────────────────────
    {
        "id": qid("VPN Direct Connect PrivateLink VPC Peering connectivity match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "1.2",
        "stem": (
            "A solutions architect is selecting network connectivity options for four different "
            "connectivity requirements. Match each requirement to the MOST appropriate AWS "
            "networking service. Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Site-to-Site VPN",
            "B": "AWS Direct Connect",
            "C": "AWS PrivateLink",
            "D": "VPC Peering",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "Two VPCs in the same Region must route traffic between their private CIDR "
                    "ranges with low latency and no bandwidth throttling. The connection must "
                    "not traverse the internet and there is no overlapping IP space."
                ),
                "correct": "D",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A company needs encrypted connectivity from its on-premises data centre "
                    "to an AWS VPC within hours, without waiting for months of physical circuit "
                    "provisioning, accepting that traffic will traverse the public internet."
                ),
                "correct": "A",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A SaaS provider wants to expose a specific service running in their VPC "
                    "to thousands of customer VPCs across different AWS accounts and Regions "
                    "without peering VPCs, advertising CIDR routes, or exposing the service "
                    "to the public internet."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A bank requires a private, dedicated 10 Gbps connection to AWS with "
                    "consistent, low-latency performance that never traverses the public "
                    "internet and supports a Service Level Agreement with AWS."
                ),
                "correct": "B",
            },
        ],
        "explanation": (
            "VPC Peering creates a direct private connection between two VPCs (same or "
            "different accounts/Regions) using private IP addresses, with no internet "
            "traversal and no bandwidth cap — ideal for same-Region private routing with "
            "non-overlapping CIDRs. Site-to-Site VPN is an encrypted IPSec tunnel over the "
            "public internet that can be provisioned in hours, making it the fastest path to "
            "on-premises connectivity. PrivateLink exposes services through Network Load "
            "Balancer endpoints that consumers access via Interface VPC Endpoints, enabling "
            "service-specific private access without VPC routing or CIDR overlap concerns. "
            "Direct Connect is a dedicated physical circuit (1/10/100 Gbps) with consistent "
            "network performance and no public internet traversal, suitable for demanding "
            "enterprise workloads with SLA requirements."
        ),
        "tags": [
            "Securing external network connections to and from the AWS Cloud (for example, VPN, AWS Direct Connect)",
            "Reviewing existing workloads for network optimizations",
            "Network services with appropriate use cases (for example, DNS)",
            "AWS Direct Connect",
            "AWS Client VPN",
            "AWS PrivateLink",
        ],
    },

    # ── Q16: MAMCQ – EKS Anywhere + ECS Anywhere ─────────────────────────────
    {
        "id": qid("EKS Anywhere ECS Anywhere hybrid container management mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "3.2",
        "stem": (
            "A manufacturing company runs containerised workloads on-premises for data-residency "
            "reasons and also runs workloads on AWS. Some applications use Kubernetes (managed "
            "via Amazon EKS in the cloud) and others use Amazon ECS. The team wants a unified "
            "AWS-native control plane for BOTH on-premises Kubernetes and on-premises ECS "
            "workloads using their existing on-premises servers — without purchasing additional "
            "dedicated hardware from AWS. Which TWO services satisfy this requirement? "
            "(Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Amazon EKS Anywhere — deploys and manages Kubernetes clusters on the company's existing on-premises infrastructure using the same EKS tooling and control plane APIs",
            "B": "AWS Outposts rack — delivers fully AWS-managed infrastructure (EC2, EKS, ECS) deployed at the company's data centre on dedicated AWS-supplied hardware",
            "C": "Amazon ECS Anywhere — registers the company's existing on-premises servers as ECS external instances that are managed through the same ECS control plane in the AWS console",
            "D": "AWS Fargate — runs ECS and EKS tasks on AWS-managed infrastructure so the company no longer needs to manage any servers",
            "E": "Amazon EC2 instances in AWS Local Zones configured as ECS container instances, placed closer to the on-premises facility to reduce latency",
        },
        "explanation": (
            "EKS Anywhere extends the Amazon EKS control plane to customer-owned infrastructure "
            "(on-premises bare metal, VMware vSphere, etc.) so teams manage on-premises "
            "Kubernetes clusters using the same eksctl, kubectl, and AWS Console workflows as "
            "cloud EKS clusters. ECS Anywhere registers any Linux server (physical or VM) as "
            "an ECS external instance via the SSM agent; it appears in the ECS control plane "
            "alongside cloud instances, enabling unified task scheduling and management. AWS "
            "Outposts requires purchasing and installing AWS-supplied rack hardware — this "
            "contradicts the 'no additional hardware' requirement. Fargate is a serverless "
            "AWS-only compute engine and does not extend to on-premises servers. Local Zone "
            "instances still run in AWS infrastructure and are not physically on-premises."
        ),
        "tags": [
            "Hybrid compute options (for example, AWS Outposts)",
            "Amazon ECS Anywhere",
            "Amazon EKS Anywhere",
            "Determining the appropriate placement of resources to meet business requirements",
        ],
    },

    # ── Q17: MATCH – Storage Gateway Modes + DataSync ─────────────────────────
    {
        "id": qid("Storage Gateway File Volume DataSync Transfer Family hybrid storage match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "3.1",
        "stem": (
            "A solutions architect must recommend the correct AWS storage service for each "
            "hybrid storage scenario. Match each scenario to the MOST appropriate service. "
            "Each service is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "AWS Storage Gateway – File Gateway",
            "B": "AWS Storage Gateway – Volume Gateway (Cached mode)",
            "C": "AWS DataSync",
            "D": "AWS Transfer Family",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A video-production studio needs on-premises NFS and SMB shares that "
                    "transparently back to Amazon S3, allowing editing workstations to read "
                    "and write cloud-stored video files without any application changes."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A hospital's legacy PACS imaging system uses iSCSI block storage. The "
                    "team wants to keep a frequently accessed local cache on-premises while "
                    "durably storing all primary volumes in AWS for disaster recovery."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A company is migrating 80 TB of on-premises NFS data to Amazon EFS over "
                    "a 3-week window. The migration must include per-file checksum verification, "
                    "bandwidth throttling to protect production traffic, and automated scheduling."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "External trading partners transmit daily settlement files using SFTP "
                    "client software. The company wants to receive these files into Amazon S3 "
                    "without requiring any partner-side reconfiguration of SFTP endpoints or "
                    "credentials."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "File Gateway presents S3 buckets as NFS/SMB file shares on-premises with a local "
            "cache, making S3 appear as a network file system to existing applications. Volume "
            "Gateway (Cached mode) presents iSCSI block volumes on-premises with frequently "
            "accessed data cached locally and all data stored durably in AWS — ideal for "
            "legacy block-storage applications needing cloud backup. DataSync is a managed "
            "online migration service with scheduling, per-file checksums, bandwidth "
            "throttling, and filtering — purpose-built for large-scale file migrations. "
            "Transfer Family provides managed SFTP/FTPS/FTP endpoints that store files "
            "directly in S3 or EFS, letting external partners continue using their existing "
            "SFTP tooling unchanged."
        ),
        "tags": [
            "Hybrid storage options (for example, AWS DataSync, AWS Transfer Family, AWS Storage Gateway)",
            "Storage options and characteristics (for example, durability, replication)",
            "AWS DataSync",
            "AWS Storage Gateway",
            "AWS Transfer Family",
        ],
    },

    # ── Q18: MAMCQ – Amazon Inspector + Patch Manager ─────────────────────────
    {
        "id": qid("Amazon Inspector v2 Patch Manager CVE vulnerability remediation mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "1.3",
        "stem": (
            "A security team requires continuous assessment of EC2 instances and Amazon ECR "
            "container images for known CVEs and must automatically patch EC2 instances that "
            "fall outside the approved patch baseline without manual intervention. Which TWO "
            "services should the solutions architect implement to fulfil BOTH requirements? "
            "(Select TWO.)"
        ),
        "correct": ["A", "D"],
        "difficulty": "HARD",
        "answers": {
            "A": "Enable Amazon Inspector v2 to continuously scan EC2 instances and ECR container images for software vulnerabilities (CVEs) and unintended network exposure, generating prioritised findings",
            "B": "Enable Amazon GuardDuty to detect unusual API calls and network anomalies that may indicate active exploitation of a software vulnerability",
            "C": "Create an AWS Config managed rule (ec2-instance-managed-by-systems-manager) and configure auto-remediation to terminate non-compliant instances",
            "D": "Use AWS Systems Manager Patch Manager to define a patch baseline and maintenance window; SSM automatically installs approved patches on non-compliant EC2 instances on schedule",
            "E": "Use AWS Trusted Advisor security checks to identify EC2 instances running outdated AMIs and trigger an EventBridge rule to invoke Lambda for remediation",
        },
        "explanation": (
            "Amazon Inspector v2 is the purpose-built continuous vulnerability assessment "
            "service: it scans EC2 instances (via the SSM agent) and ECR images for CVEs and "
            "network reachability issues, generating prioritised findings with CVSS scores. "
            "AWS Systems Manager Patch Manager closes the remediation loop: administrators "
            "define a patch baseline (approved patches), create a maintenance window, and SSM "
            "automatically installs missing patches on EC2 instances on the defined schedule — "
            "no manual intervention required. GuardDuty detects active threats and anomalies "
            "but does not assess or remediate software vulnerabilities. Config rules and "
            "instance termination are too disruptive as a remediation for patch compliance. "
            "Trusted Advisor security checks are not designed for continuous CVE scanning and "
            "do not provide CVSS-prioritised vulnerability findings."
        ),
        "tags": [
            "Determining automation strategies to ensure infrastructure integrity",
            "Implementing data backups and replications",
            "Amazon Inspector",
            "AWS Systems Manager",
        ],
    },

    # ── Q19: MATCH – Availability Tiers ───────────────────────────────────────
    {
        "id": qid("Availability tiers single-AZ multi-AZ multi-region active-passive match"),
        "type": "MATCH",
        "exam": EXAM,
        "taskStatement": "2.2",
        "stem": (
            "A solutions architect must recommend the appropriate deployment model for four "
            "workloads with different availability requirements. Match each workload profile to "
            "the MOST cost-effective deployment model that meets its requirements. "
            "Each model is used once."
        ),
        "difficulty": "HARD",
        "answers": {
            "A": "Single-AZ deployment with no cross-AZ redundancy",
            "B": "Multi-AZ deployment within a single AWS Region",
            "C": "Multi-Region active-passive (primary Region serves traffic; DR Region on standby)",
            "D": "Multi-Region active-active (all Regions simultaneously serve live traffic)",
        },
        "subquestions": [
            {
                "id": "sq1",
                "prompt": (
                    "A development and QA environment used only during business hours by an "
                    "internal team of eight engineers. Occasional downtime is acceptable; "
                    "minimising monthly cost is the primary driver."
                ),
                "correct": "A",
            },
            {
                "id": "sq2",
                "prompt": (
                    "A customer-facing e-commerce site with a 99.99% monthly availability SLA "
                    "serving a single country. The architecture must survive an Availability "
                    "Zone outage with automatic failover and no data loss."
                ),
                "correct": "B",
            },
            {
                "id": "sq3",
                "prompt": (
                    "A financial regulatory reporting system with an RTO of 4 hours and RPO of "
                    "1 hour that must survive a complete AWS Region failure. The system does "
                    "not need to serve traffic from the DR Region during normal operations."
                ),
                "correct": "C",
            },
            {
                "id": "sq4",
                "prompt": (
                    "A globally distributed payment platform serving North America and Europe "
                    "with an SLA of 99.999% and zero-data-loss requirements. Any single Region "
                    "failure must be invisible to end users."
                ),
                "correct": "D",
            },
        ],
        "explanation": (
            "A single-AZ deployment offers the lowest cost but no redundancy — acceptable for "
            "non-production environments where downtime has no business impact. Multi-AZ within "
            "a Region provides automatic failover across AZs (each AZ is a separate physical "
            "data centre) with synchronous replication — the standard pattern for high-"
            "availability production workloads in one geography. Multi-Region active-passive "
            "maintains a standby environment in a second Region that is activated on failover; "
            "it meets multi-hour RTO targets at lower cost than active-active. Multi-Region "
            "active-active distributes live traffic globally with synchronous or near-"
            "synchronous replication, achieving the highest availability (99.999%+) and "
            "zero-data-loss at the highest cost."
        ),
        "tags": [
            "Determining the required availability for different classes of workloads (for example, production workloads, non-production workloads)",
            "Disaster recovery (DR) strategies (for example, backup and restore, pilot light, warm standby, active-active failover, recovery point objective [RPO], recovery time objective [RTO])",
            "Determining the appropriate placement of resources to meet business requirements",
        ],
    },

    # ── Q20: MAMCQ – Compute Cost Optimisation ────────────────────────────────
    {
        "id": qid("Spot Instances Savings Plans compute cost optimization ML inference mamcq"),
        "type": "MAMCQ",
        "exam": EXAM,
        "taskStatement": "4.2",
        "stem": (
            "A company runs two EC2-based workloads. The first is a large-scale ML training "
            "job that can tolerate interruptions, checkpoints its progress every 30 minutes to "
            "Amazon S3, and runs 8–12 hours per job with 20 jobs per month. The second is a "
            "real-time inference API that has run 24/7 for two years with stable, predictable "
            "compute requirements and cannot tolerate interruptions. Which TWO purchasing "
            "options minimise total EC2 cost for BOTH workloads? (Select TWO.)"
        ),
        "correct": ["A", "C"],
        "difficulty": "HARD",
        "answers": {
            "A": "Use EC2 Spot Instances for the ML training workload; if interrupted, the checkpoint in S3 limits recomputation to at most 30 minutes",
            "B": "Use EC2 On-Demand Instances for both workloads to ensure maximum availability and simplify cost forecasting",
            "C": "Purchase a 1-year Compute Savings Plan or Reserved Instances for the inference API to reduce the steady-state 24/7 compute bill by up to 72% compared to On-Demand",
            "D": "Use EC2 Dedicated Hosts for the inference API; the per-host billing model reduces cost for stable, long-running workloads compared to On-Demand per-instance pricing",
            "E": "Use EC2 Spot Instances for the real-time inference API, applying Spot capacity pools across multiple instance families and Availability Zones to minimise interruption risk",
        },
        "explanation": (
            "Spot Instances offer up to 90% savings over On-Demand for interruption-tolerant "
            "workloads. Because the ML training job checkpoints every 30 minutes, a Spot "
            "interruption causes at most 30 minutes of lost work — a low risk-to-savings "
            "trade-off. A Compute Savings Plan (or EC2 Reserved Instance) provides 40–72% "
            "savings for workloads with stable, predictable usage — the 24/7 inference API "
            "is a textbook candidate. On-Demand pricing for both workloads is the most "
            "expensive option. Dedicated Hosts are primarily for BYOL licensing compliance "
            "(e.g., Windows Server, SQL Server per-core licensing); their per-host cost "
            "does not inherently provide savings over RIs/Savings Plans for general workloads. "
            "Spot Instances are inappropriate for real-time inference APIs that cannot tolerate "
            "interruption — a Spot reclaim would take the endpoint offline immediately."
        ),
        "tags": [
            "Determining appropriate scaling methods and strategies for elastic workloads (for example, horizontal compared with vertical, EC2 hibernation)",
            "Determining the required availability for different classes of workloads (for example, production workloads, non-production workloads)",
            "AWS purchasing options (for example, Spot Instances, Reserved Instances, Savings Plans)",
            "Amazon EC2",
        ],
    },
]

# ── Load, append, write ────────────────────────────────────────────────────────
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
