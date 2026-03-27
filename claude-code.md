[Option 3] Development using Claude Code
Architecture diagram for a synchronous user microservice

Module Overview
Everyone needs to start somewhere! In this module, you will build a complete serverless Users Service from an empty directory using Claude Code, Anthropic's agentic coding tool that lives in your terminal.

Unlike traditional code-generation assistants that produce snippets for you to copy and paste, Claude Code is an agent. It reads your files, writes code directly into your project, and runs commands on your behalf. You describe what you want, review what it proposes, and approve each action. Think of it as pair-programming with a senior developer who never gets tired.

You will build the same synchronous, authenticated Users Service as the other workshop options (DynamoDB for storage, Lambda for compute, API Gateway for the front door, and Cognito for authentication), all defined with Terraform and deployed to your AWS account.

What is Claude Code?
Claude Code is Anthropic's agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. It is available in your terminal, VS Code, JetBrains IDEs, a standalone desktop app, and even the web browser. All of these connect to the same underlying engine.

Unlike traditional code-completion tools that suggest the next few lines, Claude Code is a full agent. It plans multi-step approaches, creates and edits files across your project, executes shell commands, and verifies the results, all within a single conversational session.

Core Capabilities
Agentic execution with human-in-the-loop. Claude Code operates on a propose-review-execute loop. It reads your project files and plans an approach, proposes an action (creating a file, editing code, or running a command), waits for you to review and approve, then executes and moves to the next step. Nothing happens without your explicit approval. You stay in full control while Claude Code does the heavy lifting.

Full project context. Claude Code reads your source files, understands your project structure, and makes changes that fit your existing codebase. It can trace how data flows through your application, understand relationships between components (e.g., Terraform resources referencing each other), make coordinated changes across many files at once, and identify the root cause of bugs by reading error messages and source code together.

CLAUDE.md: persistent project knowledge. A CLAUDE.md file in your project root gives Claude Code persistent context about your tech stack, coding standards, architecture decisions, and constraints. Claude Code reads this file at the start of every session. Similar to how Kiro uses steering documents (product.md, tech.md, structure.md), CLAUDE.md acts as your project's "institutional memory", ensuring consistent naming, conventions, and architectural decisions across all interactions.

Built-in tools. Claude Code comes with a set of tools that make it truly agentic. It can read files from your project, create new files or modify existing ones with precise edits, execute shell commands (build, deploy, test, AWS CLI), search for files by pattern or content, retrieve documentation from the web, and spawn parallel sub-agents for research or complex multi-step tasks. These tools are what separate Claude Code from a chat assistant. It doesn't just generate text; it takes real actions in your development environment.

Git integration. Claude Code works directly with Git. It can stage changes, write descriptive commit messages, create branches, and open pull requests. In CI/CD pipelines, it can automate code review, issue triage, and pull request creation via GitHub Actions or GitLab CI/CD.

Slash commands and custom skills. Built-in slash commands like /help, /compact, /clear, /cost, and /doctor give you quick access to common workflows. You can also create custom slash commands (called Skills) by adding SKILL.md files to your project's .claude/skills/ directory, packaging repeatable workflows your team can share, like /review-pr or /deploy-staging.

MCP (Model Context Protocol). The Model Context Protocol (MCP)  is an open standard for connecting AI tools to external data sources. With MCP, Claude Code can read design docs from Google Drive, update tickets in Jira, pull data from Slack, query documentation databases, or use your own custom tooling. MCP servers are configured in your project settings and extend Claude Code's capabilities beyond the built-in tools.

Multi-agent teams. For complex tasks, Claude Code can spawn multiple agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results. This enables parallel research and implementation, independent frontend/backend work, or concurrent test writing and code implementation.

CLI composability. Claude Code follows the Unix philosophy: it is composable and scriptable. You can pipe logs into it for analysis (tail -f app.log | claude -p "alert me if you see errors"), run it in non-interactive mode for automation (claude -p "review these files for security issues"), or chain it with other tools (git diff main --name-only | claude -p "review changed files").

Plan Mode: Think Before You Act
One of Claude Code's most powerful features is plan mode. When you toggle plan mode on (press Shift+Tab in the input area), Claude Code switches from executing actions to planning them. In plan mode, Claude Code explores your codebase, reads files, searches for patterns, and designs an approach. It will not create, edit, or run anything. You get a detailed plan that you can review, refine, and approve before a single file is touched.

This is especially valuable when:

Starting a new feature. Ask Claude Code to plan the implementation before writing code. You can catch architectural issues early.
Debugging complex problems. Let Claude Code investigate the codebase and form a hypothesis before making changes.
Understanding unfamiliar code. Use plan mode to explore and explain code without risking accidental modifications.
Toggle plan mode off (press Shift+Tab again) to return to the normal execution mode where Claude Code carries out the plan.

Plan mode in this workshop
We recommend using plan mode at the start of each major task in this workshop. Ask Claude Code to plan the approach first, review its plan, then switch back to execution mode and tell it to proceed. This mirrors a real-world workflow where you think before you code.

Essential Keyboard Shortcuts and Commands
Getting comfortable with these shortcuts and commands will make your Claude Code sessions much smoother:

Shortcut	What it does
Esc	Cancel the current generation or action. Claude Code stops immediately. Use this when it's heading in the wrong direction. You won't lose your conversation history.
Shift+Tab	Toggle plan mode on/off. Plan mode lets Claude Code research and plan without executing any changes.
Shift+Enter	Insert a new line in your prompt without sending it. Useful for writing multi-line instructions.
@filename	Reference a specific file in your prompt (e.g., @src/lambda_function.py). Claude Code focuses on that file instead of searching your entire project.
/compact	Compress the conversation history to free up context space. Use this when conversations get long and Claude Code starts losing track of earlier context.
/context	Show how much of Claude Code's context window is in use, broken down by category. Helps you decide when to run /compact.
/rewind	Step back through Claude Code's recent changes and selectively undo them. Useful when Claude Code takes a wrong turn and you want to restore previous file versions.
/clear	Clear the entire conversation and start fresh. Useful when switching to a completely different task.
/rename	Name your current session (e.g., /rename dynamodb-setup). Resume it later with claude --resume dynamodb-setup. Handy if you need to take a break mid-workshop.
/cost	Show how much the current session has cost in API usage. Good for keeping an eye on consumption.
/doctor	Run diagnostics to check your Claude Code installation and configuration.
Tips for Effective Prompting
Be specific about what you want. "Create a DynamoDB table" is fine for a quick prototype, but "Create a DynamoDB table named users with a partition key userId (String), enable point-in-time recovery, and add Name/Environment/Project tags" gives Claude Code the detail it needs to get it right the first time.

Break large tasks into smaller steps. Instead of "Build me a complete serverless API with authentication," work through it piece by piece: first the database, then the Lambda function, then the API Gateway, then auth. This gives you checkpoints to verify each component works before moving on.

Tell Claude Code to verify its work. After generating Terraform code, ask it to run terraform validate or terraform plan. After writing a Lambda function, ask it to run the tests. Claude Code can catch its own mistakes if you ask it to check.

Use CLAUDE.md to prevent recurring mistakes. If Claude Code keeps making the same error (wrong naming convention, missing tags, incorrect import paths), add a rule to CLAUDE.md. It reads this file at the start of every session and will follow those instructions going forward.

Start a new session for unrelated tasks. Claude Code's context window is finite. If you have finished deploying your DynamoDB table and are moving on to a completely different feature, consider running /clear or starting a fresh claude session. This gives Claude Code a clean slate with full context capacity.

Permission Modes: Staying in Control
When Claude Code proposes an action, you can:

Press Enter / y to approve and execute
Press n to reject the specific action
Type feedback to explain what you want changed before it executes
By default, Claude Code asks permission for every file edit and shell command. As you build trust during your session, you can relax this by allowing specific tool categories. But for this workshop, we recommend keeping the default "ask every time" mode. It helps you understand exactly what Claude Code is doing at each step.

Review before you approve
Always read what Claude Code proposes before pressing Enter. This is especially important for shell commands like terraform apply or terraform destroy that make real changes to your AWS account. The human-in-the-loop review is your safety net.

Services used in this module
Claude Code  - Anthropic's agentic coding tool for the terminal
AWS API Gateway  - the front door for applications; REST, HTTP, and WebSocket APIs
AWS Lambda  - compute service; functions in serverless runtimes
AWS Cognito  - identity store for user sign-up and sign-in
AWS DynamoDB  - a fully managed NoSQL key/value data store
Terraform  - infrastructure as code tool for provisioning AWS resources
What you will accomplish
By the end of this module, you will have:

Set up Claude Code with project context via CLAUDE.md
Created a DynamoDB table using Claude Code-generated Terraform code
Generated a Lambda function for full CRUD operations on users
Configured API Gateway with proper REST endpoints and CORS
Implemented Cognito authentication with a Lambda authorizer
Written and run unit tests with pytest and moto
Deployed everything using Terraform, with Claude Code running the commands for you
Estimated duration: 60-90 minutes

How this module works
Throughout this module, you will give Claude Code natural-language instructions. Since Claude Code is non-deterministic, its output may differ from the examples shown. Expandable "Reference Code" sections provide working code you can fall back on if you get stuck.

Let's get started by setting up your development environment and Claude Code!

Previous
Next

© 2008 - 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.


Development Environment Setup
Before you can start building, you need access to your development environment and Claude Code installed and ready to go.

VS Code Server
Important
If VS Code Server encounters issues while launching in your browser, try a different browser (Chrome, Firefox, Edge, Safari).

Navigate to the Event Outputs pane at the bottom of the Workshop Studio page.
Event Outputs

Click the URL 01CodeServerURL to open VS Code Server in a new browser tab.

In the Welcome to code-server dialog, paste the development environment password you copied earlier, and choose Submit.

VS Code Server Password

You should now see the VS Code IDE. To reclaim screen space, close any side panels. You will work primarily in the integrated terminal for this module.
VS Code IDE

Verify Claude Code Installation
Claude Code runs as a command-line tool that is already installed in your workshop environment. Open a terminal in VS Code (Terminal > New Terminal) and verify installation:

claude --version

You should see the Claude Code version number printed to the terminal.

If Claude Code is not installed, follow instructions below.

Claude Code installation instructions
Install Claude Code by running the following command in the terminal:

npm install -g @anthropic-ai/claude-code

Authentication
Claude Code requires an Anthropic API key. If you are at an AWS-hosted event, the key is pre-configured in your environment. If you are self-hosting, set your API key:

1
export ANTHROPIC_API_KEY=your-key-here

Start Claude Code
Launch Claude Code from the terminal:

cd ~/workspace/my-workspace
claude

You will see Claude Code's interactive prompt. This is where you will have a conversation to build your entire serverless application.

VS Code IDE with Claude Code

How Claude Code works
Claude Code operates in a conversational loop:

You type a request in natural language
Claude proposes actions (creating files, editing code, running commands)
You review and approve each action (or ask for changes)
Claude executes the approved action and moves to the next step
You stay in control at every step. Nothing happens without your approval.

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

Claude Code is installed and ready to go. Let's start building!
In the next section, you will set up your project structure and Terraform foundation with Claude Code doing the heavy lifting.



Getting started
Setting up resources for a new application can take a lot of time. Introductory tutorials typically show you how to configure resources in the web-based console. The web-based console is easy, but it will slow you down and lead to mistakes.

Important Note About Reference Code: Throughout this workshop, you will find expandable sections containing reference code examples. Since Claude Code's output is non-deterministic, your generated code may differ from these examples. These code snippets are provided as guidance. If you get stuck or your generated code doesn't work as expected, feel free to use these examples to continue with the workshop.
For production projects, you may need dozens or even hundreds of resources. You will need to provision infrastructure for many developers and environments, such as dev, stage, prod.

In this module, you will use scalable Infrastructure as Code (IaC) techniques with Claude Code to define, deploy, and test service resources and code.

Infrastructure as Code (IaC) applies the same rigor of application code development to provisioning infrastructure. Resources are defined declaratively, so the configuration can be stored in a source control system. Automated pipelines can then deploy both your application code and the necessary infrastructure resources.

We'll show you how to use Claude Code and Terraform to quickly build and deploy your application with an agentic AI-powered approach.

Project Structure Overview
By the end of this workshop, you will have built a complete serverless application with the following structure:

workshop/
├── src/                           # Source code
│   ├── users/                     # Users Lambda function
│   │   ├── lambda_function.py     # Main handler
│   │   ├── __init__.py
│   │   ├── requirements.txt
│   │   └── requirements-dev.txt
│   │
│   └── authorizer/                # Authorizer Lambda function
│       ├── lambda_authorizer.py   # Main handler
│       └── requirements.txt
│
├── tests/                         # Tests directory
│   ├── unit/                      # Unit tests
│   │   └── users/                 # Tests for users function
│   │       ├── test_app.py
│   │       └── conftest.py
│   │
│   └── integration/               # Integration tests
│
├── infrastructure/                # Infrastructure code directory
│   ├── main.tf                    # Main Terraform configuration
│   ├── api-gateway.tf             # API Gateway resources
│   ├── cognito.tf                 # Cognito user pool resources
│   ├── ddb.tf                     # DynamoDB resources
│   ├── lambda.tf                  # Lambda resources
│   ├── lambda-authorizer.tf       # Lambda authorizer resources
│   ├── provider.tf                # Provider configuration
│   ├── variables.tf               # Variables definition
│   └── terraform.tfstate          # Terraform state files
│
├── CLAUDE.md                      # Project context for Claude Code
└── README.md                      # Project overview
This structure follows best practices for serverless applications, with clear separation of concerns between application code, infrastructure definitions, and tests. Throughout this workshop, we will build this structure incrementally using Claude Code.

Important!!: Follow the above directory structure throughout this workshop. The commands and code examples assume this specific structure, and deviating from it may cause errors in later steps.
A modern approach to AWS IaC with Claude Code
Claude Code offers a uniquely agentic approach to infrastructure as code. Rather than generating a snippet and asking you to paste it into the right file, Claude Code creates the files directly, runs initialization commands, and validates the result, all within a single conversation.

This approach reduces the learning curve and helps you focus on your application's business logic rather than infrastructure details. Claude Code understands AWS best practices and can help you implement them automatically.

Infrastructure as Code (IAC) with Terraform

Create a CLAUDE.md for project context
Before we start generating code, let's give Claude Code persistent context about our project. A CLAUDE.md file acts like a steering document: it tells Claude Code about your tech stack, conventions, and constraints every time it starts a new session.

In your Claude Code session, type:

Create a CLAUDE.md file in the workshop directory with the following project context:
- This is a serverless Users Service built with Terraform and Python
- Infrastructure is in the infrastructure/ directory using Terraform (not SAM or CDK)
- Lambda functions are Python 3.10, located under src/
- Tests use pytest with moto for AWS mocking, located under tests/
- The base name for all resources is "workshop" (use the Terraform variable workshop_stack_base_name)
- AWS region is us-west-2
- Follow least-privilege IAM principles
- All Terraform resources should be tagged with Name, Environment ("Workshop"), and Project ("Serverless Patterns")

Claude Code will create the CLAUDE.md file directly in your project. This context will guide all subsequent code generation.

Why CLAUDE.md matters
Think of CLAUDE.md as the project's "institutional memory" for Claude Code. Every time you start a new session, Claude Code reads this file first. This means consistent naming, conventions, and architectural decisions across all your interactions, similar to how Kiro uses steering documents.

Create the project structure
Now let's have Claude Code set up the entire project scaffolding:

Create a serverless project structure for a project named "workshop" with:
1. Source code directory for Lambda functions (users and authorizer, using Python)
2. Test directories for unit and integration tests
3. Infrastructure directory for Terraform templates
4. Do not create modules directories or directories per environment

First show me the plan, then create just the directory structure without any files yet.

Claude Code will show you its plan and then create the directory structure. You will see it propose shell commands like mkdir -p. Review and approve them.

Create Terraform configuration files
Next, let's have Claude Code create the foundational Terraform files:

Under the infrastructure directory in the workshop project, create these Terraform files:
- provider.tf: AWS provider with region from a variable
- variables.tf: variables for "region" (default: us-west-2), "workshop_stack_base_name" (default: workshop), "environment" (default: Workshop), "project" (default: Serverless Patterns)
- outputs.tf: empty file for future outputs
- versions.tf: minimum Terraform version 1.0.0, do not include required_providers
- README.md with project description

Claude Code will create each file directly (no copy-pasting required). Review the content it proposes for each file before approving.

Reference Code - provider.tf
1
2
3
provider "aws" {
  region = var.region
}

Reference Code - variables.tf
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
variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-2"
}

variable "workshop_stack_base_name" {
  description = "Base name for workshop resources"
  type        = string
  default     = "workshop"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "Workshop"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "Serverless Patterns"
}

Reference Code - versions.tf
1
2
3
terraform {
  required_version = ">= 1.0.0"
}

Reference - project structure
The resulting structure for the workshop/infrastructure folder should look similar to the following:

.
├── README.md
├── outputs.tf
├── provider.tf
├── variables.tf
└── versions.tf
Initialize Terraform
Now ask Claude Code to initialize Terraform:

Initialize Terraform in the infrastructure directory. Run terraform init.

Claude Code will propose running terraform init. Approve it and watch the providers download. This is where the agentic approach shines: Claude Code runs the command, reads the output, and can immediately troubleshoot if something goes wrong.

Troubleshooting with Claude Code
If you encounter any issues during setup, just describe the problem naturally:

I'm getting an error 'Error: No valid credential sources found'. How do I configure AWS credentials for Terraform?

Claude Code will analyze the error, check your environment, and suggest fixes, potentially even running diagnostic commands to help pinpoint the issue.

Claude Code vs. traditional code assistants
Notice how different this is from copy-pasting code snippets. Claude Code created files, ran commands, and is ready to debug, all within the same conversation. You stay focused on what you want to build, not how to type it out. Similar to a traditional web framework scaffolding tool, but powered by AI and infinitely more flexible.

Your project is set up and Terraform is initialized. You are ready to move on to building your serverless application with Claude Code!



1 - Create data store
Your application needs a place to store user data. For that, you'll create a Users table in Amazon DynamoDB.

module architecture diagram highlighting DynamoDB

You will use Claude Code to generate Terraform code for creating the DynamoDB table resource. Because Claude Code is agentic, it will create the file directly in your project and can immediately deploy it with Terraform.

With Claude Code, you describe what you want in plain English and it writes the infrastructure code, creates the files, and can even run the deployment, all within the same conversation.
Plan the table design with Claude Code
If you already know exactly what you want (partition key, billing mode, encryption settings), you can skip straight to the next section and give Claude Code a detailed prompt. It will happily generate the Terraform in one shot.

But if you are still figuring out the design, or you want Claude Code to help you think through the trade-offs, plan mode is a powerful alternative. It lets you have a design conversation before any code is written, and the decisions you reach become the basis for a precise implementation prompt.

Toggle plan mode on by pressing Shift+Tab. You will see the mode indicator change at the bottom of the prompt. In plan mode, Claude Code will research and reason but will not create or edit any files.

Ask Claude Code to help you design the table:

I need a DynamoDB table to store user records for a REST API that supports CRUD operations. Each user will have fields like userid, first name, last name, and email.

Help me think through the table design: what should the partition key be, do I need a sort key, what billing mode makes sense for a workshop/dev workload, and what security features should I enable?

Claude Code will analyze your requirements and come back with questions and recommendations. This is one of its most useful behaviors: instead of blindly generating code, it engages in a design discussion. You might see it ask questions like:

"Do you need to query users by email or name, or only by user ID?" This determines whether you need Global Secondary Indexes (GSIs).
"What's your expected traffic pattern: steady or spiky?" This helps choose between provisioned and on-demand billing.
"Do you need point-in-time recovery for this environment?" This is a cost/safety trade-off.
Answer Claude Code's questions. For this workshop, here are the design decisions to guide the conversation:

Partition key: userid (string), since each user has a unique ID and all queries go through it
Sort key: not needed, because we are doing simple key-value lookups, not range queries
Billing mode: PAY_PER_REQUEST (on-demand), perfect for unpredictable workshop traffic with no capacity planning
Security: enable server-side encryption and point-in-time recovery
No GSIs needed, since we will only look up users by their ID
Why plan mode matters
Notice what just happened. Instead of jumping straight to code, you had a conversation about design. Claude Code helped you consider partition key choice, billing trade-offs, and security features. In a real project, this two-minute conversation can prevent costly redesigns later. This is especially true with DynamoDB, where changing the key schema means recreating the table.

Once you are satisfied with the design, toggle plan mode off by pressing Shift+Tab again. You are now back in execution mode, ready to generate code.
Define a Users table with Claude Code
You now have a clear picture of what you need: a single-table design with userid as the partition key, on-demand billing, encryption at rest, and point-in-time recovery. The next step is to translate those design decisions into a precise prompt. Notice how each bullet below maps directly to a decision you just made in plan mode. This is the payoff of planning first:

Create a DynamoDB table in Terraform with the following specifications:
- Resource name: users_table
- Table name: Use the workshop_stack_base_name variable as prefix followed by '_users'
- Billing mode: PAY_PER_REQUEST (on-demand capacity)
- Primary key: userid (string type)
- Add point-in-time recovery
- Add server-side encryption
- Add appropriate tags including Name, Environment, and Project
- Create an output for the table ARN, ID, and name
- Save the configuration in a file called "ddb.tf" in the infrastructure directory

Claude Code will create the ddb.tf file directly and update outputs.tf with the DynamoDB outputs. Review the proposed file contents before approving.

Once Claude Code creates the file, ask it to explain the security considerations:

Show me the content of ddb.tf and explain any security considerations or potential cost implications.

Claude Code will read the file it just created and provide a detailed explanation. No need to switch tools or windows.

Reference Code - ddb.tf
The generated ddb.tf file should look similar to this:

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
# DynamoDB table for Users
resource "aws_dynamodb_table" "users_table" {
  name         = "${var.workshop_stack_base_name}_users"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "userid"

  attribute {
    name = "userid"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}_Users"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

# Output the DynamoDB table details
output "users_table_arn" {
  description = "DynamoDB Users table ARN"
  value       = aws_dynamodb_table.users_table.arn
}

output "users_table_id" {
  description = "DynamoDB Users table ID"
  value       = aws_dynamodb_table.users_table.id
}

output "users_table_name" {
  description = "DynamoDB Users table name"
  value       = aws_dynamodb_table.users_table.name
}

Terraform Code Detective Challenge
Let's play a game! As a Terraform Code Detective, your mission is to analyze the generated DynamoDB table configuration and identify key security and performance features. This will help you understand the code better and prepare you for real-world infrastructure development.

Detective Challenge Instructions
Study the Terraform code above and identify at least 3 security features that make this DynamoDB table configuration secure.

Find at least 2 performance-related configurations in the code.

Identify at least 2 cost implications of this configuration.

Ask Claude Code to verify your findings:

I've identified these security features in my DynamoDB Terraform code:
[List your findings]

And these performance/cost considerations:
[List your findings]

Am I correct? What did I miss? Are there any other important aspects I should understand?

Solution Checklist
Click to reveal the answers
Security Features:

Server-side encryption protects data at rest
Point-in-time recovery enables backup capabilities
Variable-based naming prevents hardcoding
Performance and Cost:

PAY_PER_REQUEST scales automatically but costs more with high traffic
Point-in-time recovery adds ~20% to base cost
Hash key enables efficient data retrieval
Ask Claude Code to explain the Terraform code!
You can ask Claude Code to explain any part of the generated code:

Explain the DynamoDB table configuration in ddb.tf, focusing on point-in-time recovery, server-side encryption, and the benefits of these features for a production environment.
Because Claude Code can read your actual files, it will explain your code, not a generic example.

Deploy the DynamoDB table
Now let's have Claude Code deploy the table. This is where the agentic workflow really shines: you don't need to switch to another terminal or remember Terraform commands.

Deploy the DynamoDB table by running terraform init, plan, and apply in the infrastructure directory. Show me the plan before applying.

Claude Code will run each command in sequence, show you the plan output, and wait for your approval before applying. If something goes wrong, it can immediately diagnose the issue.

Alternatively, for a quicker deployment:

Run terraform apply with auto-approve in the infrastructure directory.

Deploy Checkpoint
Deployed!
After the deploy finishes, verify with the console that the database table was created.
After the deploy finishes, go to the DynamoDB console  (make sure your chosen region is selected) and verify that workshop_users is in the tables list.

Ask Claude Code to verify from the command line
Instead of navigating to the DynamoDB console, you can ask Claude Code to check for you:

Use the AWS CLI to describe my DynamoDB table named workshop_users and show me the table ARN, creation date, and current status.

Claude Code will generate and execute the appropriate AWS CLI command, then present the results in a readable format. One conversation, zero context switching.

Additional Resources
Amazon DynamoDB  - a fully managed, serverless, key-value NoSQL database designed to run high-performance applications.
Terraform AWS Provider Documentation  - documentation for the aws_dynamodb_table resource.
Now that you have a table defined, you can move on to the application logic...



2 - Add Business Logic
You will create one AWS Lambda function to handle all requests for the /users/* resource. The function will check the route in the request and act accordingly. The function code will be generated by Claude Code.

module architecture diagram highlighting Lambda

We have you start with a multi-purpose function because it is common when migrating existing applications to serverless. A multi-purpose function, also called a monolithic function, handles several HTTP methods. In contrast, a single-purpose function handles only one HTTP method. Similar to a traditional web application router, your Lambda function will inspect the incoming request and dispatch it to the correct handler.

This function will need to access data in the DynamoDB table created in the previous step. The table name will be passed as an environment variable (USERS_TABLE_NAME) so the dynamically prefixed table name can be used by the function to get user data.

Plan the Lambda function design
Just like you did with DynamoDB, start in plan mode to think through the Lambda function before writing code. Press Shift+Tab to toggle plan mode on, then ask Claude Code to help you work through the design:

I need a Lambda function that handles CRUD operations for user records stored in the DynamoDB table we just created. The function will sit behind API Gateway.

Help me think through the design: should I use one function for all operations or separate functions per method? How should I route requests? What error handling strategy makes sense? How should I structure the response format for API Gateway?

Claude Code will walk through the trade-offs and likely ask you clarifying questions:

"Do you want a monolithic handler that routes by HTTP method, or individual functions per endpoint?" This affects deployment complexity and cold start behavior.
"Should the function validate request bodies, or will you rely on API Gateway request validation?" This determines where input validation lives.
"Do you want to return DynamoDB errors directly or wrap them in user-friendly messages?" This is a security and UX decision.
For this workshop, guide the conversation with these design decisions:

Single monolithic function: one handler that routes by HTTP method (GET, POST, PUT, DELETE). This is simpler to deploy and common when migrating from traditional web frameworks.
Five endpoints: GET /users (list all), GET /users/{userid} (get one), POST /users (create), PUT /users/{userid} (update), DELETE /users/{userid} (delete)
Auto-generate UUIDs for new users on POST, so callers do not need to supply an ID
CORS headers on every response, since the API will be called from browsers
Table name from environment variable (USERS_TABLE_NAME) to avoid hardcoded table names
Logging for every request, essential for debugging in CloudWatch
Monolithic vs. single-purpose functions
A monolithic Lambda handles multiple routes in one function, like a traditional web server. A single-purpose Lambda handles exactly one route each. Monolithic is faster to build and has fewer cold starts (one function stays warm for all routes), but single-purpose gives you finer-grained scaling, permissions, and monitoring. For this workshop, monolithic keeps things simple. In production, evaluate the trade-off for your workload.

Once you are happy with the design, press Shift+Tab to exit plan mode.

Generate Lambda function code
Your plan mode conversation gave you a clear blueprint: a monolithic handler with five CRUD endpoints, UUID generation, CORS headers, and environment-based table configuration. Now translate that into a precise prompt. Each bullet traces back to a decision you just made:

Create a Lambda function in the workshop/src/users directory with the following specifications:
- File name: lambda_function.py
- Implement a Python handler that processes API Gateway proxy events
- Support CRUD operations (Create, Read, Update, Delete) for users in DynamoDB
- Include the following endpoints:
  * GET /users - List all users
  * GET /users/{userid} - Get a specific user
  * POST /users - Create a new user with auto-generated UUID
  * PUT /users/{userid} - Update an existing user
  * DELETE /users/{userid} - Delete a user
- Use environment variable USERS_TABLE_NAME for the table name
- Include proper CORS headers in responses
- Add logging for debugging
- Create a requirements.txt file with necessary dependencies
- Follow security best practices for handling user data

Claude Code will create both lambda_function.py and requirements.txt directly in the src/users/ directory. Review each file before approving.

Reference Code - lambda_function.py
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
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
import json
import os
import boto3
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('USERS_TABLE_NAME', 'workshop_users')
table = dynamodb.Table(table_name)

def generate_response(status_code, body):
    """Generate a standardized API response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps(body)
    }

def get_user(user_id):
    """Get a user by ID"""
    try:
        response = table.get_item(Key={'userid': user_id})
        if 'Item' in response:
            return generate_response(200, response['Item'])
        else:
            return generate_response(404, {'message': f'User with ID {user_id} not found'})
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def list_users():
    """List all users"""
    try:
        response = table.scan()
        return generate_response(200, {'users': response.get('Items', [])})
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def create_user(user_data):
    """Create a new user"""
    try:
        if 'email' not in user_data or 'name' not in user_data:
            return generate_response(400, {'message': 'Email and name are required'})

        if 'userid' not in user_data:
            user_data['userid'] = str(uuid.uuid4())

        timestamp = datetime.now().isoformat()
        user_data['createdAt'] = timestamp
        user_data['updatedAt'] = timestamp

        table.put_item(Item=user_data)

        return generate_response(201, user_data)
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def update_user(user_id, user_data):
    """Update an existing user"""
    try:
        response = table.get_item(Key={'userid': user_id})
        if 'Item' not in response:
            return generate_response(404, {'message': f'User with ID {user_id} not found'})

        user_data['updatedAt'] = datetime.now().isoformat()
        user_data['userid'] = user_id
        user_data['createdAt'] = response['Item']['createdAt']

        table.put_item(Item=user_data)

        return generate_response(200, user_data)
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def delete_user(user_id):
    """Delete a user"""
    try:
        response = table.get_item(Key={'userid': user_id})
        if 'Item' not in response:
            return generate_response(404, {'message': f'User with ID {user_id} not found'})

        table.delete_item(Key={'userid': user_id})

        return generate_response(200, {'message': f'User with ID {user_id} deleted successfully'})
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def lambda_handler(event, context):
    """Main Lambda handler function"""
    print(f"Event received: {json.dumps(event)}")

    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    path_parameters = event.get('pathParameters', {}) or {}
    query_parameters = event.get('queryStringParameters', {}) or {}

    user_id = path_parameters.get('userid') if path_parameters else None

    body = {}
    if event.get('body'):
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return generate_response(400, {'message': 'Invalid JSON in request body'})

    if http_method == 'GET':
        if user_id:
            return get_user(user_id)
        else:
            return list_users()
    elif http_method == 'POST':
        return create_user(body)
    elif http_method == 'PUT':
        if not user_id:
            return generate_response(400, {'message': 'User ID is required for update'})
        return update_user(user_id, body)
    elif http_method == 'DELETE':
        if not user_id:
            return generate_response(400, {'message': 'User ID is required for deletion'})
        return delete_user(user_id)
    else:
        return generate_response(405, {'message': 'Method not allowed'})

Reference Code - requirements.txt
boto3>=1.26.0
aws-xray-sdk>=2.12.0
Ask Claude Code to explain the Lambda code!
You can ask Claude Code to walk through the code it just wrote:

Explain the lambda_handler routing logic and how it handles each HTTP method. How does this compare to a traditional web framework's URL router?
Claude Code will read your actual file and explain it in context, not a generic example.

Create Lambda infrastructure with Claude Code
Now generate the Terraform configuration for your Lambda function:

Create a Terraform script 'users-lambda.tf' in the infrastructure directory with the following specifications:
- Create a Lambda function that deploys the code from src/users
- Package the code as a ZIP archive including dependencies from requirements.txt
- Use Python 3.10 runtime
- Configure 256MB memory and 30 second timeout
- Create a custom IAM role with least privilege permissions:
  * DynamoDB CRUD operations ONLY on the users table (no wildcard permissions)
  * Attach AWSLambdaBasicExecutionRole
  * Attach AWSXRayDaemonWriteAccess for tracing
- Set environment variable USERS_TABLE_NAME referencing the DynamoDB table name
- Enable X-Ray tracing
- Create a CloudWatch Log Group with 30-day retention
- Add permission for API Gateway to invoke the Lambda
- Add tags for resource management
- Create outputs for the Lambda ARN, function name, and invoke ARN

Claude Code will create the entire Terraform file. This is a large file, so take a moment to review the IAM policies carefully.

Reference Code - users-lambda.tf
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
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
# Lambda function for Users service

###########################################
# Lambda function package creation
###########################################

data "archive_file" "users_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/users"
  output_path = "${path.module}/../build/users_lambda.zip"

  depends_on = [null_resource.install_dependencies]
}

resource "null_resource" "install_dependencies" {
  triggers = {
    requirements_hash = filemd5("${path.module}/../src/users/requirements.txt")
  }

  provisioner "local-exec" {
    command = <<EOT
      mkdir -p ${path.module}/../build/users_package
      cp -r ${path.module}/../src/users/* ${path.module}/../build/users_package/
      pip install -r ${path.module}/../src/users/requirements.txt -t ${path.module}/../build/users_package/
      cd ${path.module}/../build/users_package && zip -r ../users_lambda.zip .
    EOT
  }
}

###########################################
# IAM Role for Lambda
###########################################

resource "aws_iam_role" "users_lambda_role" {
  name = "${var.workshop_stack_base_name}-users-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-lambda-role"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_iam_policy" "users_dynamodb_policy" {
  name        = "${var.workshop_stack_base_name}-users-dynamodb-policy"
  description = "Policy for Lambda to access DynamoDB users table with least privilege"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ]
        Resource = [
          aws_dynamodb_table.users_table.arn,
          "${aws_dynamodb_table.users_table.arn}/index/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "users_dynamodb_policy_attachment" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = aws_iam_policy.users_dynamodb_policy.arn
}

resource "aws_iam_role_policy_attachment" "users_lambda_basic_execution" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "users_lambda_xray" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

###########################################
# Lambda Function
###########################################

resource "aws_lambda_function" "users_lambda" {
  function_name    = "${var.workshop_stack_base_name}-users-function"
  filename         = data.archive_file.users_lambda_zip.output_path
  source_code_hash = data.archive_file.users_lambda_zip.output_base64sha256
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.10"
  memory_size      = 256
  timeout          = 30
  role             = aws_iam_role.users_lambda_role.arn

  environment {
    variables = {
      USERS_TABLE_NAME = aws_dynamodb_table.users_table.name
      LOG_LEVEL        = "INFO"
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-function"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
    Function    = "Users-CRUD"
  }

  depends_on = [
    aws_iam_role_policy_attachment.users_lambda_basic_execution,
    aws_iam_role_policy_attachment.users_lambda_xray,
    aws_iam_role_policy_attachment.users_dynamodb_policy_attachment
  ]
}

resource "aws_cloudwatch_log_group" "users_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.users_lambda.function_name}"
  retention_in_days = 30

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-lambda-logs"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_lambda_permission" "users_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.users_lambda.function_name
  principal     = "apigateway.amazonaws.com"
}

###########################################
# Outputs
###########################################

output "users_lambda_arn" {
  description = "ARN of the Users Lambda function"
  value       = aws_lambda_function.users_lambda.arn
}

output "users_lambda_function_name" {
  description = "Name of the Users Lambda function"
  value       = aws_lambda_function.users_lambda.function_name
}

output "users_lambda_invoke_arn" {
  description = "Invoke ARN of the Users Lambda function for API Gateway integration"
  value       = aws_lambda_function.users_lambda.invoke_arn
}

Deploy the Lambda function
Let Claude Code handle the deployment:

Run terraform plan in the infrastructure directory and show me what will be created. Then apply the changes.

Claude Code will run terraform plan, show you the output, and then run terraform apply when you approve. If there are errors, it will read the error output and suggest fixes immediately.

Deploy Checkpoint
Deployed!
After the deploy finishes, verify the function was created.
Verify your deployment by asking Claude Code:

Use the AWS CLI to describe my Lambda function named workshop-users-function and show its configuration, including memory, timeout, and environment variables.

Code Verification Challenge
Let's verify the Lambda function works. Ask Claude Code to test it:

Invoke my Lambda function workshop-users-function with a test event that creates a new user with name "Test User" and email "test@example.com". Use the AWS CLI.

Claude Code will construct the correct aws lambda invoke command, run it, and show you the result. Then try retrieving the user:

Now invoke the function again with a GET event to list all users. Show me the response.

Additional Resources
AWS Lambda Best Practices 
DynamoDB Best Practices 
Terraform AWS Lambda Documentation 
That was a substantial section! You created a Lambda function with full CRUD capabilities, proper IAM permissions, and deployed it, all through conversation with Claude Code. Next, you will connect this function to the world via API Gateway.




3 - Connect an API
Now that the backend Lambda function is deployed, it's time to connect it to the world using Amazon API Gateway. We'll use Claude Code to generate a comprehensive API Gateway configuration with Terraform.

module architecture diagram highlighting API Gateway

You will connect the front door (public URLs) to the service function using Amazon API Gateway. A REST API in API Gateway is a collection of resources and methods that are integrated with backend endpoints, Lambda functions, or other AWS services. Similar to traditional web application URL-routers, API Gateway takes inbound requests and routes them to the correct backend handler.

You will also enable distributed tracing with AWS X-Ray to help analyze and debug the application.

Plan the API Gateway design
By now you have built two components (a DynamoDB table and a Lambda function) and you may be getting comfortable jumping straight to implementation prompts. That works well when you know the domain. But API Gateway has a lot of moving parts (resources, methods, integrations, stages, CORS, usage plans), and a quick plan mode conversation can help you decide which pieces you actually need.

If you already know what you want, skip ahead to the next section. Otherwise, press Shift+Tab to enter plan mode and ask:

I have a Lambda function that handles CRUD operations for users. I need to connect it to API Gateway so it's accessible over HTTP.

Help me think through the design: should I use REST API or HTTP API? What resource paths do I need for a standard CRUD service? Do I need CORS? What about throttling, logging, and API keys?

Claude Code will walk you through the trade-offs. You might see questions like:

"Do you need features like usage plans, API keys, or request validation? Those are REST API only." This determines whether REST API (v1) or HTTP API (v2) is the right fit.
"Will browsers call this API directly, or only backend services?" This determines whether you need CORS preflight (OPTIONS) methods.
"Do you want to redeploy the API automatically when methods change?" This affects how you structure the Terraform deployment resource.
For this workshop, here are the design decisions:

REST API (v1), because we want usage plans, API keys, and detailed method-level settings that HTTP API does not support
Regional endpoint, since the API will be called from the same region
Resource paths: /users for collection operations and /users/{userid} for individual user operations
AWS_PROXY integration to pass the full request to Lambda and let it handle routing
CORS enabled with OPTIONS methods on both paths, since the API will be called from browsers
X-Ray tracing on the prod stage for debugging
CloudWatch logging with structured access logs
Usage plan with API key for throttling and quota limits
Press Shift+Tab to exit plan mode when you are ready.

Create the API with Claude Code
You have a clear picture of the API Gateway architecture: a regional REST API with two resource paths, Lambda proxy integration, CORS, X-Ray tracing, and a usage plan. Now give Claude Code a prompt that captures all of those decisions:

Create a Terraform script 'api-gateway.tf' in the infrastructure directory with the following specifications:
- Create a regional REST API Gateway named using the workshop_stack_base_name variable
- Set up resource paths for /users and /users/{userid} following REST naming conventions
- Configure the following methods:
  * GET /users - List all users
  * GET /users/{userid} - Get a specific user
  * POST /users - Create a new user
  * PUT /users/{userid} - Update an existing user
  * DELETE /users/{userid} - Delete a user
  * OPTIONS for all paths (for CORS support)
- Integrate all methods with the users Lambda function using AWS_PROXY
- Configure CORS with appropriate headers for cross-origin requests
- Deploy to a 'prod' stage with X-Ray tracing enabled
- Add CloudWatch logging with 30-day retention
- Add method settings for metrics and throttling
- Create a usage plan and API key
- Update the Lambda permission to allow API Gateway invocation with proper source ARN
- Output the API endpoint URL, execution ARN, and API ID

This is a large Terraform file. Claude Code will create it step by step. Take your time reviewing the proposed content. If you want to see it in smaller chunks, you can ask Claude Code to explain each section as it writes it.

Reference Code - api-gateway.tf
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
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
###########################################
# API Gateway for Users Service
###########################################

resource "aws_api_gateway_rest_api" "users_api" {
  name        = "${var.workshop_stack_base_name}-users-api"
  description = "API Gateway for Users Service"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

###########################################
# API Resources
###########################################

resource "aws_api_gateway_resource" "users_resource" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  parent_id   = aws_api_gateway_rest_api.users_api.root_resource_id
  path_part   = "users"
}

resource "aws_api_gateway_resource" "user_resource" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  parent_id   = aws_api_gateway_resource.users_resource.id
  path_part   = "{userid}"
}

###########################################
# Methods for /users
###########################################

resource "aws_api_gateway_method" "users_get" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "users_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.users_resource.id
  http_method             = aws_api_gateway_method.users_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

resource "aws_api_gateway_method" "users_post" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "users_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.users_resource.id
  http_method             = aws_api_gateway_method.users_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

resource "aws_api_gateway_method" "users_options" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "users_options_integration" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  resource_id = aws_api_gateway_resource.users_resource.id
  http_method = aws_api_gateway_method.users_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "users_options_response" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  resource_id = aws_api_gateway_resource.users_resource.id
  http_method = aws_api_gateway_method.users_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "users_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  resource_id = aws_api_gateway_resource.users_resource.id
  http_method = aws_api_gateway_method.users_options.http_method
  status_code = aws_api_gateway_method_response.users_options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

###########################################
# Methods for /users/{userid}
###########################################

resource "aws_api_gateway_method" "user_get" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.userid" = true
  }
}

resource "aws_api_gateway_integration" "user_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.user_resource.id
  http_method             = aws_api_gateway_method.user_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

resource "aws_api_gateway_method" "user_put" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "PUT"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.userid" = true
  }
}

resource "aws_api_gateway_integration" "user_put_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.user_resource.id
  http_method             = aws_api_gateway_method.user_put.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

resource "aws_api_gateway_method" "user_delete" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "DELETE"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.userid" = true
  }
}

resource "aws_api_gateway_integration" "user_delete_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.user_resource.id
  http_method             = aws_api_gateway_method.user_delete.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

resource "aws_api_gateway_method" "user_options" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "user_options_integration" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  resource_id = aws_api_gateway_resource.user_resource.id
  http_method = aws_api_gateway_method.user_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "user_options_response" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  resource_id = aws_api_gateway_resource.user_resource.id
  http_method = aws_api_gateway_method.user_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "user_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  resource_id = aws_api_gateway_resource.user_resource.id
  http_method = aws_api_gateway_method.user_options.http_method
  status_code = aws_api_gateway_method_response.user_options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,PUT,DELETE,OPTIONS'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

###########################################
# Deployment and Stage
###########################################

resource "aws_api_gateway_deployment" "users_api_deployment" {
  depends_on = [
    aws_api_gateway_integration.users_get_integration,
    aws_api_gateway_integration.users_post_integration,
    aws_api_gateway_integration.users_options_integration,
    aws_api_gateway_integration.user_get_integration,
    aws_api_gateway_integration.user_put_integration,
    aws_api_gateway_integration.user_delete_integration,
    aws_api_gateway_integration.user_options_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.users_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.users_resource.id,
      aws_api_gateway_resource.user_resource.id,
      aws_api_gateway_method.users_get.id,
      aws_api_gateway_method.users_post.id,
      aws_api_gateway_method.users_options.id,
      aws_api_gateway_method.user_get.id,
      aws_api_gateway_method.user_put.id,
      aws_api_gateway_method.user_delete.id,
      aws_api_gateway_method.user_options.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "users_api_stage" {
  deployment_id        = aws_api_gateway_deployment.users_api_deployment.id
  rest_api_id          = aws_api_gateway_rest_api.users_api.id
  stage_name           = "prod"
  xray_tracing_enabled = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.users_api_logs.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api-stage"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_cloudwatch_log_group" "users_api_logs" {
  name              = "/aws/apigateway/${aws_api_gateway_rest_api.users_api.name}"
  retention_in_days = 30

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api-logs"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_api_gateway_method_settings" "users_api_settings" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  stage_name  = aws_api_gateway_stage.users_api_stage.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled        = true
    logging_level          = "INFO"
    data_trace_enabled     = true
    throttling_rate_limit  = 100
    throttling_burst_limit = 50
  }
}

###########################################
# Usage Plan and API Key
###########################################

resource "aws_api_gateway_usage_plan" "users_api_usage_plan" {
  name        = "${var.workshop_stack_base_name}-users-api-usage-plan"
  description = "Usage plan for Users API"

  api_stages {
    api_id = aws_api_gateway_rest_api.users_api.id
    stage  = aws_api_gateway_stage.users_api_stage.stage_name
  }

  quota_settings {
    limit  = 1000
    period = "DAY"
  }

  throttle_settings {
    burst_limit = 20
    rate_limit  = 10
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api-usage-plan"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_api_gateway_api_key" "users_api_key" {
  name = "${var.workshop_stack_base_name}-users-api-key"

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api-key"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_api_gateway_usage_plan_key" "users_api_usage_plan_key" {
  key_id        = aws_api_gateway_api_key.users_api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.users_api_usage_plan.id
}

###########################################
# Update Lambda permissions
###########################################

resource "aws_lambda_permission" "api_gateway_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.users_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.users_api.execution_arn}/*/*"
}

###########################################
# Outputs
###########################################

output "users_api_url" {
  description = "URL of the Users API"
  value       = aws_api_gateway_stage.users_api_stage.invoke_url
}

output "users_api_execution_arn" {
  description = "Execution ARN of the Users API"
  value       = aws_api_gateway_rest_api.users_api.execution_arn
}

output "users_api_id" {
  description = "ID of the Users API"
  value       = aws_api_gateway_rest_api.users_api.id
}

output "users_api_key" {
  description = "API Key for the Users API"
  value       = aws_api_gateway_api_key.users_api_key.value
  sensitive   = true
}

Understanding the API Gateway Configuration
Let's explore what Claude Code generated. Ask it to explain each major component:

The API Gateway Resource Tree
Explain how the API Gateway resources are organized in api-gateway.tf. What's the relationship between the root, /users, and /users/{userid} paths?

API Gateway Structure
Your API Gateway resources form a tree:

Root (/): the API entry point
/users: child of root, handles collection operations (list, create)
/users/{userid}: child of /users, handles individual user operations (get, update, delete)
Each resource has methods (GET, PUT, DELETE, OPTIONS) that map to Lambda integrations.

The Lambda Integration
Ever wonder how API Gateway talks to your Lambda function? Ask Claude Code:

Why does the API Gateway use POST to call Lambda even when the API method is GET? Explain the AWS_PROXY integration type.

The key insight: API Gateway always uses POST to invoke Lambda, regardless of the original HTTP method. The AWS_PROXY integration passes the entire request (method, headers, body, path) as a JSON event to your Lambda function. Your function reads httpMethod from that event to decide what to do.

CORS: The Browser's Security Guard
What is CORS and why do I need all these OPTIONS methods? Why is the origin set to '*'?

CORS wildcard origin
The reference code uses Access-Control-Allow-Origin: '*' which allows any website to call your API. This is acceptable for a workshop, but in production you should restrict this to your specific domain(s).

Deploy the API
Time to make it live:

Run terraform apply with auto-approve in the infrastructure directory.

Deploy Checkpoint
Deployed!
After the deploy finishes, verify your API is working.
Get your API endpoint URL and test it:

Get the API Gateway endpoint URL from Terraform outputs. Then test it by creating a user with curl and listing all users.

Claude Code will:

Run terraform output to get the URL
Run curl commands to create a user
Run curl to list users
Show you the results
All within the same conversation. No switching between terminals, no copy-pasting URLs.

When things go wrong
If you get a 500 error, just tell Claude Code:

My API is returning a 500 error. Help me troubleshoot by checking Lambda logs and API Gateway configuration.
Claude Code will check CloudWatch logs, inspect your Terraform configuration, and help you find the root cause.

Heads up!
The next sections dive into authentication and testing, and they can get a bit more challenging! Don't worry if you get stuck; use the reference code sections to keep moving forward. The goal is learning, not perfection.

Additional Resources
Amazon API Gateway REST API 
AWS X-Ray  - distributed tracing for debugging
API Gateway Best Practices 
You have a working API with proper logging, monitoring, and CORS support. In the next section, we will add authentication to secure your API.




3.1 - Create User Pool
For API authentication and authorization you will use a Lambda Authorizer function in API Gateway and a Cognito User Pool  for the user directory. We'll use Claude Code to generate the Terraform code.

module architecture diagram highlighting Cognito

Amazon Cognito provides user sign-up, sign-in, and access control. It supports sign-in with social identity providers and enterprise identity providers via SAML 2.0 and OpenID Connect. Think of it as a managed user database that handles all the complexity of password hashing, token generation, and account verification for you.

Plan the authentication design
Authentication has more moving parts than most developers expect. Before generating Terraform, it is worth spending a minute in plan mode to understand what you are building and why.

If you are already familiar with Cognito and know what configuration you need, skip ahead to the next section. Otherwise, press Shift+Tab to enter plan mode and ask:

I need to add authentication to my REST API. Users should be able to sign up, sign in, and get a JWT token that they pass to API Gateway. I'm considering Amazon Cognito.

Help me think through the design: what Cognito resources do I need? What auth flows should I enable? How will the JWT token get validated: in API Gateway or in a Lambda authorizer? What are the trade-offs?

Claude Code will explain the Cognito resource model and ask clarifying questions like:

"Do you want API Gateway's built-in Cognito authorizer, or a custom Lambda authorizer that validates JWTs?" The built-in authorizer is simpler but less flexible; a Lambda authorizer lets you add custom logic like group-based access control.
"Should users sign up with email or username?" This affects the user pool schema and cannot be changed after creation.
"Do you need a hosted UI for sign-up/sign-in, or will you build your own?" This determines whether you need a Cognito domain and callback URLs.
For this workshop, here are the design decisions:

Cognito User Pool as the identity store: managed sign-up, sign-in, and token generation
Email as username, so users sign in with their email address
Hosted UI for sign-up and sign-in. Cognito provides a ready-made web page so we don't need to build one
Lambda authorizer (not the built-in Cognito authorizer), which we will implement in the next step, giving us full control over JWT validation and the ability to extract user claims
Self-registration with email verification, allowing users to sign up on their own and confirm via a verification code
Admin group called "Administrators" for future group-based access control
Press Shift+Tab to exit plan mode when you are ready.

Create Cognito User Pool with Claude Code
Your plan gives you a clear picture: a Cognito User Pool with email-based sign-in, a hosted UI, self-registration, and an admin group. Now give Claude Code a prompt that captures those decisions:

Create a Terraform script 'cognito.tf' in the infrastructure directory with the following specifications:
- Create a Cognito User Pool named using the workshop_stack_base_name variable with '-user-pool' suffix
- Configure email as a required attribute and username
- Set up password policies with minimum length of 8 characters requiring numbers, special chars, uppercase and lowercase
- Enable self-registration with email verification
- Set up proper account recovery mechanisms
- Create a user pool client with:
  * Refresh token expiration of 30 days
  * Support for USER_PASSWORD_AUTH, USER_SRP_AUTH, REFRESH_TOKEN_AUTH, and ADMIN_USER_PASSWORD_AUTH flows
  * No client secret
  * Callback URL to http://localhost:3000/callback
  * OAuth scopes for email and openid
- Create a Cognito domain using the user pool client ID
- Create an admin group called 'Administrators'
- Add appropriate tags for resource management
- Output the user pool ID, client ID, admin group name, login URL, and a sample auth CLI command

Claude Code will create cognito.tf directly. This is where you start to see the power of an agentic tool: it understands the relationships between Cognito resources (pool, client, domain, group) and wires them together correctly.

Reference Code - cognito.tf
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
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
variable "user_pool_admin_group_name" {
  description = "Name for the admin group in Cognito User Pool"
  type        = string
  default     = "Administrators"
}

# 1. AWS Cognito User Pool
resource "aws_cognito_user_pool" "main" {
  name = "${var.workshop_stack_base_name}-user-pool"

  admin_create_user_config {
    allow_admin_create_user_only = false
  }

  auto_verified_attributes = ["email"]

  schema {
    name                = "name"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }

  username_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  lifecycle {
    ignore_changes = [schema]
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}-user-pool"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

# 2. Cognito User Pool Client
resource "aws_cognito_user_pool_client" "client" {
  name         = "${var.workshop_stack_base_name}-client"
  user_pool_id = aws_cognito_user_pool.main.id

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]

  generate_secret                      = false
  prevent_user_existence_errors        = "ENABLED"
  refresh_token_validity               = 30
  supported_identity_providers         = ["COGNITO"]
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["email", "openid"]
  callback_urls                        = ["http://localhost:3000/callback"]
}

# 3. Cognito User Pool Domain
resource "aws_cognito_user_pool_domain" "main" {
  domain       = aws_cognito_user_pool_client.client.id
  user_pool_id = aws_cognito_user_pool.main.id
}

# 4. Cognito User Group for administrators
resource "aws_cognito_user_group" "admin" {
  name         = var.user_pool_admin_group_name
  user_pool_id = aws_cognito_user_pool.main.id
  description  = "API Administrators"
  precedence   = 0
}

# 5. Outputs
output "cognito_user_pool_id" {
  description = "ID of the Cognito User Pool"
  value       = aws_cognito_user_pool.main.id
}

output "cognito_user_pool_client_id" {
  description = "ID of the Cognito User Pool Client"
  value       = aws_cognito_user_pool_client.client.id
}

output "cognito_user_pool_admin_group_name" {
  description = "Name of the Cognito User Pool Admin Group"
  value       = aws_cognito_user_group.admin.name
}

output "cognito_login_url" {
  description = "Login URL for Cognito User Pool"
  value       = "https://${aws_cognito_user_pool_domain.main.domain}.auth.${var.region}.amazoncognito.com/login?client_id=${aws_cognito_user_pool_client.client.id}&response_type=code&redirect_uri=http://localhost:3000/callback"
}

output "cognito_auth_sample_command" {
  description = "Sample AWS CLI command for Cognito authentication"
  value       = "aws cognito-idp admin-initiate-auth --user-pool-id ${aws_cognito_user_pool.main.id} --client-id ${aws_cognito_user_pool_client.client.id} --auth-flow ADMIN_USER_PASSWORD_AUTH --auth-parameters USERNAME=<email>,PASSWORD=<password>"
}

Deploy and Test Cognito User Pool
The next steps are intentionally less detailed; you've done this before! If you need a refresher, refer back to the previous deployment sections.

Deploy the Cognito resources:

Run terraform apply with auto-approve in the infrastructure directory. After deployment, show me the cognito_login_url from the outputs.

Claude Code will deploy and then print the login URL. Copy that URL and open it in a new browser tab.

You should see a Cognito hosted UI where you can either sign in or sign up for a new account.

Cognito sign up form

Choose the Sign up link (not the Sign In button) and fill in the user registration form with your email and password.

You should receive an email with a verification code. Use the code to confirm your account.

Take note of your new userid and password
You will need the userid and password you set in the next step! Make a note of both.

Ask Claude Code to explain the Cognito configuration!
You can ask Claude Code to explain the security features:

Explain the security features in my Cognito configuration. Why do we need the password policy, email verification, and the different auth flows?
Claude Code will read your cognito.tf file and explain each security decision in context.

Next Steps
After setting up your Cognito User Pool, you are ready to implement API Gateway authorization in the next section.

Additional Resources
Amazon Cognito - Getting started with user pools 
JWT Token Validation 
Terraform AWS Cognito Documentation 
Now that you have a user directory, let's secure your API endpoints with a Lambda authorizer.

3.2 - Secure API Gateway
Now that we have our Cognito User Pool set up, we need to create a Lambda authorizer to validate JWT tokens and secure our API endpoints.

Security First!
To ensure robust authentication and authorization, your platform/security team will typically provide you a standardized Lambda authorizer function. Below is a reference implementation that demonstrates proper JWT token validation.

Plan the Lambda authorizer design
A Lambda authorizer is the gatekeeper for your entire API, so it is worth understanding what it does before generating code. If you are already familiar with Lambda authorizers and JWT validation, skip ahead to the next section. Otherwise, press Shift+Tab to enter plan mode and ask:

I need a Lambda authorizer for my API Gateway that validates JWT tokens issued by Cognito. The authorizer should check the token and return an IAM policy that allows or denies the request.

Help me think through the design: how does a Lambda authorizer receive the token? How should I validate it (full signature verification or claims-only)? What claims should I check? What does the response format look like?

Claude Code will explain the authorizer flow and ask clarifying questions like:

"Do you want a TOKEN authorizer (reads from the Authorization header) or a REQUEST authorizer (reads from multiple headers/query params)?" TOKEN is simpler and standard for bearer tokens.
"Should I verify the JWT signature against Cognito's JWKS public keys, or just validate claims?" Full signature verification is required for production, but adds complexity with key fetching and caching.
"Do you want to pass user information (sub, username, groups) to the backend Lambda via the authorizer context?" This lets your CRUD function know who is making the request.
For this workshop, here are the design decisions:

TOKEN authorizer: reads the JWT from the Authorization header
Claims-only validation (workshop shortcut): verify issuer, client_id, and token_use without full signature verification. Production code must verify signatures against JWKS.
Fetch JWKS from Cognito: validate that the token's kid (key ID) exists in Cognito's published keys
Pass user context: include userId (sub) and username in the authorizer response so the backend Lambda can use them
Configuration via environment variables: USER_POOL_ID and CLIENT_ID injected by Terraform, not hardcoded
Press Shift+Tab to exit plan mode when you are ready.

Create the Lambda authorizer code
Your plan mode conversation gave you a clear design: a TOKEN authorizer that fetches JWKS, validates claims (issuer, client_id, token_use), and returns an IAM policy with user context. Now give Claude Code a precise prompt:

Create a Lambda authorizer function in the workshop/src/authorizer directory with the following specifications:
- File name: lambda_authorizer.py
- Validate JWT tokens from Cognito
- Get configuration from environment variables: AWS_REGION, USER_POOL_ID, CLIENT_ID
- Fetch JWKS from Cognito to validate token headers
- For this workshop, verify basic token structure and claims without full signature verification
- Verify issuer matches the Cognito user pool
- Verify client_id claim matches the app client
- Verify token_use is 'access'
- Generate an IAM allow/deny policy based on validation results
- Include proper error handling and logging
- Also create a requirements.txt with PyJWT and requests dependencies

Claude Code will create both files directly. Review the authorizer code carefully; this is a security-critical component.

Reference Code - lambda_authorizer.py
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
import json
import jwt
import requests
import os

def lambda_handler(event, context):
    token = event['authorizationToken'].replace('Bearer ', '')

    try:
        # Get configuration from environment variables
        region = os.environ['AWS_REGION']
        user_pool_id = os.environ['USER_POOL_ID']
        client_id = os.environ['CLIENT_ID']

        # Get Cognito JWKS
        jwks_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'

        # Fetch JWKS
        jwks_response = requests.get(jwks_url)
        jwks = jwks_response.json()

        # Get token header
        header = jwt.get_unverified_header(token)
        kid = header['kid']

        # Find matching key
        key_data = None
        for jwk in jwks['keys']:
            if jwk['kid'] == kid:
                key_data = jwk
                break

        if not key_data:
            raise Exception('Key not found')

        # Verify basic token structure and claims
        # In production, you should verify the signature properly
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )

        # Verify issuer and audience
        expected_issuer = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}'
        if payload.get('iss') != expected_issuer:
            raise Exception('Invalid issuer')

        if payload.get('client_id') != client_id:
            raise Exception('Invalid audience')

        # Check token type
        if payload.get('token_use') != 'access':
            raise Exception('Invalid token use')

        # Generate allow policy
        policy = {
            'principalId': payload.get('sub', 'user'),
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': event['methodArn']
                    }
                ]
            },
            'context': {
                'userId': payload.get('sub', ''),
                'username': payload.get('username', '')
            }
        }

        return policy

    except Exception as e:
        print(f"Authorization failed: {str(e)}")
        raise Exception('Unauthorized')

Workshop Shortcut
The reference implementation uses verify_signature: False for simplicity. In a production environment, you must verify the JWT signature against the Cognito JWKS public keys. Never skip signature verification in production code.

Reference Code - requirements.txt
PyJWT==2.8.0
requests==2.31.0
Action Required!
Verify that Claude Code created lambda_authorizer.py in the src/authorizer/ directory before proceeding. You can ask:

Show me the contents of the src/authorizer directory.
Understanding the Lambda Authorizer
Ask Claude Code to explain the key concepts:

Explain how the Lambda authorizer validates JWT tokens. What does each step do and why? What happens when a token is invalid?

Claude Code will walk you through:

JWT structure: header, payload, signature
JWKS fetching: how Cognito publishes its public keys
Claim verification: why we check issuer, audience, and token_use
Policy generation: how the IAM allow/deny policy controls API access
Create the Authorizer Infrastructure
Now create the Terraform configuration to deploy the authorizer:

Create a Terraform script 'lambda-authorizer.tf' in the infrastructure directory that:
1. Creates an IAM role with AWSLambdaBasicExecutionRole
2. Packages the Lambda code from src/authorizer including dependencies
3. Creates a Lambda function using Python 3.10 runtime
4. Sets environment variables for USER_POOL_ID and CLIENT_ID using values from the Cognito resources
5. Creates a Lambda permission for API Gateway to invoke it
6. Outputs the authorizer Lambda ARN
7. Uses the workshop_stack_base_name variable as a prefix for resource names

Reference Code - lambda-authorizer.tf
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
# IAM role for authorizer Lambda
resource "aws_iam_role" "authorizer_lambda_role" {
  name = "${var.workshop_stack_base_name}-authorizer-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.workshop_stack_base_name}-authorizer-lambda-role"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_iam_role_policy_attachment" "authorizer_lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.authorizer_lambda_role.name
}

# Install dependencies and package authorizer Lambda
resource "null_resource" "authorizer_dependencies" {
  triggers = {
    requirements = filemd5("${path.module}/../src/authorizer/requirements.txt")
    source_code  = filemd5("${path.module}/../src/authorizer/lambda_authorizer.py")
  }

  provisioner "local-exec" {
    command = <<EOF
      cd ${path.module}/../src/authorizer
      pip install -r requirements.txt -t .
      rm -rf __pycache__ *.dist-info
    EOF
  }
}

data "archive_file" "authorizer_lambda_zip" {
  depends_on  = [null_resource.authorizer_dependencies]
  type        = "zip"
  source_dir  = "${path.module}/../src/authorizer"
  output_path = "${path.module}/authorizer-lambda.zip"
}

resource "aws_lambda_function" "authorizer" {
  filename         = data.archive_file.authorizer_lambda_zip.output_path
  function_name    = "${var.workshop_stack_base_name}-authorizer"
  role             = aws_iam_role.authorizer_lambda_role.arn
  handler          = "lambda_authorizer.lambda_handler"
  runtime          = "python3.10"
  source_code_hash = data.archive_file.authorizer_lambda_zip.output_base64sha256

  environment {
    variables = {
      USER_POOL_ID = aws_cognito_user_pool.main.id
      CLIENT_ID    = aws_cognito_user_pool_client.client.id
    }
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}-authorizer"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

resource "aws_lambda_permission" "authorizer_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.authorizer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.users_api.execution_arn}/*/*"
}

Deploy the Lambda Authorizer
terraform apply -auto-approve

Deployed!
Your Lambda authorizer is deployed! This is a major milestone. You have implemented token-based security for your serverless API.
Connect the Authorizer to API Gateway
Now we need to update the API Gateway configuration to use the authorizer. Ask Claude Code:

Update api-gateway.tf to:
1. Add an aws_api_gateway_authorizer resource of type TOKEN that uses the Authorization header and references the authorizer Lambda function
2. Update all API methods (except OPTIONS) to use authorization = "CUSTOM" with the new authorizer
3. Keep the OPTIONS methods with authorization = "NONE" for CORS
4. Show me the changes before applying

Claude Code will read your existing api-gateway.tf, understand its structure, and make targeted edits. This is a key advantage of the agentic approach: it modifies existing code rather than asking you to find and replace sections manually.

Reference Code - API Gateway authorizer additions
Add these resources and update existing methods:

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
# Lambda Authorizer
resource "aws_api_gateway_authorizer" "cognito_authorizer" {
  name                   = "${var.workshop_stack_base_name}-authorizer"
  rest_api_id            = aws_api_gateway_rest_api.users_api.id
  authorizer_uri         = aws_lambda_function.authorizer.invoke_arn
  type                   = "TOKEN"
  identity_source        = "method.request.header.Authorization"
}

# For each method resource (users_get, users_put, user_get, user_put, user_delete),
# change:
#   authorization = "NONE"
# to:
#   authorization = "CUSTOM"
#   authorizer_id = aws_api_gateway_authorizer.cognito_authorizer.id

Deploy the API Gateway Updates
terraform apply -auto-approve

Congratulations!
Your API is now secured with Cognito authentication and Lambda authorization! Only authenticated users with valid JWT tokens can access the protected endpoints.
Additional Resources
Lambda Authorizer 
JWT Token Validation 
Now that you have secured your API, let's verify that the authentication actually works by testing with valid and invalid tokens.

3.3 - Verify Authentication
Let's verify that the authentication works by testing with both valid and invalid tokens. Claude Code can run all of these commands for you directly. We will run two simple tests: one with a valid token and one with an invalid token.

Get Cognito Token
Ask Claude Code to help you get a token:

Get the Cognito client ID from Terraform outputs, then use the AWS CLI to authenticate with Cognito using USER_PASSWORD_AUTH flow. I need the access token. My email is your-email@example.com and my password is your-password. Replace these with my actual credentials.

Or run the commands manually:

# Get client ID
COGNITO_CLIENT_ID=$(terraform output -raw cognito_user_pool_client_id)

# Get token for your user
TOKEN=$(aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id $COGNITO_CLIENT_ID \
  --auth-parameters USERNAME=your-email@example.com,PASSWORD=your-password \
  --query 'AuthenticationResult.AccessToken' \
  --output text)

Note: Replace your-email@example.com and your-password with the credentials you created when signing up in the previous step.

Valid Token Test
# Get API endpoint
API_ENDPOINT=$(terraform output -raw users_api_url)

# Test with valid token
curl -H "Authorization: Bearer $TOKEN" \
  $API_ENDPOINT/users

Expected: 200 response with user data (or an empty users list).

Invalid Token Test
# Test with invalid token
curl -w "\nStatus: %{http_code}\n" \
  -H "Authorization: Bearer invalid-token-123" \
  $API_ENDPOINT/users

Expected: 401 Unauthorized

Let Claude Code do the testing
You can ask Claude Code to run both tests for you in sequence:

Get my API endpoint and Cognito token from Terraform outputs, then test the API with the valid token and also with an invalid token. Show me both results.
Claude Code will execute the commands, capture the results, and present them clearly.

Your API correctly accepts valid tokens and rejects invalid ones. Authentication is working!
Additional Resources
Lambda Authorizer 
Amazon Cognito - Getting started with user pools 
JWT Token Validation 
You have successfully tested your secured API with token-based authentication. Next, we will add unit tests to ensure your application logic is solid.

4 - Unit Test
Running unit tests is a well-known best practice in traditional development.

Test cycle illustration

In a serverless/cloud environment the test cycle is equally important! Some tests can use mocked services. Mocked services provide a representation that can stand in for the real service. Generally, mocked services are much faster to create, configure, and tear down after testing is done.

In this section, we'll use Claude Code to generate unit tests for our serverless application. This is where Claude Code's ability to read your existing code really shines: it can analyze your Lambda function and generate tests that match your actual implementation.

Plan the test strategy
You could jump straight to "generate tests for my Lambda function" and get a reasonable result. But a quick plan mode conversation helps you think about what to test and how thoroughly, decisions that are easy to overlook when you let an AI generate everything.

If you already have a clear testing strategy in mind, skip ahead to the next section. Otherwise, press Shift+Tab to enter plan mode and ask:

I have a Lambda function at src/users/lambda_function.py that handles CRUD operations for users via API Gateway. I want to write unit tests for it.

Help me think through a test strategy: what test cases do I need for each CRUD operation? What edge cases and error scenarios should I cover? How should I mock DynamoDB? What testing framework and tools make sense for Python Lambda functions?

Claude Code will read your Lambda function code and come back with a testing plan. You might see questions like:

"Do you want to test each CRUD function individually AND test the lambda_handler routing, or just one level?" Testing both gives you better fault isolation when something breaks.
"Should I mock at the boto3 level or use moto to simulate real DynamoDB behavior?" Moto creates a fake DynamoDB in memory and catches more integration issues than simple mocks.
"What about invalid JSON in the request body, missing path parameters, or unsupported HTTP methods?" These edge cases are easy to forget but common in production.
For this workshop, here are the testing decisions:

pytest as the test framework, the standard for Python projects, with great fixture support
moto for DynamoDB mocking, which simulates real DynamoDB behavior in memory, catching issues that simple mocks would miss
Two levels of testing: test each CRUD function directly (unit) AND test the lambda_handler routing (integration-style)
Happy path for every operation: create, read single, list all, update, delete
Error cases: missing required fields on create, get/update/delete a nonexistent user, invalid HTTP method, malformed JSON body
CORS headers verified on responses (easy to break accidentally)
Coverage reporting with pytest-cov to see which code paths are untested
Press Shift+Tab to exit plan mode when you are ready.

Generate unit tests with Claude Code
Your plan mode conversation mapped out the test surface: two levels of testing, happy paths for all five CRUD operations, error cases for missing fields and nonexistent resources, and moto for realistic DynamoDB simulation. Now give Claude Code a prompt that captures all of that:

Read my Lambda function at src/users/lambda_function.py and generate a complete unit test suite with the following requirements:
1. Use pytest framework with moto for AWS service mocking
2. Test all CRUD operations (create, read, update, delete)
3. Test the lambda_handler routing for all HTTP methods
4. Test error cases (missing fields, nonexistent users, invalid methods)
5. Mock DynamoDB interactions using moto's mock_dynamodb
6. Create the tests in tests/unit/users/test_app.py
7. Create a conftest.py for path setup
8. Include a requirements-dev.txt file with all testing dependencies

Claude Code will read your actual lambda_function.py, understand the function signatures, DynamoDB interactions, and response formats, and generate tests that match your implementation perfectly. This is far more effective than generic test templates.

Reference Code - requirements-dev.txt
pytest==7.4.0
pytest-cov==4.1.0
moto==4.2.0
boto3==1.28.0
coverage==7.3.0
pytest-mock==3.11.1
freezegun==1.2.2
Reference Code - test_app.py
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
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
import json
import os
import pytest
import boto3
from moto import mock_dynamodb

# Import the module to test
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/users'))
import lambda_function as app

# Test constants
TEST_TABLE_NAME = 'test-users-table'
TEST_USER_ID = 'test-user-123'
TEST_USER = {
    'userid': TEST_USER_ID,
    'name': 'Test User',
    'email': 'test@example.com'
}


@pytest.fixture
def dynamodb_table():
    """Create a mock DynamoDB table for testing"""
    with mock_dynamodb():
        os.environ['USERS_TABLE_NAME'] = TEST_TABLE_NAME

        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.create_table(
            TableName=TEST_TABLE_NAME,
            KeySchema=[{'AttributeName': 'userid', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'userid', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        app.table_name = TEST_TABLE_NAME
        app.table = table

        yield table


class TestUserAPI:
    """Test suite for User API functions"""

    def test_generate_response(self):
        """Test the generate_response helper function"""
        response = app.generate_response(200, {'message': 'test'})
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == {'message': 'test'}
        assert response['headers']['Content-Type'] == 'application/json'
        assert response['headers']['Access-Control-Allow-Origin'] == '*'

    def test_create_user(self, dynamodb_table):
        """Test creating a new user"""
        user_data = {
            'name': 'New User',
            'email': 'new@example.com'
        }

        response = app.create_user(user_data)
        body = json.loads(response['body'])

        assert response['statusCode'] == 201
        assert 'userid' in body
        assert body['name'] == 'New User'
        assert body['email'] == 'new@example.com'
        assert 'createdAt' in body
        assert 'updatedAt' in body

    def test_create_user_with_missing_fields(self, dynamodb_table):
        """Test creating a user with missing required fields"""
        user_data = {'name': 'Incomplete User'}

        response = app.create_user(user_data)
        body = json.loads(response['body'])

        assert response['statusCode'] == 400
        assert 'message' in body
        assert 'required' in body['message']

    def test_get_user(self, dynamodb_table):
        """Test getting a user by ID"""
        dynamodb_table.put_item(Item=TEST_USER)

        response = app.get_user(TEST_USER_ID)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['userid'] == TEST_USER_ID
        assert body['name'] == TEST_USER['name']
        assert body['email'] == TEST_USER['email']

    def test_get_nonexistent_user(self, dynamodb_table):
        """Test getting a user that doesn't exist"""
        response = app.get_user('nonexistent-user')
        body = json.loads(response['body'])

        assert response['statusCode'] == 404
        assert 'not found' in body['message']

    def test_list_users(self, dynamodb_table):
        """Test listing all users"""
        dynamodb_table.put_item(Item=TEST_USER)
        dynamodb_table.put_item(Item={
            'userid': 'user-2',
            'name': 'User Two',
            'email': 'user2@example.com'
        })

        response = app.list_users()
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert 'users' in body
        assert len(body['users']) == 2

    def test_update_user(self, dynamodb_table):
        """Test updating an existing user"""
        dynamodb_table.put_item(Item={
            **TEST_USER,
            'createdAt': '2023-01-01T00:00:00',
            'updatedAt': '2023-01-01T00:00:00'
        })

        updated_data = {
            'name': 'Updated Name',
            'email': TEST_USER['email']
        }

        response = app.update_user(TEST_USER_ID, updated_data)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['name'] == 'Updated Name'
        assert body['createdAt'] == '2023-01-01T00:00:00'
        assert body['updatedAt'] != '2023-01-01T00:00:00'

    def test_update_nonexistent_user(self, dynamodb_table):
        """Test updating a user that doesn't exist"""
        response = app.update_user('nonexistent-user', {'name': 'New Name'})
        body = json.loads(response['body'])

        assert response['statusCode'] == 404
        assert 'not found' in body['message']

    def test_delete_user(self, dynamodb_table):
        """Test deleting a user"""
        dynamodb_table.put_item(Item=TEST_USER)

        response = app.delete_user(TEST_USER_ID)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert 'deleted successfully' in body['message']

        verify = app.get_user(TEST_USER_ID)
        assert verify['statusCode'] == 404

    def test_delete_nonexistent_user(self, dynamodb_table):
        """Test deleting a user that doesn't exist"""
        response = app.delete_user('nonexistent-user')
        body = json.loads(response['body'])

        assert response['statusCode'] == 404
        assert 'not found' in body['message']

    def test_lambda_handler_get_all(self, dynamodb_table):
        """Test lambda_handler for GET all users"""
        dynamodb_table.put_item(Item=TEST_USER)

        event = {
            'httpMethod': 'GET',
            'path': '/users',
            'pathParameters': None,
            'queryStringParameters': None
        }

        response = app.lambda_handler(event, {})
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert 'users' in body
        assert len(body['users']) == 1

    def test_lambda_handler_get_one(self, dynamodb_table):
        """Test lambda_handler for GET one user"""
        dynamodb_table.put_item(Item=TEST_USER)

        event = {
            'httpMethod': 'GET',
            'path': f'/users/{TEST_USER_ID}',
            'pathParameters': {'userid': TEST_USER_ID},
            'queryStringParameters': None
        }

        response = app.lambda_handler(event, {})
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['userid'] == TEST_USER_ID

    def test_lambda_handler_create(self, dynamodb_table):
        """Test lambda_handler for POST (create user)"""
        event = {
            'httpMethod': 'POST',
            'path': '/users',
            'pathParameters': None,
            'queryStringParameters': None,
            'body': json.dumps({
                'name': 'New Handler User',
                'email': 'handler@example.com'
            })
        }

        response = app.lambda_handler(event, {})
        body = json.loads(response['body'])

        assert response['statusCode'] == 201
        assert body['name'] == 'New Handler User'
        assert 'userid' in body

    def test_lambda_handler_update(self, dynamodb_table):
        """Test lambda_handler for PUT (update user)"""
        dynamodb_table.put_item(Item={
            **TEST_USER,
            'createdAt': '2023-01-01T00:00:00',
            'updatedAt': '2023-01-01T00:00:00'
        })

        event = {
            'httpMethod': 'PUT',
            'path': f'/users/{TEST_USER_ID}',
            'pathParameters': {'userid': TEST_USER_ID},
            'queryStringParameters': None,
            'body': json.dumps({
                'name': 'Updated Handler User',
                'email': 'updated@example.com'
            })
        }

        response = app.lambda_handler(event, {})
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['name'] == 'Updated Handler User'

    def test_lambda_handler_delete(self, dynamodb_table):
        """Test lambda_handler for DELETE"""
        dynamodb_table.put_item(Item=TEST_USER)

        event = {
            'httpMethod': 'DELETE',
            'path': f'/users/{TEST_USER_ID}',
            'pathParameters': {'userid': TEST_USER_ID},
            'queryStringParameters': None
        }

        response = app.lambda_handler(event, {})
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert 'deleted successfully' in body['message']

    def test_lambda_handler_invalid_method(self, dynamodb_table):
        """Test lambda_handler with an invalid HTTP method"""
        event = {
            'httpMethod': 'PATCH',
            'path': '/users',
            'pathParameters': None,
            'queryStringParameters': None
        }

        response = app.lambda_handler(event, {})
        body = json.loads(response['body'])

        assert response['statusCode'] == 405
        assert 'Method not allowed' in body['message']

Reference Code - conftest.py
1
2
3
4
5
6
7
8
"""
Pytest configuration file for user tests
"""
import os
import sys

# Add the src directory to the Python path so we can import the app module
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/users'))

Setting Up and Running Tests
Now let Claude Code set up the test environment and run the tests for you:

Set up a Python virtual environment in the workshop directory, install the test dependencies from requirements-dev.txt, and run the unit tests with verbose output. Show me the results.

Claude Code will execute each step:

Create a virtual environment:

cd ~/workspace/my-workspace/workshop
python -m venv venv

Activate and install dependencies:

source venv/bin/activate
pip install -r requirements-dev.txt

Run the tests:

pytest tests/unit/users/test_app.py -v

Run with coverage:

pytest tests/unit/users/test_app.py --cov=src/users -v

Deactivate when done:

deactivate

Claude Code handles failures too
If any tests fail, Claude Code will read the error output, analyze the mismatch between the test expectations and your actual code, and suggest fixes. This is the agentic debugging loop in action. No need to manually compare expected vs. actual values.

Keep Building with Claude Code
Now that you have the basics down, here's where the real fun begins! Claude Code is your coding companion. Think of it as having a senior developer sitting right next to you in the terminal.

Start Small, Dream Big
Don't try to build everything at once. Have a conversation with Claude Code:

I want to add input validation to my users API. What should I validate first?
My tests are passing, but I want to add error handling for edge cases. Show me the most common errors I should handle.
Make It Your Own
Every project is different, and Claude Code understands your specific code:

I want to add a 'last_login' field to my users. Update both the Lambda function and the tests.
Notice the difference from a traditional assistant? Claude Code will read your actual files, make the edits directly, and update the tests, all in one conversation turn.

Learn as You Go
Explain why mocking is important in testing. Show me how moto works by walking through my test fixtures.
What is test-driven development? How would I use that approach with my users API?
When Things Break
Don't panic! Just describe what happened:

My test is failing with this error: [paste error]. What's wrong and how do I fix it?
Claude Code will read the error, examine the relevant source file, and fix the issue directly.

Level Up
Ready for more? Just ask:

Add integration tests that hit my deployed API endpoint with real HTTP calls.
Show me how to add performance testing to my serverless application.
Pro Tip: Be specific!
The more specific your requests, the better Claude Code can help. Instead of "fix my code," try "my GET /users endpoint returns 500 when the database is empty. How should I handle this?" Claude Code will read the relevant code, understand the issue, and apply the fix.

Congratulations! You have built a complete serverless Users Service with Claude Code: infrastructure, application code, authentication, and tests. You experienced agentic development: describing what you want, reviewing proposals, and letting Claude Code do the typing and the running.
Ready to clean up your resources? Head to the cleanup section. Or explore the MCP module to extend your tools with AI agents!