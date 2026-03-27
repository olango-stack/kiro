[Option 4] Spec-driven development using Claude Code
Architecture diagram for a synchronous user microservice

What Is Spec-Driven Development?
AI coding assistants are powerful, and it is tempting to jump straight in: "Build me a users API with authentication." The AI will produce something, but you have little control over the architecture, no way to review the plan before implementation starts, and no shared document to reference when things go sideways. Sound familiar?

Spec-driven development flips the order. Before a single line of code is written, you invest time in defining three things:

What you are building: requirements expressed as user stories with testable acceptance criteria
How it should work: a design document mapping requirements to technical components and data flows
What steps are needed: an ordered task list with dependencies and verification checkpoints
These structured documents become first-class artifacts in your project, just like source code. They are version-controlled, reviewable, and repeatable. Hand the same spec to an AI tool tomorrow and you get consistent results. Hand it to a different AI tool entirely and the intent carries over.

Why This Matters
Specs solve three fundamental problems in AI-assisted development.

First, clarity. Without specs, edge cases surface during code review or, worse, in production. Writing a spec forces you to think through those edge cases before any code exists, when changes are cheap and consequences are low.

Second, reviewability. Without specs, the first artifact a teammate can review is code, and reworking code is expensive. A spec gives you a lightweight design review that catches misunderstandings early, before anyone has invested time in implementation.

Third, reproducibility. A freeform prompt produces different results every time you run it. Structured specs produce consistent, predictable output because the AI receives the same detailed instructions on every run.

The core insight behind all three is simple: the quality of AI-generated code is bounded by the quality of the instructions it receives. A vague prompt produces vague code. A precise spec produces precise code.

The Three Spec Documents
Regardless of tooling, spec-driven workflows converge on the same three artifacts:

Requirements (requirements.md) capture what the system must do. Good requirements use structured formats like user stories with acceptance criteria written in testable language: "WHEN a POST request is sent to /users with a valid JSON body, THE System SHALL create a new user record with a unique UUID." If you cannot write a test for a requirement, it is too vague.

Design (design.md) maps requirements to how the system is built. It names the components (DynamoDB table, Lambda function, API Gateway), describes how data flows between them, and documents key configuration choices. A simple ASCII diagram and a table of components is enough; AI tools read text, not polished architecture diagrams.

Tasks (tasks.md) break the design into discrete, ordered implementation steps. Good tasks respect dependencies (create the database before the function that reads it), are individually verifiable (each ends with a way to confirm it worked), and are small (one logical change per task).

The three files work together: requirements define what, design defines how, and tasks break it into steps. Together they form a complete blueprint that an AI coding assistant can follow methodically.

Tools and Frameworks for Spec-Driven Development
The spec-driven approach is tool-agnostic. You can write specs in a plain text editor and hand them to any AI assistant. That said, several tools have emerged to streamline the workflow:

Kiro  is an IDE with a built-in spec-driven workflow. Kiro walks you through requirements, design, and task generation step by step, with AI assistance at each phase. It distinguishes between a structured "Spec" mode for complex features and a lightweight "Vibe" mode for quick prototyping.

OpenSpec  is a framework for incremental specification management. OpenSpec introduces the concept of delta specs: changes expressed as ADDED, MODIFIED, or REMOVED requirements relative to an existing baseline. This makes evolving specs over time transparent and reviewable, particularly useful for larger projects.

BMAD Method  is a framework that orchestrates multiple AI agent personas (product manager, architect, developer) to collaboratively produce specs. BMAD guides you from brainstorming through adversarial review to implementation, adapting to your project's complexity.

Each tool takes a different approach, but they all share the same philosophy: define before you build.

This Module: Specs + Claude Code
In this module you will apply spec-driven development using Claude Code, Anthropic's agentic coding tool for the terminal. Starting from an empty directory, you will build a complete serverless Users Service by writing specs first and then handing them to Claude Code for implementation.

You will learn how to:

Write a CLAUDE.md file that gives Claude Code persistent knowledge about your project (the equivalent of project-level steering docs in other tools)
Author specification documents (requirements, design, and tasks) by hand, or use Claude Code's plan mode to draft them collaboratively
Hand those specs to Claude Code and watch it build infrastructure, application code, and tests
Services used in this module
Claude Code  - Anthropic's agentic coding tool for the terminal
AWS API Gateway  - the front door for applications; REST, HTTP, and WebSocket APIs
AWS Lambda  - compute service; functions in serverless runtimes
AWS Cognito  - identity store for user sign-up and sign-in
AWS DynamoDB  - a fully managed NoSQL key/value data store
Terraform  - infrastructure as code tool for provisioning AWS resources
What you will accomplish
By the end of this module, you will have:

Created a CLAUDE.md file that gives Claude Code persistent project context
Written specification documents (requirements, design, and tasks) that define your application
Used Claude Code to implement a DynamoDB table with Terraform
Generated a Lambda function for full CRUD operations on users
Configured API Gateway with REST endpoints and a Lambda authorizer
Implemented Cognito authentication with JWT validation
Written and run unit tests with pytest and moto
Deployed everything using Terraform, with Claude Code running the commands for you
Estimated duration: 60-90 minutes

How this module works
Throughout this module, you will give Claude Code natural-language instructions. Since Claude Code is non-deterministic, its output may differ from the examples shown. Expandable "Reference Code" sections provide working code you can fall back on if you get stuck.

Let's get started by setting up your development environment and Claude Code!

Development Environment Setup
This page walks you through opening your development environment, verifying that Claude Code is installed, and launching your first session. The whole setup takes about five minutes.

Open your terminal environment
Scroll to the Event outputs pane at the bottom of the Workshop Studio event page.
Event Outputs

Click the URL labeled VSCodeServerURL to open VS Code Server in a new browser tab.

In the login dialog, paste the development environment password you copied from the event page and choose Sign in.

VS Code Server password dialog

You should see VS Code running in your browser. Open a terminal with Terminal → New Terminal from the menu bar.
Verify Claude Code is installed
In the terminal, run:

claude --version

You should see a version number. If the command is not found, install Claude Code:

npm install -g @anthropic-ai/claude-code

Verify AWS credentials
Claude Code will run Terraform commands on your behalf. Verify your AWS credentials are configured:

aws sts get-caller-identity

You should see your AWS account ID and IAM role in the output.

Create your working directory
Create a fresh directory for the workshop project and initialize a git repository:

mkdir -p ~/workspace/my-workspace && cd ~/workspace/my-workspace
git init

Add a .gitignore to keep Terraform state and build artifacts out of version control:

cat > .gitignore << 'EOF'
.terraform/
*.tfstate
*.tfstate.backup
*.tfplan
__pycache__/
*.pyc
.pytest_cache/
EOF

The git repository enables several Claude Code features you will use later: /commit for creating commits with AI-generated messages, /rewind for stepping back through actions, and /diff for reviewing changes.

Start Claude Code
Launch Claude Code from inside the project directory:

claude

You will see the Claude Code welcome screen. Claude Code is ready when you see the > prompt.

Claude Code permission mode
When Claude Code proposes an action (creating a file, running a command), it will ask for your approval. You can type yes or press Enter to allow it. You can also use --dangerously-skip-permissions to allow all actions automatically. This is not recommended for a first-time session since reviewing each action is how you learn what Claude Code is doing.

Install the AWS Serverless plugin
Claude Code is fully capable of building serverless applications out of the box. It already knows AWS services, Terraform syntax, and Python Lambda patterns from its training data. You can complete this entire workshop without any plugins.

So why install one? Plugins raise the floor. Without a plugin, Claude Code draws on its general knowledge and usually makes good choices. With the aws-serverless plugin, it draws on curated, AWS-specific guidance that reflects current best practices, common pitfalls, and proven architectural patterns. The difference shows up in the details: better IAM scoping, correct event source mappings on the first try, proper CORS configuration for API Gateway, and observability patterns (structured logging, X-Ray tracing) included by default rather than as an afterthought.

Think of it this way: Claude Code without a plugin is a strong generalist developer. Claude Code with the serverless plugin is that same developer after reading every AWS Lambda and API Gateway best-practices guide. The plugin does not unlock new capabilities. It makes the existing ones more reliable and more aligned with AWS conventions.

AWS provides an open-source plugin collection at awslabs/agent-plugins  that includes plugins for serverless development, architecture design, and deployment workflows. You will install the aws-serverless plugin for this workshop.

At the > prompt, type:

/plugin install aws-serverless@claude-plugins-official

Approve the installation when prompted. The plugin includes four skills that activate automatically when your prompts match their domain:

Skill	What it provides
aws-lambda	Lambda function development, event-driven architectures, event source mappings, cold start optimization, observability
api-gateway	REST, HTTP, and WebSocket API design; Lambda authorizers; CORS; custom domains; throttling; troubleshooting 4xx/5xx errors
aws-serverless-deployment	SAM and CDK deployment workflows, template validation, multi-environment patterns, CI/CD pipelines
aws-lambda-durable-functions	Resilient multi-step workflows with checkpointing using Lambda durable functions
The plugin also bundles an MCP server that gives Claude Code access to serverless-specific tooling.

How plugins work
Plugins are self-contained packages that can bundle skills, agents, hooks, and MCP servers. You do not need to invoke plugin skills explicitly. Claude Code activates the relevant skill automatically when your prompt matches its description. For example, when you ask Claude Code to "create a REST API with a Lambda authorizer," the api-gateway skill activates and provides Claude Code with detailed guidance on authentication patterns, OpenAPI extensions, and SAM template structure.

You can manage plugins at any time with /plugin to open the plugin manager, or /reload-plugins to apply changes without restarting your session.

You have configured your development environment, installed the AWS Serverless plugin, and Claude Code is running.
Next, we will create the project context file that gives Claude Code persistent knowledge about your project.


MVP: Users Service
Overview
In this section you will build a serverless user management platform that centralizes user data into a single, secure API. The MVP supports creating, reading, updating, and deleting user records through authenticated REST endpoints.

Services:

DynamoDB: User data storage
Lambda (Python): CRUD operations and authentication
API Gateway: REST API endpoints
Cognito + Lambda Authorizer: JWT-based authentication
Terraform: Infrastructure as code
Project Structure
Your specs and code will live side by side in the project directory:

my-workspace/
├── CLAUDE.md               ← persistent project context
├── specs/
│   └── users-service/
│       ├── requirements.md ← user stories and acceptance criteria
│       ├── design.md       ← architecture and data flow
│       └── tasks.md        ← discrete implementation tasks
├── src/                    ← Lambda function source code
├── tests/                  ← unit and integration tests
└── *.tf                    ← Terraform infrastructure files
Workflow
Now that you understand the spec-driven approach, here is how it maps to concrete steps in this module:

CLAUDE.md: Establish persistent project knowledge (tech stack, best practices)
Requirements: Define user stories and acceptance criteria
Design: Document technical architecture and data flow
Tasks: Break down work into discrete, trackable steps
Execution: Claude Code reads the specs and implements them
Additional Resources
Claude Code: CLAUDE.md documentation 
Spec-driven development with Claude Code 
Let's begin with the foundation: creating the CLAUDE.md file that gives Claude Code persistent knowledge about your project.

0 - Create CLAUDE.md
Before generating specs or writing any code, create a CLAUDE.md file in your project root. This file gives Claude Code persistent knowledge about your project that carries over across every conversation.

Why CLAUDE.md?
Every time you start a new Claude Code session, it reads CLAUDE.md automatically. Without it, you would have to explain your tech stack, goals, and preferences at the start of each conversation. With it, Claude Code consistently follows your patterns from the very first prompt.

Think of CLAUDE.md as the project brief that a new team member reads on their first day. It answers the big questions upfront: What are we building? What tools are we using? What practices do we follow?

A typical CLAUDE.md starts with a project overview so Claude Code knows what you are building and why. It then lists the technology stack so it reaches for the right services and tools. Finally, it captures best practices (coding style, testing conventions, and deployment patterns) so every generated file follows the same standards.

Create CLAUDE.md
In your project root (~/workspace/my-workspace), create a file named CLAUDE.md with the following content.

Keep it focused, not prescriptive
A good CLAUDE.md tells Claude Code what matters: tech stack, quality expectations, and guardrails. You do not need to prescribe every file name or variable value. Claude Code works best when it has room to make reasonable decisions within your stated constraints. You can always refine the file as the project evolves.

CLAUDE.md (copy this into your project)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
# AnyCompany Users Service

## Project Overview

Serverless Users Service for AnyCompany. A RESTful API for managing user records with
JWT-based authentication. All infrastructure is defined with Terraform and deployed to AWS.

## Technology Stack

- **IaC**: Terraform (`.tf` files in project root)
- **Language**: Python 3.10
- **Compute**: AWS Lambda
- **Database**: Amazon DynamoDB (on-demand billing)
- **API**: Amazon API Gateway REST API (v1)
- **Auth**: Amazon Cognito User Pool + Lambda Token Authorizer

## Best Practices

- Use descriptive resource names with a consistent prefix to avoid naming collisions
- Lambda functions use Python logging (`logging.getLogger()`) at INFO level
- All HTTP responses include CORS headers
- Timestamps stored as ISO 8601 strings
- User IDs are UUIDs generated server-side when not provided by the caller
- Terraform resources are organized by concern (one `.tf` file per logical component)
- API Gateway is defined using an OpenAPI 3.0 JSON body for clear endpoint documentation

## Testing

- Unit tests live in `tests/unit/` and run with `pytest`
- Use `moto` for AWS service mocking in unit tests
- Every Lambda function should have test coverage for its happy path and error cases

Notice what this file does not do: it does not dictate exact file names, variable values, or folder hierarchies. It tells Claude Code the technology choices and quality expectations, then trusts it to make sensible structural decisions. If Claude Code proposes something you disagree with, you can say no and steer it in a different direction.

Verify the File
After creating the file, confirm it exists:

cat CLAUDE.md

How Claude Code Uses CLAUDE.md
When you start a new Claude Code session inside the project directory, it automatically reads CLAUDE.md and uses it as context for all requests. You can verify this by asking:

claude

Then at the prompt:

What tech stack is this project using?
Claude Code will answer based on your CLAUDE.md content without you needing to explain anything.

CLAUDE.md is version-controlled
Commit CLAUDE.md to your repository alongside your code. It is a first-class project artifact, just like README.md or .editorconfig. Team members who clone the repository automatically get the same Claude Code context.

Your CLAUDE.md is ready. Claude Code now has persistent knowledge of your project.
Next, you will write the spec documents that define what to build.



1 - Write Specifications
With CLAUDE.md in place, the next step is to write three spec files that tell Claude Code what to build:

requirements.md: user stories and acceptance criteria
design.md: architecture, components, and data flow
tasks.md: discrete, trackable implementation steps
First, create the specs directory:

mkdir -p specs/users-service

Approach 1: Write Specs by Hand
The most educational approach is to write the specs yourself. You do not need a special tool; a text editor and clear thinking are enough. Here is how to approach each file.

requirements.md: What to Build
A good requirements file contains user stories and acceptance criteria. Each requirement follows a pattern:

**User Story:** As a [role], I want to [action] so that [benefit].

**Acceptance Criteria:**
1. WHEN [condition], THE System SHALL [behavior]
2. WHEN [condition], THE System SHALL [behavior]
The "WHEN... SHALL..." format (sometimes called EARS notation) makes requirements testable. If you can not write a test for a requirement, it is too vague.

For our Users Service, think about what the API needs to do:

CRUD operations: create, read, update, delete user records
Authentication: only authorized callers can access the API
Data storage: records persist in a database
Tip: Start with the obvious, then refine
Your first draft does not need to be perfect. Write the requirements you know, then ask yourself: "What happens when the user ID is missing? What format should timestamps use? What response code does a delete return?" Each question you answer now is a bug you prevent later.

design.md: How to Build It
The design document maps requirements to technical components. For each component, answer:

What AWS service implements it?
How does data flow between components?
What are the key configuration choices (billing mode, runtime, stage name)?
A simple architecture diagram in ASCII or a table of components works well. You do not need polished diagrams; Claude Code reads text, not images.

tasks.md: Steps to Implement
Break the design into discrete tasks that can be implemented and verified one at a time. Good tasks are:

Ordered: respect dependencies (create the database before the function that reads it)
Verifiable: each task ends with a way to confirm it worked
Small: one logical change per task (not "build everything")
Group tasks by concern: infrastructure first, then business logic, then API, then auth, then testing.

Approach 2: Use Claude Code Plan Mode
If you prefer a guided experience, Claude Code itself can help you draft specs. Claude Code has a dedicated plan mode where it thinks through problems, proposes solutions, and discusses tradeoffs, all without writing a single file or running any command. This makes it ideal for spec authoring: you want Claude Code's reasoning, not its actions.

Enter plan mode
Type /plan in your Claude Code session to switch to plan mode. You will see the prompt change to indicate you are in planning mode. Now give it the project context:

I need to build a serverless Users Service with these characteristics:
- RESTful API for CRUD operations on user records
- JWT authentication using Amazon Cognito
- DynamoDB for storage
- Terraform for infrastructure
- Python Lambda functions

Help me write three specification files:
1. specs/users-service/requirements.md - user stories with testable acceptance criteria
2. specs/users-service/design.md - architecture, components, and data flow
3. specs/users-service/tasks.md - ordered implementation tasks with verification steps

Draft each file and let me review before saving.

In plan mode, Claude Code will draft each file as text in the conversation rather than creating files on disk. This is exactly what you want: a proposal you can review and iterate on before committing to anything.

Iterate on the plan
This is where plan mode earns its keep. Push back on the proposals. Ask questions:

Why did you choose a Token authorizer instead of a Request authorizer? What are the tradeoffs?
The tasks look too coarse. Can you break Task 2 into smaller subtasks that I can verify independently?
Claude Code will reason through your question and revise its proposal. You are having a design conversation, not generating code. Each round of feedback sharpens the spec.

Switch back to act mode
When you are satisfied with the specs, exit plan mode:

/plan

The /plan command toggles between plan mode and act mode. Back in act mode, tell Claude Code to save the files:

Save the three spec files we just drafted to specs/users-service/.

Claude Code will create the files with the content you reviewed and approved.

When to use plan mode vs. act mode
Use plan mode when you want to think before you build: drafting specs, exploring architecture options, discussing tradeoffs, or reviewing a design. Use act mode when you want Claude Code to create files, run commands, and make changes. The toggle is instant, so switch as often as you need. Many developers start a task in plan mode to sketch the approach, switch to act mode for implementation, and flip back to plan mode when they hit a design question.

Reference Specs
Whether you wrote specs by hand or used Claude Code to draft them, compare your output against these reference specs. They were derived from the end-state implementation and represent what a solid spec looks like for this project.

If you want to skip the writing exercise and jump straight to implementation, copy these files directly into specs/users-service/.

specs/users-service/requirements.md
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
# Requirements: Serverless Users Service

## User Stories

### Requirement 1: User Record Management

**User Story:** As an API consumer, I want to create, read, update, and delete user
records so that I can manage user data programmatically through a consistent API.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/users` with a valid JSON body, THE System SHALL create
   a new user record with a unique UUID as `userid` if one is not provided
2. WHEN a GET request is sent to `/users`, THE System SHALL return all user records from
   the database
3. WHEN a GET request is sent to `/users/{userid}`, THE System SHALL return the specific
   user record, or an empty object if not found
4. WHEN a PUT request is sent to `/users/{userid}`, THE System SHALL overwrite the user
   record with the provided JSON body, preserving the `userid`
5. WHEN a DELETE request is sent to `/users/{userid}`, THE System SHALL remove the user
   record from the database
6. THE System SHALL include a `timestamp` field (ISO 8601) on every created or updated record
7. ALL API responses SHALL include `Access-Control-Allow-Origin: *` header

### Requirement 2: Authentication

**User Story:** As a system administrator, I want all API endpoints protected by JWT
authentication so that only authorized users can access or modify user data.

#### Acceptance Criteria

1. THE Authentication_Service SHALL use Amazon Cognito as the identity provider
2. WHEN a request is made without a valid `Authorization` header, THE API SHALL return
   HTTP 401 Unauthorized
3. WHEN a valid JWT token is provided in the `Authorization` header, THE Authorizer SHALL
   verify the token signature using the Cognito JWKS endpoint
4. THE Authorizer SHALL cache the JWKS public keys during Lambda cold start to reduce
   latency on subsequent invocations
5. THE Cognito User Pool SHALL support email/password authentication
   (USER_PASSWORD_AUTH flow)

### Requirement 3: Data Storage

**User Story:** As a developer, I want user data stored in a managed NoSQL database so
that storage scales automatically without capacity planning.

#### Acceptance Criteria

1. THE System SHALL store user records in DynamoDB with `userid` (String) as partition key
2. THE DynamoDB table SHALL use PAY_PER_REQUEST billing mode
3. THE System SHALL support storing arbitrary JSON fields alongside the required `userid`
   and `timestamp` fields

specs/users-service/design.md
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
# Design: Serverless Users Service

## Architecture Overview

```
Client
  │
  ▼
API Gateway (REST, v1)
  │  Authorization header
  ├──────────────────────▶ Lambda Authorizer ──▶ Cognito JWKS
  │  (on valid JWT)
  ▼
Lambda (CRUD) ──▶ DynamoDB Table
```

All resources are deployed to a single AWS region. Infrastructure is defined with Terraform.

## Components

### DynamoDB Table

- Partition key: `userid` (String)
- Billing mode: PAY_PER_REQUEST
- Table name should use a consistent prefix to avoid naming collisions

### Lambda: CRUD Function

- **Runtime**: Python 3.10
- **Environment**: `USERS_TABLE` (DynamoDB table name)
- **Permissions**: DynamoDB GetItem, PutItem, DeleteItem, Scan on the Users table
- **Route dispatch**: uses `httpMethod` and `resource` from the API Gateway event

### Lambda: Authorizer

- **Runtime**: Python 3.10
- **Environment**: `USER_POOL_ID`, `APPLICATION_CLIENT_ID`, `ADMIN_GROUP_NAME`
- **Type**: Token authorizer (reads `Authorization` header)
- **Caching**: JWKS public keys cached at module level (outside handler)

### API Gateway

- REST API defined with OpenAPI 3.0 body
- Stage name: `Prod`
- All endpoints use a Lambda token authorizer security scheme

#### Endpoints

| Method | Path | Integration |
|--------|------|-------------|
| GET | `/users` | Lambda proxy (CRUD function) |
| POST | `/users` | Lambda proxy (CRUD function) |
| GET | `/users/{userid}` | Lambda proxy (CRUD function) |
| PUT | `/users/{userid}` | Lambda proxy (CRUD function) |
| DELETE | `/users/{userid}` | Lambda proxy (CRUD function) |

### Cognito

- User Pool with email as username attribute
- User Pool Client with `ALLOW_USER_PASSWORD_AUTH`, `ALLOW_USER_SRP_AUTH`,
  `ALLOW_REFRESH_TOKEN_AUTH`
- Admin group for role-based access

## Data Flow: Create User

```
1. Client → POST /users  (Authorization: Bearer <token>)
2. API Gateway → Lambda Authorizer (validate JWT)
3. Authorizer → Cognito JWKS endpoint (cold start only)
4. Authorizer → API Gateway (Allow policy)
5. API Gateway → Lambda CRUD (event with httpMethod=POST, resource=/users)
6. Lambda CRUD → DynamoDB PutItem (generates uuid, adds timestamp)
7. Lambda CRUD → API Gateway (200 + created user JSON)
8. API Gateway → Client (200 response)
```

specs/users-service/tasks.md
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
# Tasks: Serverless Users Service

## Task 1: Infrastructure Foundation

- [ ] 1.1 Create Terraform provider configuration and data sources for region and account ID
- [ ] 1.2 Define variables for resource naming prefix, Lambda runtime, timeout, and memory
- [ ] 1.3 Create DynamoDB table resource (PAY_PER_REQUEST, `userid` partition key)
- [ ] 1.4 Run `terraform init` and `terraform apply` to create the DynamoDB table
- [ ] 1.5 Verify the table exists using the AWS CLI

## Task 2: Business Logic (CRUD Lambda)

- [ ] 2.1 Create the Lambda function source with route-based CRUD handler
        (GET/POST /users, GET/PUT/DELETE /users/{userid})
- [ ] 2.2 Create an IAM role with DynamoDB access policy for the Lambda
- [ ] 2.3 Create the Terraform resources for packaging and deploying the Lambda
- [ ] 2.4 Run `terraform apply` and verify the Lambda appears in AWS
- [ ] 2.5 Test the Lambda manually with a test event

## Task 3: API Gateway

- [ ] 3.1 Create REST API using OpenAPI 3.0 body with all five endpoints
- [ ] 3.2 Add deployment, stage, and Lambda invoke permission
- [ ] 3.3 Add CloudWatch logging for access logs
- [ ] 3.4 Run `terraform apply` and note the API endpoint URL
- [ ] 3.5 Test with `curl` (expect 403, authorizer not yet configured)

## Task 4: Authentication

- [ ] 4.1 Create Cognito User Pool, Client, Domain, and admin group
- [ ] 4.2 Create the Lambda authorizer function with JWT validation against Cognito JWKS
- [ ] 4.3 Create IAM role and Terraform resources for the authorizer Lambda
- [ ] 4.4 Update API Gateway to wire the authorizer security scheme
- [ ] 4.5 Run `terraform apply` and verify all resources deploy successfully

## Task 5: End-to-End Verification

- [ ] 5.1 Create a test user in Cognito and retrieve a JWT token
- [ ] 5.2 Call `GET /users` with the token (expect 200 and empty list)
- [ ] 5.3 Call `POST /users` to create a user (expect 200 and the created record)
- [ ] 5.4 Call `GET /users/{userid}` to retrieve the user (expect 200)
- [ ] 5.5 Call `PUT /users/{userid}` to update the user (expect 200)
- [ ] 5.6 Call `DELETE /users/{userid}` to delete the user (expect 200)

## Task 6: Unit Tests

- [ ] 6.1 Create test directory structure
- [ ] 6.2 Write unit tests for CRUD Lambda using `moto` for DynamoDB mocking
- [ ] 6.3 Run `pytest tests/unit/` and verify all tests pass

Review Your Specs
Whichever approach you used, review the spec files before handing them to Claude Code. Check that:

Requirements:

Are acceptance criteria specific and testable?
Does scope match the MVP (nothing more, nothing less)?
Are there any contradictions between requirements?
Design:

Does the architecture match the tech stack in CLAUDE.md?
Are all requirements addressable with this design?
Is the data model correct (partition key, billing mode)?
Tasks:

Are tasks ordered with dependencies respected?
Is each task concrete enough for Claude Code to action?
Is there a verification step after each infrastructure change?
AI-generated specs require human review
Whether you wrote specs by hand or had Claude Code draft them, you are responsible for what they say. Spend five minutes reviewing now; it saves debugging time later.

Your spec files are ready. Claude Code has everything it needs to implement the Users Service.
Next, you will hand the specs to Claude Code and watch it build the application.



2 - Implement with Claude Code
Your CLAUDE.md and spec files are in place. Now it is time to hand the work to Claude Code and watch it build the Users Service step by step.

Start a Claude Code session
From your project root:

cd ~/workspace/my-workspace
claude

Claude Code reads CLAUDE.md automatically. You are ready to start.

Tip: You can use the @ prefix to reference specific files when talking to Claude Code. For example, @specs/users-service/requirements.md tells Claude Code to read that file as context for your request, without you having to paste its contents.

Run the implementation
Give Claude Code the following instruction:

Read the spec files in specs/users-service/ and implement the Users Service
according to those specs. Work through the tasks in tasks.md in order.
As you complete each subtask, update tasks.md to check off the checkbox
(change `- [ ]` to `- [x]`). Start with Task 1 (infrastructure foundation)
and wait for my approval before moving to the next task group.

By checking off tasks in the spec file itself, you create a persistent record of what has been completed. If you need to stop your Claude Code session and resume later (or if Claude Code loses context), the checked boxes in tasks.md tell it exactly where to pick up. The specs double as a live progress tracker.

Claude Code will propose each file creation and command execution. Read each proposal before approving. This is how you stay in control and how you learn what Claude Code is doing. If something does not look right, type no and explain what you want instead.

Resuming after a break
This module takes 60-90 minutes. If you need to stop and come back later, run /rename to give your session a memorable name (e.g., users-service-mvp), then exit. When you return, run claude --resume to pick up from where you left off. Alternatively, start a fresh session and say:

Read specs/users-service/tasks.md and continue implementing from where I left off. The checked boxes show what is already done.

Claude Code will read the checked/unchecked boxes and pick up at the next incomplete task.

Task 1: Infrastructure Foundation
Claude Code will create main.tf, variables.tf, and ddb.tf, then run:

terraform init
terraform apply

Before approving terraform apply, glance at variables.tf. It sets a hardcoded base name for all resources. What happens if you deploy two copies of this stack in the same account? Resource names would collide. In a real project, you would parameterize this with a workspace or environment prefix. For this workshop, the default value is fine.

After terraform apply completes, ask Claude Code to verify:

Verify the DynamoDB table was created successfully using the AWS CLI.

DynamoDB table deployed. You have working infrastructure.
While you wait for Terraform to apply: DynamoDB is a key-value and document store. Every item must have a partition key (in this case userid). DynamoDB uses the partition key to distribute data across storage nodes. Since userid is unique per user, each item gets its own node.

PAY_PER_REQUEST billing means you pay per read/write operation rather than reserving capacity upfront. For a workshop API with unpredictable traffic, this is ideal. You would switch to PROVISIONED capacity only when you have predictable, high-volume traffic and want cost predictability.

Task 2: Business Logic
Ask Claude Code to continue:

Implement Task 2: create the CRUD Lambda function and its IAM role, then deploy.
Check off each subtask in tasks.md as you complete it.

Claude Code will create src/users/lambda_function.py, src/users/requirements.txt, lambda-iam.tf, and lambda.tf.

Sub-agents: Claude Code's parallel workers
As Claude Code implements Task 2, watch the tool calls closely. When it needs to create multiple independent files (the Lambda source, the IAM role, the Terraform resource), it may spawn sub-agents, specialized workers that each run in their own context window and report results back. You will see several file-creation or research actions appear almost simultaneously rather than one at a time.

You can nudge Claude Code to use sub-agents explicitly. Try a prompt like:

Research the Lambda function, IAM role, and Terraform packaging in parallel using separate subagents, then implement each.

Sub-agents are most effective when the subtasks are independent: they cannot talk to each other, so each one needs a self-contained piece of work. Creating the Lambda source code and defining its IAM role are good examples: neither depends on the other, so they can run in parallel.

CORS wildcard is a workshop shortcut
The reference code returns Access-Control-Allow-Origin: * on every response. This allows any website to call your API from a browser. Convenient for local testing, but never appropriate for production. In a real API you would restrict origins to your known frontend domains (e.g., https://app.example.com). For this workshop, the wildcard is intentional.

Reference: src/users/lambda_function.py
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
import json
import uuid
import os
import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

USERS_TABLE = os.getenv('USERS_TABLE', None)
dynamodb = boto3.resource('dynamodb')
ddbTable = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    route_key = f"{event['httpMethod']} {event['resource']}"

    response_body = {'Message': 'Unsupported route'}
    status_code = 400
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }

    try:
        if route_key == 'GET /users':
            ddb_response = ddbTable.scan(Select='ALL_ATTRIBUTES')
            response_body = ddb_response['Items']
            status_code = 200

        elif route_key == 'GET /users/{userid}':
            ddb_response = ddbTable.get_item(
                Key={'userid': event['pathParameters']['userid']}
            )
            response_body = ddb_response.get('Item', {})
            status_code = 200

        elif route_key == 'DELETE /users/{userid}':
            ddbTable.delete_item(
                Key={'userid': event['pathParameters']['userid']}
            )
            response_body = {}
            status_code = 200

        elif route_key == 'POST /users':
            request_json = json.loads(event['body'])
            request_json['timestamp'] = datetime.now().isoformat()
            if 'userid' not in request_json:
                request_json['userid'] = str(uuid.uuid1())
            ddbTable.put_item(Item=request_json)
            response_body = request_json
            status_code = 200

        elif route_key == 'PUT /users/{userid}':
            request_json = json.loads(event['body'])
            request_json['timestamp'] = datetime.now().isoformat()
            request_json['userid'] = event['pathParameters']['userid']
            ddbTable.put_item(Item=request_json)
            response_body = request_json
            status_code = 200

    except Exception as e:
        logger.exception("Unhandled exception")
        status_code = 500
        response_body = {'Error': str(e)}

    return {
        'statusCode': status_code,
        'body': json.dumps(response_body),
        'headers': headers
    }

After deploy, test the Lambda directly:

Test the Lambda function with a GET /users event using the AWS CLI and show me the output.

While Lambda deploys: the first time a Lambda function is invoked (or after a period of inactivity), AWS must provision a container, load your code, and run your initialization code outside lambda_handler. This is called a cold start and adds 100-500 ms of latency. Subsequent invocations reuse the same container (warm invocations) and are much faster. This is why the Lambda authorizer you will build later caches the Cognito JWKS public keys at module level (outside lambda_handler): the keys only need to be fetched on cold start.

Lambda function deployed. CRUD operations are working.
If your Claude Code session starts feeling sluggish or it forgets earlier decisions, run /compact to summarize the conversation and free up context. Run /context to check how much of the context window is in use.

Task 3: API Gateway
Implement Task 3: create the API Gateway REST API with all five endpoints, deploy it,
and give me the invoke URL. Check off each subtask in tasks.md as you complete it.

Claude Code creates api-gateway.tf with the OpenAPI 3.0 body and deploys. After terraform apply, test the endpoint (without auth yet):

Call GET /users on the new API endpoint and show me the response.

Expected result: HTTP 403. The Lambda authorizer security scheme is attached but the authorizer Lambda does not exist yet. This is intentional.

Expected error: 403 Forbidden
You will see a 403 response at this point. Why did we lead you here deliberately?

The API Gateway OpenAPI definition references the lambdaTokenAuthorizer security scheme on every endpoint. When the stage deploys without the authorizer Lambda, API Gateway cannot invoke it and refuses all requests with 403. This is the system working correctly: it is enforcing the security policy even before the authorizer exists.

Compare this to a system without a security policy: it would return 200 to anyone. By designing authentication into the API definition from the start, you guarantee that no endpoint can be accidentally left unprotected. You will wire up the authorizer Lambda in the next task.

If Claude Code ever produces something unexpected (a wrong file, a broken Terraform config, or an unwanted change), run /rewind to step back through recent actions and selectively undo them.

Task 4: Authentication
Task 4 is the most architecturally complex step: Cognito, a Lambda authorizer, IAM roles, and API Gateway updates all need to work together. This is a good moment to ask Claude Code to think harder about the problem before it starts writing code.

Extended thinking and effort levels
Claude Code uses extended thinking to reason through complex problems before acting. You can see this reasoning by pressing Ctrl+O to toggle verbose mode. Claude Code's thinking appears as gray italic text above its response. Watch it work through questions like: "Which Cognito auth flows does the spec require?", "How should the authorizer Lambda get the User Pool ID?", and "What order should I create these resources to avoid Terraform dependency cycles?"

You can control how deeply Claude Code thinks using effort levels:

/effort low: fast, minimal reasoning, good for simple file edits
/effort medium: the default, balanced
/effort high: deeper reasoning for complex multi-file changes
/effort max: deepest reasoning with no token budget constraint (current session only)
For Task 4, try bumping the effort level before you send the prompt:

/effort high

You can also include the keyword ultrathink anywhere in a single prompt to set effort to high for that one turn without changing your session default. For example: "ultrathink, implement Task 4..."

Note that phrases like "think hard" or "think deeply" are treated as regular text and do not change the effort level. Use /effort or ultrathink for the actual effect.

Implement Task 4: create the Cognito User Pool, Lambda authorizer, and update the API
to use the authorizer. Deploy everything. Check off each subtask in tasks.md as you
complete it.

Claude Code creates cognito.tf, src/authorizer/, lambda-authorizer.tf, lambda-authorizer-iam.tf, and updates api-gateway.tf.

Reference: src/authorizer/lambda_function.py
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
import os
import json
import time
import urllib.request
import logging
from jose import jwk, jwt
from jose.utils import base64url_decode

logger = logging.getLogger()
logger.setLevel(logging.INFO)

is_cold_start = True
keys = {}
user_pool_id = os.getenv('USER_POOL_ID', None)
app_client_id = os.getenv('APPLICATION_CLIENT_ID', None)
admin_group_name = os.getenv('ADMIN_GROUP_NAME', None)


def validate_token(token, region):
    global keys, is_cold_start, user_pool_id, app_client_id
    if is_cold_start:
        keys_url = (
            f'https://cognito-idp.{region}.amazonaws.com/'
            f'{user_pool_id}/.well-known/jwks.json'
        )
        with urllib.request.urlopen(keys_url) as f:
            response = f.read()
        keys = json.loads(response.decode('utf-8'))['keys']
        is_cold_start = False

    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        logger.error('Public key not found in jwks.json')
        return False

    public_key = jwk.construct(keys[key_index])
    message, encoded_signature = str(token).rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not public_key.verify(message.encode('utf8'), decoded_signature):
        logger.error('Signature verification failed')
        return False

    claims = jwt.get_unverified_claims(token)
    if time.time() > claims['exp']:
        logger.error('Token is expired')
        return False
    if claims['aud'] != app_client_id:
        logger.error('Token was not issued for this audience')
        return False
    return claims


def lambda_handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    token = event['authorizationToken']
    region = context.invoked_function_arn.split(':')[3]

    claims = validate_token(token, region)
    if not claims:
        raise Exception('Unauthorized')

    policy = {
        'principalId': claims.get('sub', 'user'),
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Allow',
                'Resource': event['methodArn']
            }]
        },
        'context': {
            'username': claims.get('email', ''),
            'groups': claims.get('cognito:groups', '')
        }
    }
    return policy

JWT signature verification is required in production
The authorizer above validates the JWT signature using Cognito's JWKS endpoint. Never disable signature verification in production code. An unverified JWT is just a JSON document that anyone can forge. The signature is what proves it was issued by your Cognito User Pool. The verify_signature: False pattern sometimes seen in examples is only appropriate for local testing of token claims, never in a deployed authorizer.

After terraform apply completes, verify the new resources:

Verify that the Cognito User Pool, Lambda authorizer, and updated API Gateway all deployed
successfully. Show me the Cognito User Pool ID and the authorizer function name.

All authentication resources deployed. The Users Service is secured with Cognito JWT authentication.
Task 5: End-to-End Verification
Ask Claude Code to run the full verification:

Complete Task 5: create a test user in Cognito, retrieve a JWT token, and run all
five API tests (list, create, get, update, delete). Check off each subtask in
tasks.md as you complete it.

Claude Code will run the AWS CLI commands for you. Expected output:

GET /users → [] (empty list)
POST /users → {"userid": "...", "name": "...", "timestamp": "..."}
GET /users/{userid} → the created record
PUT /users/{userid} → updated record
DELETE /users/{userid} → {}
End-to-end authentication is working. The Users Service is fully deployed.
Task 6: Unit Tests
Implement Task 6: write unit tests for the CRUD Lambda using moto for DynamoDB mocking,
then run pytest and show me the results. Check off each subtask in tasks.md as you
complete it.

Claude Code writes the tests and runs them. A passing test suite looks like:

tests/unit/test_users.py::test_create_user PASSED
tests/unit/test_users.py::test_get_user PASSED
tests/unit/test_users.py::test_list_users PASSED
tests/unit/test_users.py::test_update_user PASSED
tests/unit/test_users.py::test_delete_user PASSED

5 passed in 1.23s
If any test fails, share the error output with Claude Code and ask it to fix the test.

Unit tests are passing. You have a tested, deployed serverless application.
Configure the test command
Now that you have a passing test suite, configure Claude Code to run it automatically with a single slash command. In your Claude Code session, type:

/test pytest tests/unit/

This registers pytest tests/unit/ as the project's test command. From now on, whenever you type /test, Claude Code runs the full test suite, reads the output, and if any test fails, automatically attempts to fix the failing code and re-run the tests until they pass. You do not need to copy-paste error messages or explain what went wrong.

You will see this in action in the next section when you add the customer search feature. Each time Claude Code modifies the Lambda function or adds a new test, you can run /test to verify nothing is broken, or ask Claude Code to run /test after each change.

The /test command closes the feedback loop between specs and implementation. Your specs define the expected behavior, your tests encode that behavior as assertions, and /test gives Claude Code a one-command way to verify its work against those assertions. When Claude Code knows the test command, it can self-correct without your intervention. You stay focused on reviewing the what, not debugging the how.

Review what Claude Code built
Ask Claude Code to summarize what was created:

List all the files you created in this session and give me a one-line description of each.

You should see the full project structure from CLAUDE.md (all Terraform files, Lambda source code, and tests) created by Claude Code following your specs.

Commit the MVP
You have a working, tested application. This is the right time to commit. It gives you a clean checkpoint before you add new features or configure automation.

Claude Code can create commits for you. It reads the staged changes, understands the project context from CLAUDE.md, and writes a descriptive commit message. Try it:

/commit

Claude Code will:

Run git status and git diff to understand what changed
Stage the relevant files (it will not stage .terraform/ or state files thanks to your .gitignore)
Draft a commit message summarizing the MVP: infrastructure, Lambda functions, API Gateway, Cognito auth, and unit tests
Ask you to approve before creating the commit
Review the proposed commit message. If you want to adjust it, tell Claude Code what to change. Once you approve, the commit is created locally.

Committing the MVP before starting the customer search feature gives you a clean rollback point. If anything goes wrong during the next feature, you can git diff to see exactly what changed, or git checkout . to reset to the last known good state. Claude Code makes this frictionless. You do not need to leave your session or think about what to stage.

Keep the README current with a hook
You just asked Claude Code to list what it built. That is useful now, but the list goes stale the moment you add the next feature. What if Claude Code updated the project README automatically every time it finished a piece of work?

Claude Code hooks let you run actions at specific points during a session. A hook can be a shell command, an HTTP call, or (most powerfully) an agent prompt that spawns a sub-agent with full access to your project. You will create a Stop hook: it fires every time Claude Code finishes responding, and the agent sub-task will review recent changes and update the README.

Create the hook configuration
Create the project-level settings file:

mkdir -p .claude

Add the following to .claude/settings.json (create the file if it does not exist). If the file already exists with other settings, merge the hooks key into it:

.claude/settings.json
1
2
3
4
5
6
7
8
9
10
11
12
13
14
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Check if any new files were created or significant changes were made during this conversation. If so, update README.md to reflect the current project structure, components, and how to deploy and test the application. If README.md does not exist, create it. Keep the README concise: project title, one-paragraph description, directory structure, deploy instructions, and test instructions. Do not add content that is not supported by actual files in the project."
          }
        ]
      }
    ]
  }
}

How it works
The Stop event fires every time Claude Code finishes a response. Because the hook type is agent, Claude Code spawns a sub-agent that:

Reads the current project files to understand what exists
Compares against the existing README (or notes its absence)
Updates or creates README.md with accurate, current content
You do not need to remember to update documentation. The hook handles it after every meaningful interaction. If Claude Code only answered a question and made no file changes, the agent will see that nothing changed and leave the README alone.

The agent type is the most powerful hook. It gives a sub-agent full tool access to read, write, and run commands. Claude Code also supports simpler hook types: command runs a shell command (e.g., a linter or notification), and prompt evaluates a prompt with an LLM but without tool access (good for validation checks). You configure hooks in .claude/settings.json (shared with the team) or .claude/settings.local.json (personal). Type /hooks in Claude Code to see all active hooks for your session.

Hook performance
Agent hooks spawn a full sub-agent, which adds time and token cost to every stop event. For a workshop this is fine and educational. In a production workflow, consider whether a simpler command hook (e.g., a script that checks git diff --name-only and only triggers the agent when specific files changed) would be more efficient.

See it in action
The hook is already active. In the next section, when Claude Code finishes implementing the customer search feature, check your README.md. It will be updated automatically with the new endpoint and GSI documentation, without you asking.

Adding Features Post-MVP
Create separate specs for each new feature rather than one monolithic spec for the entire application. When you are ready to add the Customer Search feature, create a new spec:

specs/
├── users-service/      # Initial MVP (done)
└── customer-search/    # New feature spec
    ├── requirements.md
    ├── design.md
    └── tasks.md
Additional Resources
Claude Code: CLAUDE.md documentation 
Claude Code: Agentic loop documentation 
Terraform AWS Provider documentation 
AWS DynamoDB Developer Guide 
AWS Cognito Developer Guide 
Next, we will add a search feature to the existing platform using a new spec.

Feature: Customer Search
This section walks through adding a new feature, customer search, to the existing Users Service using a new spec. This demonstrates the recommended pattern for incremental development: one spec per feature, building on top of the deployed MVP.

Prerequisites
MVP deployed and working (all six tasks from the previous section completed)
Existing codebase with DynamoDB, Lambda, API Gateway, and Cognito
The Feature
Your Users Service MVP supports full CRUD operations, but every lookup requires knowing the user's userid (a UUID that is not human-friendly). In practice, support agents and internal tools need to find users by something they actually know: an email address.

The customer search feature adds a single new endpoint, GET /users/search?email=<value>, that returns all user records matching a given email address. The endpoint must:

Return matching users as a JSON list (or an empty list if none match)
Return HTTP 400 if the email query parameter is missing
Be protected by the same JWT authentication as the rest of the API
Query efficiently without scanning the entire table
This last point is the interesting design constraint. DynamoDB can only query by partition key (userid) natively. To search by email, you need a Global Secondary Index (GSI), essentially a second copy of the data organized by a different key. The GSI is the only new infrastructure resource; everything else is a modification to existing code.

What You Will Add
Change	File(s)	Why
DynamoDB GSI on email	ddb.tf	Enables efficient query-by-email without full table scans
Search route handler	src/users/lambda_function.py	New GET /users/search route that queries the GSI
API Gateway endpoint	api-gateway.tf	Exposes /users/search through the REST API
Unit tests	tests/unit/test_users.py	Covers search success, missing parameter, and empty results
Create the Feature Spec
Create a new spec directory alongside the MVP spec:

mkdir -p specs/customer-search

The key difference from the MVP spec is scope. Your MVP spec defined an entire system from scratch: every component, every resource, every connection. A feature spec is narrower: it builds on the existing codebase and describes only what changes. It does not recreate the architecture or redefine existing resources. It adds a GSI, modifies a Lambda handler, and extends an API definition. Everything else stays untouched.

Write the Feature Spec
Use the same approach you used for the MVP spec. If you wrote specs by hand before, try it again here: the feature is small enough that you can draft all three files in a few minutes. Think about what the requirements are (search by email, error cases), what changes to existing infrastructure (GSI, new route, new API path), and what order to implement them.

Alternatively, ask Claude Code to draft the spec for you using plan mode, or copy the reference files below directly.

specs/customer-search/requirements.md
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
# Requirements: Customer Search Feature

## Context

Extending the existing Users Service (MVP) to support searching for users by email
address. The existing DynamoDB table, Lambda function, and API Gateway are already deployed.

## User Stories

### Requirement 1: Search by Email

**User Story:** As an API consumer, I want to search for users by email address so that
I can find a specific user without knowing their `userid`.

#### Acceptance Criteria

1. WHEN a GET request is sent to `/users/search?email=<value>`, THE System SHALL return
   all user records whose `email` field matches the provided value
2. WHEN no users match the search query, THE System SHALL return an empty list with HTTP 200
3. WHEN the `email` query parameter is missing, THE System SHALL return HTTP 400
4. THE search endpoint SHALL require the same JWT authentication as all other endpoints
5. THE search SHALL use a DynamoDB GSI (not a full table scan) for efficiency

specs/customer-search/design.md
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
# Design: Customer Search Feature

## Changes to Existing Resources

### DynamoDB Table (modify `ddb.tf`)

Add a Global Secondary Index on the `email` attribute:

| Property | Value |
|----------|-------|
| Index name | `email-index` |
| Partition key | `email` (String) |
| Projection type | ALL |
| Billing | inherited from table (PAY_PER_REQUEST) |

**Note:** CloudFormation/Terraform can add one GSI per apply. Adding the GSI is a
non-destructive table modification; existing data is preserved.

### Lambda CRUD Function (modify `src/users/lambda_function.py`)

Add a new route handler for `GET /users/search`:

```python
elif route_key == 'GET /users/search':
    email = event.get('queryStringParameters', {}).get('email')
    if not email:
        response_body = {'Message': 'email query parameter is required'}
        status_code = 400
    else:
        ddb_response = ddbTable.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email)
        )
        response_body = ddb_response['Items']
        status_code = 200
```

### API Gateway (modify `api-gateway.tf`)

Add new path `/users/search` with GET method:

```hcl
"/users/search" = {
  get = {
    security = [{ "lambdaTokenAuthorizer": [] }]
    x-amazon-apigateway-integration = {
      httpMethod = "POST"
      type       = "aws_proxy"
      uri        = "...userfunctions_lambda.arn/invocations"
    }
  }
}
```

**Important:** The `/users/search` path must be defined *before* `/users/{userid}` in the
OpenAPI body, otherwise API Gateway may route `GET /users/search` to the `{userid}`
wildcard instead of the literal `search` path.

specs/customer-search/tasks.md
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
# Tasks: Customer Search Feature

## Task 1: DynamoDB GSI

- [ ] 1.1 Update `ddb.tf` to add a GSI on the `email` attribute (index name: `email-index`)
- [ ] 1.2 Run `terraform apply` to add the GSI to the existing table
- [ ] 1.3 Verify the GSI appears in the DynamoDB console as ACTIVE

## Task 2: Search Handler

- [ ] 2.1 Update `src/users/lambda_function.py` to add the `GET /users/search` route
- [ ] 2.2 Add `boto3.dynamodb.conditions.Key` import for the query expression
- [ ] 2.3 Run `terraform apply` to redeploy the Lambda with the updated code
- [ ] 2.4 Test the search endpoint directly with the AWS CLI

## Task 3: API Gateway Update

- [ ] 3.1 Add `/users/search` GET endpoint to the OpenAPI body in `api-gateway.tf`
        (place it before the `/users/{userid}` path)
- [ ] 3.2 Run `terraform apply` to redeploy the API stage
- [ ] 3.3 Test `GET /users/search?email=test@example.com` with a JWT token

## Task 4: Verification

- [ ] 4.1 Create a user with a known email address via `POST /users`
- [ ] 4.2 Search for the user via `GET /users/search?email=<the email>`
- [ ] 4.3 Verify the response contains the created user
- [ ] 4.4 Search for a non-existent email and verify empty list response
- [ ] 4.5 Update unit tests to cover the new search route

## Task 5: Unit Tests

- [ ] 5.1 Add `email-index` GSI definition to the moto mock table in test fixtures
- [ ] 5.2 Write test for successful email search
- [ ] 5.3 Write test for missing email parameter (expect 400)
- [ ] 5.4 Write test for no matching results (expect 200 + empty list)
- [ ] 5.5 Run `pytest tests/unit/` and verify all tests pass

Implement with Claude Code
With the feature spec in place, tell Claude Code to implement it:

Read specs/customer-search/ and implement the customer search feature on top of the
existing codebase. Work through the tasks in tasks.md in order, deploying after
each task group. Check off each subtask in tasks.md as you complete it.

Because Claude Code has already read your CLAUDE.md and knows the existing project structure, it understands the context without further explanation. It will make targeted changes to ddb.tf, lambda_function.py, and api-gateway.tf without touching anything else.

Use /test to validate as you go
You configured the /test command at the end of the MVP section. As Claude Code implements the search feature, run /test after each task group to verify that existing tests still pass and new tests work. If Claude Code breaks something, /test catches it immediately and Claude Code will fix the regression before moving on.

You can also ask Claude Code to run tests automatically as part of its workflow:

After each change to the Lambda function, run /test to make sure nothing is broken.

Specs make incremental development safe
Notice that the feature spec is entirely self-contained. It describes only what changes, not what to leave alone. Claude Code uses the spec to make precise, scoped modifications. Compare this to a vague prompt like "add email search to the API" which might cause Claude Code to make unnecessary changes to unrelated files.

Check your README
After Claude Code finishes implementing the search feature, open README.md. The Stop hook you configured in the previous section fired automatically and updated the README with the new /users/search endpoint and GSI documentation, without you asking. This is the hook doing its job: keeping project documentation in sync with the actual codebase as it evolves.

Additional Resources
DynamoDB: Working with Global Secondary Indexes 
API Gateway: Working with API resources 
Congratulations! You have built and extended a production-ready serverless Users Service using spec-driven development with Claude Code. When you are finished, proceed to the Clean up and next steps section to tear down the deployed AWS resources.
