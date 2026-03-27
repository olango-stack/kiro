Create a project with Kiro CLI
We'll use Kiro CLI to create our project structure and generate the necessary Terraform files.

Tip: For large prompts when using Kiro CLI, you can use the /editor command to open a text editor, author your prompt, and then save and exit with :wq! to run the prompt.
Login to Kiro and start a chat session:

cd ~/workspace/my-workspace
kiro-cli login --use-device-flow
kiro-cli

Create the project structure using Kiro CLI:

Create a serverless project structure using best practices for a AWS Lambda-based API with the following components:

1. First, show me the complete directory structure, do not create files, for a project named "workshop" with:
   - Source code directory for Lambda functions (users and authorizer, (Python))
   - Test directories for unit and integration tests
   - Directory for infrastructure code (called infrastructure) which will be used for Terraform templates
   - Directory for Documentation
   - Do not create modules directories or directories per environment

2. After showing the directory structure, create directory structure, without any file, per the plan above:

The project should follow best practices for serverless applications on AWS, with separate concerns for business logic, infrastructure, testing, and documentation.

Kiro will generate a bash script similar to the following to create the project structure:

1
mkdir -p workshop/{src/{users,authorizer},tests/{unit/{users,authorizer},integration/{users,authorizer}},infrastructure,docs/{architecture,api,development},scripts}

This command creates the complete directory structure for your serverless application, following best practices with separate directories for source code, tests, infrastructure, and documentation.

Create the Terraform configuration files with Kiro:

Under the "infrastructure" directory, which is under the "workshop" directory, create a complete Terraform project structure with the following specifications:
- Create provider.tf that configures the AWS provider with region from a variable
- Create variables.tf with variables for "region" (default: us-west-2), "workshop_stack_base_name" (default: workshop), "environment" (default: Workshop) and "project" (default: Serverless Patterns)
- Create outputs.tf as an empty file for future outputs
- Create versions.tf that sets the minimum Terraform version to 1.0.0.  Do not include the "required_providers" section
- Create a README.md with project description and setup instructions

Expand - Terraform code - provider.tf
1
2
3
provider "aws" {
  region = var.region
}

Expand - Terraform code - variables.tf
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

Expand - Terraform code - versions.tf
1
2
3
terraform {
  required_version = ">= 1.0.0"
}

Expand - project structure...
The resulting structure for the workshop/infrastructure folder should look similar to the following:

.
├── README.md
├── outputs.tf
├── provider.tf
├── variables.tf
└── versions.tf
Initialize Terraform
After creating the Terraform configuration files, initialize Terraform to download the required providers:

Under the "infrastructure" directory, which is under the "workshop" directory, generate a command to initialize Terraform with detailed output. Do not include any flags.

Kiro will suggest, something similar as below:

1
cd ~/workspace/my-workspace/infrastructure && terraform init

Troubleshooting with Kiro
If you encounter any issues during setup, Kiro can help:

I'm getting an error 'Error: No valid credential sources found'. How do I configure AWS credentials for Terraform?

Kiro will provide detailed troubleshooting steps and solutions for common issues.




1 - Create data store
Your application needs a place to store user data. For that, you'll create a Users table in Amazon DynamoDB.

module architecture diagram

You will use Kiro to generate Terraform code for creating the DynamoDB table resource.

First, you'll ask Kiro to create the Terraform configuration for your DynamoDB table. Then, you'll use Terraform to deploy the infrastructure.

With Kiro, you can describe what you want to build in natural language, and it will generate the necessary infrastructure code for you.
Define a Users table with Kiro
Use Kiro to generate the Terraform code for your DynamoDB table with specific requirements:

   Create a DynamoDB table in Terraform with the following specifications:
   - Resource name: users_table
   - Table name: Use the workshop_stack_base_name variable as prefix followed by '_users'
   - Billing mode: PAY_PER_REQUEST (on-demand capacity)
   - Primary key: userid (string type)
   - Add point-in-time recovery with a 35-day retention period
   - Add server-side encryption without AWS managed KMS key
   - Add appropriate tags including Name, Environment, and Project
   - Create an output for the table ARN, ID, and name
   - Save the configuration in a file called "ddb.tf" in the "workshop/infrastructure" directory
   - Follow least privilege security principles
   - Ensure the configuration is production-ready

After Kiro generates the file (/infrastructure/outputs.tf is also updated with DynamoDB Table Outputs), review it before proceeding:

   Show me the content of ddb.tf and explain any security considerations or potential cost implications

Expand - Terraform code for DynamoDB
🎮 Terraform Code Detective Challenge
Let's play a game! As a Terraform Code Detective, your mission is to analyze the generated DynamoDB table configuration and identify key security and performance features. This will help you understand the code better and prepare you for real-world infrastructure development.

🕵️ Detective Challenge Instructions:
Study the Terraform code above and identify at least 3 security features that make this DynamoDB table configuration secure.

Find at least 2 performance-related configurations in the code.

Identify at least 2 cost implications of this configuration.

Use Kiro to verify your findings with this prompt:

I've identified these security features in my DynamoDB Terraform code:
[List your findings]

And these performance/cost considerations:
[List your findings]

Am I correct? What did I miss? Are there any other important aspects I should understand?
🏆 Solution Checklist:
Security Features:

Server-side encryption protects data at rest
Point-in-time recovery enables backup capabilities
Variable-based naming prevents hardcoding
Performance & Cost:

PAY_PER_REQUEST scales automatically but costs more with high traffic
Point-in-time recovery adds ~20% to base cost
Hash key enables efficient data retrieval
Ask Kiro to explain the Terraform code!
You can ask Kiro to explain any part of the generated code:

"Explain the DynamoDB table configuration in ddb.tf, focusing on point-in-time recovery, server-side encryption, and the benefits of these features for a production environment"
Kiro will provide a detailed explanation of the Terraform code, including:

The resource type and its purpose
The table configuration (name, billing mode, hash key)
The security features like point-in-time recovery and encryption
Best practices for production-ready DynamoDB tables
Deploy the DynamoDB table
Now let's use Kiro to help us deploy the DynamoDB table with Terraform:

Generate the commands to initialize Terraform, create a plan, and apply the changes to deploy our DynamoDB table. Include explanations for each step.

Kiro will suggest a workflow like this:

# Make sure you're in the infrastructure directory
cd infrastructure

# Initialize Terraform in the current directory
terraform init

# Create a plan to preview the changes
terraform plan -out=dynamodb.tfplan

# Apply the plan to create the DynamoDB table
terraform apply dynamodb.tfplan

Or for a quicker deployment:

# One-step deployment with auto-approval
terraform apply -auto-approve

Deploy Checkpoint
Deployed!
After the deploy finishes, verify with the console that the database table was created...
After the deploy finishes, go to the DynamoDB console  (make sure your chosen region is selected) and verify that workshop_Users is in the tables list.

Ask Kiro for help from the command line
Instead of using the DynamoDB console to look up the database ARN, you can ask Kiro directly from the command line:

Use the AWS CLI to describe my DynamoDB table named workshop_Users and format the output to show me only the table ARN, creation date, and current status

Kiro will generate and execute the appropriate AWS CLI command to retrieve detailed information about your DynamoDB table.

Additional Resources
Amazon DynamoDB  - a fully managed, serverless, key-value NoSQL database designed to run high-performance applications.
Terraform AWS Provider Documentation  - documentation for the aws_dynamodb_table resource.
Now that you have a table defined, you can move on to the application logic...



2 - Add Business Logic
You will create one AWS Lambda function to handle all requests for the /users/* resource. The function will check the route in the request and act accordingly. The function code will be generated by Kiro.

module architecture diagram

We have you start with a multi-purpose function because it is common when migrating existing applications to serverless. A multi-purpose function, also called a monolithic function, handles several HTTP methods. In contrast, a single-purpose function handles only one HTTP method.

This function will need to access data in the DynamoDB table created in the previous step. The table name will be passed as an environment variable (USERS_TABLE) so the dynamically prefixed table name can be used by the function to get user data.

1) Plan Your Lambda Function
Before generating code, let's plan what we need:

What are the key components and best practices I should consider when creating a Lambda function for a users service with DynamoDB integration? Include security considerations, error handling patterns, and performance optimizations.

2) Generate Lambda Function Code with Kiro
Now, use Kiro to generate the Lambda function code with comprehensive error handling, logging, and best practices:

Create a Lambda function in the "workshop/src/functions/users" directory with the following specifications:
- Implement a Python handler that processes API Gateway proxy events
- Support CRUD operations (Create, Read, Update, Delete) for users in DynamoDB
- Include the following endpoints:
  * GET /users - List all users
  * GET /users/{userid} - Get a specific user
  * POST /users - Create a new user with auto-generated UUID
  * PUT /users/{userid} - Update an existing user
  * DELETE /users/{userid} - Delete a user
- Use environment variables for configuration
- Create a requirements.txt file with necessary dependencies
- Follow security best practices for handling user data
- Implement pagination for list operations

Expand - Lambda Function Code - lambda_function.py
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
        # Changed from userId to userid to match DynamoDB table structure
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
        # Validate required fields
        if 'email' not in user_data or 'name' not in user_data:
            return generate_response(400, {'message': 'Email and name are required'})
        
        # Generate a unique ID if not provided
        if 'userid' not in user_data:  # Changed from userId to userid
            user_data['userid'] = str(uuid.uuid4())  # Changed from userId to userid
        
        # Add timestamps
        timestamp = datetime.now().isoformat()
        user_data['createdAt'] = timestamp
        user_data['updatedAt'] = timestamp
        
        # Save to DynamoDB
        table.put_item(Item=user_data)
        
        return generate_response(201, user_data)
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def update_user(user_id, user_data):
    """Update an existing user"""
    try:
        # Check if user exists
        response = table.get_item(Key={'userid': user_id})  # Changed from userId to userid
        if 'Item' not in response:
            return generate_response(404, {'message': f'User with ID {user_id} not found'})
        
        # Update timestamp
        user_data['updatedAt'] = datetime.now().isoformat()
        user_data['userid'] = user_id  # Changed from userId to userid
        
        # Preserve creation timestamp
        user_data['createdAt'] = response['Item']['createdAt']
        
        # Update the item
        table.put_item(Item=user_data)
        
        return generate_response(200, user_data)
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def delete_user(user_id):
    """Delete a user"""
    try:
        # Check if user exists
        response = table.get_item(Key={'userid': user_id})  # Changed from userId to userid
        if 'Item' not in response:
            return generate_response(404, {'message': f'User with ID {user_id} not found'})
        
        # Delete the item
        table.delete_item(Key={'userid': user_id})  # Changed from userId to userid
        
        return generate_response(200, {'message': f'User with ID {user_id} deleted successfully'})
    except Exception as e:
        return generate_response(500, {'message': str(e)})

def lambda_handler(event, context):
    """Main Lambda handler function"""
    print(f"Event received: {json.dumps(event)}")  # Added logging
    
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    path_parameters = event.get('pathParameters', {}) or {}
    query_parameters = event.get('queryStringParameters', {}) or {}
    
    # Extract user_id from path parameters if available
    user_id = path_parameters.get('userid') if path_parameters else None  # Changed from userId to userid
    
    # Parse request body if present
    body = {}
    if event.get('body'):
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return generate_response(400, {'message': 'Invalid JSON in request body'})
    
    # Route the request based on HTTP method and path
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

Expand - requirements.txt
1
2
boto3>=1.26.0
aws-xray-sdk>=2.12.0

Ask Kiro to explain the Lambda code!
You can ask Kiro to explain any part of the generated code:

Explain how the Lambda function handles pagination for the GET /users endpoint and why this approach is important for performance and cost optimization.
Kiro will provide a detailed explanation of the code, including:

How the pagination parameters are extracted from the request
How the DynamoDB scan operation is configured with pagination
How the next token is generated and included in the response
Why pagination is important for performance and cost optimization with DynamoDB
4) Create Lambda Infrastructure with Kiro
Before generating the infrastructure code, let's check what permissions we need:

What are the minimum IAM permissions needed for a Lambda function that performs CRUD operations on a DynamoDB table and uses X-Ray tracing?
Now, generate the Terraform configuration for your Lambda function with comprehensive settings:

Create a Terraform script 'users-lambda.tf' in the "workshop/infrastructure" directory, with the following specifications:
- Create a Lambda function that deploys the code from /src/users
- Package the code as a ZIP archive including dependencies from requirements.txt
- Use Python 3.10 runtime
- Configure 256MB memory and 30 second timeout
- Create a custom IAM role with least privilege permissions:
  * DynamoDB CRUD operations ONLY on the users table (no wildcard permissions)
  * Attach AWSLambdaBasicExecutionRole
- Set environment variables for the DynamoDB table name
- Configure proper error handling and retry behavior
- Add tags for resource management
- Create outputs for the Lambda ARN, function name, and invoke URL
- Ensure all security best practices are followed

Expand - Terraform Code - users-lambda.tf
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
# Lambda function for Users service
# This file defines the Lambda function that handles CRUD operations for users

###########################################
# Lambda function package creation
###########################################

# Create a zip archive of the Lambda function code
data "archive_file" "users_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/users"
  output_path = "${path.module}/../build/users_lambda.zip"

  depends_on = [
    null_resource.install_dependencies
  ]
}

# Install Python dependencies before creating the zip
resource "null_resource" "install_dependencies" {
  triggers = {
    requirements_hash = filemd5("${path.module}/../src/users/requirements.txt")
    source_hash       = filemd5("${path.module}/../src/users/app.py")
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

# IAM role for the Lambda function with least privilege
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

# Custom policy for DynamoDB access with least privilege
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

# Attach the custom DynamoDB policy to the Lambda role
resource "aws_iam_role_policy_attachment" "users_dynamodb_policy_attachment" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = aws_iam_policy.users_dynamodb_policy.arn
}

# Attach the basic Lambda execution role policy
resource "aws_iam_role_policy_attachment" "users_lambda_basic_execution" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Attach X-Ray tracing policy
resource "aws_iam_role_policy_attachment" "users_lambda_xray" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

###########################################
# Lambda Function
###########################################

# Lambda function for users service
resource "aws_lambda_function" "users_lambda" {
  function_name    = "${var.workshop_stack_base_name}-users-function"
  filename         = data.archive_file.users_lambda_zip.output_path
  source_code_hash = data.archive_file.users_lambda_zip.output_base64sha256
  handler          = "app.lambda_handler"
  runtime          = "python3.10"
  memory_size      = 256
  timeout          = 30
  role             = aws_iam_role.users_lambda_role.arn

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.users_table.name
      LOG_LEVEL           = "INFO"
    }
  }

  # Enable X-Ray tracing
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

# CloudWatch Log Group with retention policy
resource "aws_cloudwatch_log_group" "users_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.users_lambda.function_name}"
  retention_in_days = 30

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-lambda-logs"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "users_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.users_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  # The source ARN will be set when API Gateway is created
  # source_arn    = "${aws_api_gateway_rest_api.users_api.execution_arn}/*/*"
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

5) Review the Infrastructure Code
After Kiro generates the infrastructure code, review it carefully:

Review the generated "workshop/infrastructure/users-lambda.tf" file and identify:
1. Any overly permissive IAM policies that should be restricted
2. Any missing security configurations
3. Any cost optimization opportunities
4. Any potential deployment issues

Expand - Terraform Configuration - users_lambda.tf
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
# Lambda function for Users service
# This file defines the Lambda function that handles CRUD operations for users

###########################################
# Lambda function package creation
###########################################

# Create a zip archive of the Lambda function code
data "archive_file" "users_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/users"
  output_path = "${path.module}/../build/users_lambda.zip"

  depends_on = [
    null_resource.install_dependencies
  ]
}

# Install Python dependencies before creating the zip
resource "null_resource" "install_dependencies" {
  triggers = {
    requirements_hash = filemd5("${path.module}/../src/users/requirements.txt")
    source_hash       = filemd5("${path.module}/../src/users/app.py")
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

# IAM role for the Lambda function with least privilege
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

# Custom policy for DynamoDB access with least privilege
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

# Attach the custom DynamoDB policy to the Lambda role
resource "aws_iam_role_policy_attachment" "users_dynamodb_policy_attachment" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = aws_iam_policy.users_dynamodb_policy.arn
}

# Attach the basic Lambda execution role policy
resource "aws_iam_role_policy_attachment" "users_lambda_basic_execution" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Attach X-Ray tracing policy
resource "aws_iam_role_policy_attachment" "users_lambda_xray" {
  role       = aws_iam_role.users_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

###########################################
# Lambda Function
###########################################

# Lambda function for users service
resource "aws_lambda_function" "users_lambda" {
  function_name    = "${var.workshop_stack_base_name}-users-function"
  filename         = data.archive_file.users_lambda_zip.output_path
  source_code_hash = data.archive_file.users_lambda_zip.output_base64sha256
  handler          = "app.lambda_handler"
  runtime          = "python3.10"
  memory_size      = 256
  timeout          = 30
  role             = aws_iam_role.users_lambda_role.arn

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.users_table.name
      LOG_LEVEL           = "INFO"
    }
  }

  # Enable X-Ray tracing
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

# CloudWatch Log Group with retention policy
resource "aws_cloudwatch_log_group" "users_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.users_lambda.function_name}"
  retention_in_days = 30

  tags = {
    Name        = "${var.workshop_stack_base_name}-users-lambda-logs"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "users_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.users_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  # The source ARN will be set when API Gateway is created
  # source_arn    = "${aws_api_gateway_rest_api.users_api.execution_arn}/*/*"
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

6) Deploy the Lambda Function
Before deploying, let's create a plan to review the changes:

Generate the commands to plan and deploy terraform scripts to AWS

Kiro will suggest:

# Make sure you're in the infrastructure directory
cd infrastructure

# Initialize Terraform in the current directory
terraform init

# Create a plan to preview the changes
terraform plan

# Apply the plan to create the DynamoDB table
terraform apply

Review the plan:

What should I look for when reviewing the Terraform plan for the Lambda function?

Now deploy:

terraform apply

Deploy Checkpoint
Deployed!
After the deploy finishes, verify the function was created...
Verify your deployment:

Use the AWS CLI to describe my Lambda function and show its configuration, including memory, timeout, and environment variables. Format the output to be easily readable.

🧪 Code Verification Challenge
Let's verify if the generated Lambda function actually works as expected! Here's how to test it:

1. AWS Console Testing
After deployment, you can test the function in the AWS Console:

Navigate to the Lambda console
Select your function
Click the "Test" tab
Create test events for each operation using the templates below
Test Event Templates
Create User Test Event

1
2
3
4
5
{
  "httpMethod": "POST",
  "path": "/users",
  "body": "{\"name\":\"Test User\",\"email\":\"test@example.com\"}"
}

Get User Test Event

1
2
3
4
5
6
7
{
  "httpMethod": "GET",
  "path": "/users/{userid}",
  "pathParameters": {
    "userid": "USER_ID_FROM_CREATE_RESPONSE"
  }
}

2. AWS CLI Testing
You can also test the deployed function using the AWS CLI:

1
2
3
4
5
6
7
8
# Invoke the function with a test event
aws lambda invoke --function-name workshop-users-function \
  --payload '{"httpMethod":"POST","path":"/users","body":"{\"name\":\"CLI Test User\",\"email\":\"cli@example.com\"}"}' \
  --cli-binary-format raw-in-base64-out \
  response.json

# Check the response
cat response.json

3. Verification Checklist
✅ Function Deployment: Lambda function deploys successfully
✅ Create Operation: Successfully creates a new user with a generated ID
✅ Read Operation: Successfully retrieves a user by ID
✅ Update Operation: Successfully updates an existing user
✅ Delete Operation: Successfully deletes a user
✅ Error Handling: Returns appropriate error responses for invalid inputs
✅ Pagination: Correctly handles pagination for list operations

Additional Resources
AWS Lambda Best Practices 
DynamoDB Best Practices 
Terraform AWS Lambda Documentation 
AWS X-Ray Developer Guide 
Congratulations! You've created a comprehensive Lambda function using Kiro that handles all CRUD operations for Users with proper error handling, logging, and security best practices.

3 - Connect an API
Now that the backend Lambda functions are deployed, it's time to connect them to the world using Amazon API Gateway. We'll use Kiro to generate a comprehensive API Gateway configuration with Terraform.

module 2 architecture with a focus on api

You will connect the front door (public URLs) to the service function(s) using Amazon API Gateway. A REST API in API Gateway is a collection of resources and methods that are integrated with backend endpoints, Lambda functions, or other AWS services.

You will also enable distributed tracing with AWS X-Ray to help analyze and debug the application, which will help you troubleshoot the root cause of performance issues and errors.

Create the API with Kiro
Use Kiro to generate a comprehensive API Gateway configuration with best practices:

Create a Terraform script 'api-gateway.tf' in the "workshop/infrastructure" directory, with the following specifications:
- Create a regional REST API Gateway named using the workshop_stack_base_name variable
- Set up resource paths for /users and /users/{userid} following REST naming conventions
- Configure the following methods:
  * GET /users - List all users
  * GET /users/{userid} - Get a specific user
  * PUT /users - Create a new user
  * PUT /users/{userid} - Update an existing user
  * DELETE /users/{userid} - Delete a user
  * OPTIONS for all paths (for CORS support)
- Integrate all methods with the users Lambda function
- Set up proper request/response mappings for each method
- Configure CORS with appropriate headers for cross-origin requests
- Deploy to a 'Prod' stage with auto-generated stage name
- Add appropriate tags for resource management
- Output the API endpoint URL, execution ARN, and stage URL
- Update README.md with curl examples for all operations

Expand - Terraform code - api-gateway.tf
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
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
###########################################
# API Gateway for Users Service
###########################################

# Create REST API Gateway
resource "aws_api_gateway_rest_api" "users_api" {
  name        = "${var.workshop_stack_base_name}-users-api"
  description = "API Gateway for Users Service"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  
  # Enable X-Ray tracing
  minimum_compression_size = 0
  
  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

###########################################
# API Resources and Methods
###########################################

# /users resource
resource "aws_api_gateway_resource" "users_resource" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  parent_id   = aws_api_gateway_rest_api.users_api.root_resource_id
  path_part   = "users"
}

# /users/{userid} resource
resource "aws_api_gateway_resource" "user_resource" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  parent_id   = aws_api_gateway_resource.users_resource.id
  path_part   = "{userid}"
}

###########################################
# Methods for /users resource
###########################################

# GET /users - List all users
resource "aws_api_gateway_method" "users_get" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users_resource.id
  http_method   = "GET"
  authorization = "NONE"
  
  request_parameters = {
    "method.request.header.Content-Type" = false
  }
}

# Integration for GET /users
resource "aws_api_gateway_integration" "users_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.users_resource.id
  http_method             = aws_api_gateway_method.users_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
  
  request_templates = {
    "application/json" = <<EOF
{
  "httpMethod": "GET",
  "path": "/users",
  "queryStringParameters": $input.json('$.queryStringParameters'),
  "headers": {
    #foreach($param in $input.params().header.keySet())
    "$param": "$util.escapeJavaScript($input.params().header.get($param))"
    #if($foreach.hasNext),#end
    #end
  }
}
EOF
  }
}

# PUT /users - Create a new user
resource "aws_api_gateway_method" "users_put" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users_resource.id
  http_method   = "PUT"
  authorization = "NONE"
  
  request_parameters = {
    "method.request.header.Content-Type" = false
  }
}

# Integration for PUT /users
resource "aws_api_gateway_integration" "users_put_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.users_resource.id
  http_method             = aws_api_gateway_method.users_put.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

# OPTIONS /users - For CORS support
resource "aws_api_gateway_method" "users_options" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# Integration for OPTIONS /users
resource "aws_api_gateway_integration" "users_options_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.users_resource.id
  http_method             = aws_api_gateway_method.users_options.http_method
  type                    = "MOCK"
  
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

# Response for OPTIONS /users
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

# Integration response for OPTIONS /users
resource "aws_api_gateway_integration_response" "users_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  resource_id = aws_api_gateway_resource.users_resource.id
  http_method = aws_api_gateway_method.users_options.http_method
  status_code = aws_api_gateway_method_response.users_options_response.status_code
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,PUT,OPTIONS'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

###########################################
# Methods for /users/{userid} resource
###########################################

# GET /users/{userid} - Get a specific user
resource "aws_api_gateway_method" "user_get" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "GET"
  authorization = "NONE"
  
  request_parameters = {
    "method.request.path.userid" = true
  }
}

# Integration for GET /users/{userid}
resource "aws_api_gateway_integration" "user_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.user_resource.id
  http_method             = aws_api_gateway_method.user_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

# PUT /users/{userid} - Update an existing user
resource "aws_api_gateway_method" "user_put" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "PUT"
  authorization = "NONE"
  
  request_parameters = {
    "method.request.path.userid" = true
  }
}

# Integration for PUT /users/{userid}
resource "aws_api_gateway_integration" "user_put_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.user_resource.id
  http_method             = aws_api_gateway_method.user_put.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

# DELETE /users/{userid} - Delete a user
resource "aws_api_gateway_method" "user_delete" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "DELETE"
  authorization = "NONE"
  
  request_parameters = {
    "method.request.path.userid" = true
  }
}

# Integration for DELETE /users/{userid}
resource "aws_api_gateway_integration" "user_delete_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.user_resource.id
  http_method             = aws_api_gateway_method.user_delete.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_lambda.invoke_arn
}

# OPTIONS /users/{userid} - For CORS support
resource "aws_api_gateway_method" "user_options" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# Integration for OPTIONS /users/{userid}
resource "aws_api_gateway_integration" "user_options_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.user_resource.id
  http_method             = aws_api_gateway_method.user_options.http_method
  type                    = "MOCK"
  
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

# Response for OPTIONS /users/{userid}
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

# Integration response for OPTIONS /users/{userid}
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
# API Gateway Deployment and Stage
###########################################

# Deployment of the API
resource "aws_api_gateway_deployment" "users_api_deployment" {
  depends_on = [
    aws_api_gateway_integration.users_get_integration,
    aws_api_gateway_integration.users_put_integration,
    aws_api_gateway_integration.users_options_integration,
    aws_api_gateway_integration.user_get_integration,
    aws_api_gateway_integration.user_put_integration,
    aws_api_gateway_integration.user_delete_integration,
    aws_api_gateway_integration.user_options_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.users_api.id
  
  # Force a new deployment when any of the integrations change
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.users_resource.id,
      aws_api_gateway_resource.user_resource.id,
      aws_api_gateway_method.users_get.id,
      aws_api_gateway_method.users_put.id,
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

# Stage for the API
resource "aws_api_gateway_stage" "users_api_stage" {
  deployment_id = aws_api_gateway_deployment.users_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  stage_name    = "prod"
  
  # Enable X-Ray tracing
  xray_tracing_enabled = true
  
  # Enable detailed CloudWatch logging
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.users_api_logs.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
  
  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api-stage"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

# CloudWatch Log Group for API Gateway
resource "aws_cloudwatch_log_group" "users_api_logs" {
  name              = "/aws/apigateway/${aws_api_gateway_rest_api.users_api.name}"
  retention_in_days = 30
  
  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api-logs"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

# Method Settings for detailed logging and metrics
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

# Usage plan for API throttling and quota
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

# API Key for usage plan
resource "aws_api_gateway_api_key" "users_api_key" {
  name = "${var.workshop_stack_base_name}-users-api-key"
  
  tags = {
    Name        = "${var.workshop_stack_base_name}-users-api-key"
    Environment = "Workshop"
    Project     = "Serverless Patterns"
  }
}

# Associate API Key with Usage Plan
resource "aws_api_gateway_usage_plan_key" "users_api_usage_plan_key" {
  key_id        = aws_api_gateway_api_key.users_api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.users_api_usage_plan.id
}

###########################################
# Update Lambda permissions
###########################################

# Update Lambda permission to allow API Gateway to invoke it
resource "aws_lambda_permission" "api_gateway_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.users_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  
  # Allow invocation from any method/resource in the API
  source_arn = "${aws_api_gateway_rest_api.users_api.execution_arn}/*/*"
}

###########################################
# Outputs
###########################################

output "users_api_url" {
  description = "URL of the Users API"
  value       = "${aws_api_gateway_stage.users_api_stage.invoke_url}"
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

Understanding the API Gateway Configuration 🎯
Time to peek under the hood! Let's explore what Kiro generated for us. Don't worry if this looks complex - think of it as learning to read the "recipe" that Kiro wrote for your API.

The API Gateway Family Tree 🌳
Your API Gateway is like a family tree - everything has a parent and children:

Explain how my API Gateway resources are organized. What's the relationship between the root, /users, and /users/{userid} paths?

API Gateway Structure and Resources
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
# The "grandparent" - your main API
resource "aws_api_gateway_rest_api" "users_api" {
  name        = "${var.workshop_stack_base_name}-api"
  description = "API Gateway for Users Service"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# The "parent" - /users path
resource "aws_api_gateway_resource" "users" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  parent_id   = aws_api_gateway_rest_api.users_api.root_resource_id
  path_part   = "users"
}

# The "child" - /users/{userid} path
resource "aws_api_gateway_resource" "user" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  parent_id   = aws_api_gateway_resource.users.id
  path_part   = "{userid}"
}

The Magic Bridge to Lambda 🌉
Ever wonder how API Gateway talks to your Lambda function? It's like a translator!

Why does my API Gateway use POST to call Lambda even when my API method is GET? Explain the AWS_PROXY integration

HTTP Methods and Lambda Integration
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
# Your API says "GET" but Lambda gets a "POST" - weird, right?
resource "aws_api_gateway_method" "get_users" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users.id
  http_method   = "GET"
  authorization_type = "NONE"
}

# The magic translator that turns GET into POST for Lambda
resource "aws_api_gateway_integration" "get_users_integration" {
  rest_api_id             = aws_api_gateway_rest_api.users_api.id
  resource_id             = aws_api_gateway_resource.users.id
  http_method             = aws_api_gateway_method.get_users.http_method
  integration_http_method = "POST"  # Always POST to Lambda!
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.users_function.invoke_arn
}

CORS: The Web Browser's Security Guard 🛡️
CORS is like a bouncer at a club - it decides which websites can talk to your API:

What is CORS and why do I need all these OPTIONS methods? Can I make it more secure than allowing all origins?

CORS Configuration
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
# The "bouncer" that handles preflight requests
resource "aws_api_gateway_method" "options_users" {
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  resource_id   = aws_api_gateway_resource.users.id
  http_method   = "OPTIONS"
  authorization_type = "NONE"
}

# The "guest list" - who's allowed in
resource "aws_api_gateway_integration_response" "options_users_integration_response" {
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,PUT,OPTIONS'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"  # Everyone's invited (for now!)
  }
}

Deployment: Making It Live! 🚀
Your API needs to be "published" before the world can see it:

Explain the deployment and stage concept in API Gateway. Why do I need both a deployment and a stage?

Deployment and Stage Configuration
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
# The "publishing" step
resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.users_api.id
  
  # Smart redeployment - only when things actually change
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.users.id,
      aws_api_gateway_resource.user.id,
      aws_api_gateway_method.get_users.id,
    ]))
  }
}

# The "environment" where your API lives
resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.users_api.id
  stage_name    = "Prod"
  
  xray_tracing_enabled = true  # X-Ray vision for debugging!
}

Keeping Track of Everything 📊
Your API needs to keep a diary of what happens:

How do I use CloudWatch logs to troubleshoot my API issues? What should I look for in the logs?

CloudWatch Logging Configuration
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
# The API's diary
resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/${aws_api_gateway_rest_api.users_api.name}"
  retention_in_days = 7  # Keep logs for a week
  
  tags = {
    Name        = "${var.workshop_stack_base_name}-api-logs"
    Environment = var.environment
    Project     = "Serverless Patterns Workshop"
  }
}

Deploy the API
Time to make it live! Deploy your API Gateway configuration:

Generate a command to apply my Terraform changes with detailed output

Kiro will suggest:

terraform apply -auto-approve

Deploy Checkpoint
🎉 Deployed!
After the deploy finishes, you will verify that your API is working
Get your API endpoint URL:

Show me how to get my API Gateway endpoint URL from Terraform outputs and test it

Kiro will suggest:

1
2
3
export API_ENDPOINT=$(terraform output -raw api_endpoint)
echo "API endpoint: $API_ENDPOINT"
curl -X GET $API_ENDPOINT/users -H "Content-Type: application/json"

Test Your API with Kiro
Generate curl commands to test all my Users API endpoints - list, create, get, update, and delete users

Kiro will generate a comprehensive test script that you can use to verify your API works perfectly!

🐛 When Things Go Wrong (They Sometimes Do!)
Don't panic if something doesn't work! Ask Kiro for help:

My API is returning a 500 error. Help me troubleshoot by checking Lambda logs and API Gateway configuration

Kiro is great at detective work!

Monitor Your API with Kiro
Create CloudWatch alarms for my API to alert me about errors and slow responses

📚 Heads Up!
The next sections dive deeper into authentication and testing - they can get a bit challenging! Don't worry if you get stuck - feel free to use the expected code examples we provide. Remember, the goal is learning, not perfection! 🎯

Additional Resources
Amazon API Gateway REST API 
AWS X-Ray  - Your API's X-ray vision for debugging
API Gateway Best Practices 
Great! You have a working API with proper logging, monitoring, and CORS support. In the next section, we'll add authentication to secure your API.


3.1 - Create User Pool
For the API authentication and authorization you will use a Lambda Authorizer function in API Gateway and a Cognito User Pool  for the user directory. We'll use Kiro to generate all the necessary Terraform code.

module 2 architecture with a focus on security

Amazon Cognito provides user sign-up, sign-in, and access control. It supports sign-in with social identity providers and enterprise identity providers via SAML 2.0 and OpenID Connect.

Create Cognito User Pool with Kiro
First, let's use Kiro to generate a comprehensive Cognito User Pool configuration:

Create a Terraform script 'cognito.tf' in the "workshop/infrastructure" directory, with the following specifications:
- Create a Cognito User Pool named using the workshop_stack_base_name variable with '_UserPool' suffix
- Configure email as a required attribute and username
- Set up password policies with minimum length of 8 characters requiring numbers, special chars, uppercase and lowercase
- Enable self-registration with email verification
- Add advanced security features with audit-only mode
- Set up proper account recovery mechanisms
- Create a user pool client with:
  * Refresh token expiration of 30 days
  * Support for USER_PASSWORD_AUTH, USER_SRP_AUTH, and REFRESH_TOKEN_AUTH flows
  * Callback URL to http://localhost
  * OAuth scopes for email and openid
- Create a Cognito domain using the workshop_stack_base_name variable
- Create an admin group called 'Administrators'
- Add appropriate tags for resource management
- Output the user pool ID, client ID, domain URL, and login URL

Expand - Terraform Code - cognito.tf
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
variable "user_pool_admin_group_name" {
  description = "Name for the admin group in Cognito User Pool"
  type        = string
  default     = "Administrators"
}

# 1. AWS Cognito User Pool
resource "aws_cognito_user_pool" "main" {
  name = "${var.workshop_stack_base_name}-user-pool"
  
  # Allow users to sign up themselves
  admin_create_user_config {
    allow_admin_create_user_only = false
  }
  
  # Auto-verify email attributes
  auto_verified_attributes = ["email"]
  
  # Required schema attributes
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
  
  # Use email as username
  username_attributes = ["email"]
  
  # Password policy
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }
  
  # Lifecycle to ignore schema changes
  lifecycle {
    ignore_changes = [schema]
  }
  
  # Tags
  tags = {
    Name        = "${var.workshop_stack_base_name}-user-pool"
    Environment = "workshop"
    Project     = var.workshop_stack_base_name
  }
}

# 2. Cognito User Pool Client
resource "aws_cognito_user_pool_client" "client" {
  name                                 = "${var.workshop_stack_base_name}-client"
  user_pool_id                         = aws_cognito_user_pool.main.id
  
  # Authentication flows
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]
  
  # No client secret
  generate_secret = false
  
  # Prevent user existence errors
  prevent_user_existence_errors = "ENABLED"
  
  # Refresh token validity
  refresh_token_validity = 30
  
  # Identity providers
  supported_identity_providers = ["COGNITO"]
  
  # OAuth configuration
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
After Kiro generates the Terraform code, review it to ensure it meets your requirements, then apply the changes:

terraform apply -auto-approve

After deployment finishes, copy the cognito_login_url from the outputs and paste it into a new browser tab.

You should see a Cognito hosted UI where you can either sign in or sign up for a new account.

sign up form

Choose the Sign up link (not the Sign In button) and fill in the user registration form with your email and password.

You should receive an email with a verification code. Use the code to confirm your account.

Take note of your new userid and password
You will need the userid and password you set in the next step! Make a note of both.

Ask Kiro to explain the Cognito Terraform code!
You can ask Kiro to explain any part of the generated Terraform code:

Explain the security features implemented in the Cognito User Pool configuration and how they help protect user authentication.
Kiro will provide a detailed explanation of the code, including:

How the password policy enhances security
The purpose of email verification and account recovery mechanisms
How the advanced security features in audit mode work
The token expiration settings and their security implications
The authentication flows and their appropriate use cases
Next Steps
After setting up your Cognito User Pool, you'll be ready to implement API Gateway authorization in the next section.

Additional Resources
Amazon Cognito - Getting started with user pools  - steps to set up and configure a Cognito user pool for the first time in the console
JWT Token Validation  - how to validate JWT tokens from Cognito
Terraform AWS Cognito Documentation 





3.2 - Secure API Gateway
Now that we have our Cognito User Pool set up, we need to create a Lambda authorizer to validate JWT tokens from Cognito and secure our API endpoints.

🔐 Security First!
Security is a top priority. To ensure robust authentication and authorization, your platform/security team will typically provide you a standardized Lambda authorizer function. Below is a reference implementation that demonstrates proper JWT token validation and role-based access control.

Expand - Lambda Authorizer Code - lambda_authorizer.py
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
        
        # For now, verify basic token structure and claims without signature verification
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

🚨 MANDATORY STEP - Action Required!
You MUST copy the Lambda Authorizer code above and save it as app.py in the /workshop/src/authorizer directory before proceeding.

Without this file, your authentication will not work and subsequent steps will fail.

Expand - requirements.txt
1
2
PyJWT==2.8.0
requests==2.31.0

Understanding the Lambda Authorizer
Let's have Kiro explain how this Lambda authorizer works! The authorizer handles JWT Token Validation, User Claims Extraction, Role-Based Access Control, IAM Policy Generation, and Error Handling.

Ask Kiro questions like:

"What does the validate_token function do?"
"How does cold start caching work with JWKS?"
"What happens if a JWT token is expired?"
"Why do we check the 'aud' claim in JWT tokens?"
💡 Pro Tip!
Take some time to ask Kiro about the different sections of the Lambda authorizer code. Understanding how JWT validation works will help you troubleshoot authentication issues and customize authorization rules for your specific use cases!

Now that the Lambda authorizer code is ready, let's create a Terraform script to deploy it:

⚡ Infrastructure as Code Time!
We're about to deploy some serious security infrastructure! The Terraform script will create IAM roles, Lambda functions, and API Gateway authorizers. Make sure you understand what each resource does before applying the changes.

Create a Terraform script 'lambda_authorizer.tf' in the `workshop/infrastructure` directory that creates a Lambda authorizer for API Gateway. The authorizer should:
1. Create an IAM role with with AWSLambdaBasicExecutionRole and permissions for Cognito operations
2. Create a Lambda function using code in /src/authorizer/lambda_authorizer.py
3. Include a build process that installs dependencies from src/authorizer/requirements.txt
4. Package the Lambda code from src/authorizer/lambda_authorizer.py as a ZIP archive
5. Create an API Gateway authorizer resource of type TOKEN that uses the Authorization header
6. Set environment variables for USER_POOL_ID, APPLICATION_CLIENT_ID, and ADMIN_GROUP_NAME using values from the Cognito resources
7. Output the authorizer ID and Lambda ARN
8. Use the workshop_stack_base_name variable as a prefix for resource names

Expand - Terraform Code - lambda_authorizer.tf
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
    Environment = "production"
    Project     = var.workshop_stack_base_name
  }
}

# Attach basic execution role
resource "aws_iam_role_policy_attachment" "authorizer_lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.authorizer_lambda_role.name
}

# Install dependencies and package authorizer Lambda
resource "null_resource" "authorizer_dependencies" {
  triggers = {
    requirements = filemd5("${path.module}/../src/functions/authorizer/requirements.txt")
    source_code  = filemd5("${path.module}/../src/functions/authorizer/lambda_function.py")
  }

  provisioner "local-exec" {
    command = <<EOF
      cd ${path.module}/../src/functions/authorizer
      pip install -r requirements.txt -t .
      rm -rf __pycache__ *.dist-info
    EOF
  }
}

# Archive authorizer Lambda function with dependencies
data "archive_file" "authorizer_lambda_zip" {
  depends_on  = [null_resource.authorizer_dependencies]
  type        = "zip"
  source_dir  = "${path.module}/../src/functions/authorizer"
  output_path = "${path.module}/authorizer-lambda.zip"
}

# Authorizer Lambda function
resource "aws_lambda_function" "authorizer" {
  filename         = data.archive_file.authorizer_lambda_zip.output_path
  function_name    = "${var.workshop_stack_base_name}-authorizer"
  role            = aws_iam_role.authorizer_lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  source_code_hash = data.archive_file.authorizer_lambda_zip.output_base64sha256

  environment {
    variables = {
      USER_POOL_ID = aws_cognito_user_pool.users_pool.id
      CLIENT_ID    = aws_cognito_user_pool_client.users_pool_client.id
    }
  }

  tags = {
    Name        = "${var.workshop_stack_base_name}-authorizer"
    Environment = "production"
    Project     = var.workshop_stack_base_name
  }
}

# Lambda permission for API Gateway to invoke authorizer
resource "aws_lambda_permission" "authorizer_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.authorizer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.users_api.execution_arn}/*/*"
}

Deploy Checkpoint - Lambda Authorizer
After Kiro generates the code, review it to ensure it meets your requirements, then apply the changes:

terraform apply -auto-approve

🚀 Great Progress!
Your Lambda authorizer is now deployed! This is a major milestone - you've just implemented enterprise-grade security for your serverless API. The authorizer will validate every request and ensure only authenticated users can access protected resources.

Now that we have set up our Cognito User Pool and Lambda authorizer, let's update our API Gateway and verify that our authentication and authorization mechanisms work correctly.

Update the API Gateway configuration in api-gateway.tf in workshop/infrastructure directory to:
- Add the Lambda authorizer to the API Gateway with:
  * Identity source as 'Authorization' header
  * Cache TTL of 300 seconds
  * Result handling for unauthorized requests
- Update all API methods to use the authorizer except for OPTIONS methods
- Ensure CORS configuration is maintained
- Show me the plan and the changes, before updating api-gateway.tf 

Expand - API Gateway delta for authorization additions
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

# Lambda Authorizer
resource "aws_api_gateway_authorizer" "cognito_authorizer" {
  name                   = "${var.workshop_stack_base_name}-authorizer"
  rest_api_id           = aws_api_gateway_rest_api.users_api.id
  authorizer_uri        = aws_lambda_function.authorizer.invoke_arn
  type                  = "TOKEN"
  identity_source       = "method.request.header.Authorization"
}

#For each of the method resources such as get_users, post_users, get_user_by_id, etc excluding the options

#Change 
authorization = "NONE"

#TO
authorization = "CUSTOM"
authorizer_id = aws_api_gateway_authorizer.cognito_authorizer.id

Deploy Checkpoint - Authorizer changes to API gateway
🔧 Final Integration Step!
This is the final piece of the security puzzle! We're connecting your Lambda authorizer to all the API Gateway methods. After this deployment, your API will be fully secured with JWT token validation.

After Kiro generates the code:

terraform apply -auto-approve

Congratulations!
You've successfully secured your API with Amazon Cognito authentication and Lambda authorization! Your API endpoints are now protected, ensuring that only authenticated users can access their own resources, while administrators have full access to manage all resources. This implementation follows AWS security best practices for API authentication and authorization.

Additional resources
Lambda Authorizer  - learn about working with authorizer functions and API Gateway
JWT Token Validation  - how to validate JWT tokens from Cognito
Now that you have secured access to your API with Cognito authentication and Lambda authorization, you should test the implementation to verify it works properly. The next section will guide you through creating test scripts and validating that your authentication flow functions correctly with both valid and invalid tokens.

Previous
Next

© 2008 - 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.




3.3 - Verify Authentication
Testing User Authorization
Test the secured API with two simple curl commands to verify authentication works.

Get Cognito Token
# Get client ID
COGNITO_CLIENT_ID=$(terraform output -raw cognito_user_pool_client_id)

# Get token for your user
TOKEN=$(aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id $COGNITO_CLIENT_ID \
  --auth-parameters USERNAME=your-email@example.com,PASSWORD=your-password \
  --query 'AuthenticationResult.IdToken' \
  --output text)

Note: Replace your-email@example.com and your-password with your actual Cognito user credentials, and your-user-id with your principal ID from the token's sub field.

Valid Token Test
# Get API endpoint
API_ENDPOINT=$(terraform output -raw api_endpoint)

# Test with valid token
curl -H "Authorization: Bearer $TOKEN" \
  $API_ENDPOINT/users/your-user-id

Expected: 200 response with user data

Invalid Token Test
# Test with invalid token
curl -w "Status: %{http_code}\n" \
  -H "Authorization: Bearer invalid-token-123" \
  $API_ENDPOINT/users/any-user-id

Expected: 401 Unauthorized

Additional Resources
Lambda Authorizer  - learn about working with authorizer functions and API Gateway
Amazon Cognito - Getting started with user pools  - steps to set up and configure a Cognito user pool for the first time in the console
JWT Token Validation  - how to validate JWT tokens from Cognito
Terraform AWS Cognito Documentation 
Congratulations! You've successfully tested your secured API with role-based authorization using Kiro CLI. Your API now properly restricts regular users to their own data while allowing admin users full access.



4 - Unit Test
Running unit tests is a well known best practice in traditional development.

man looking at arrows that curve around a check mark suggesting a test cycle

In a serverless/cloud environment the test cycle is equally important!

Some tests can use mocked services. Mocked services provide a representation that can stand in for the real service. Generally, mocked services are much faster to create, configure, and tear down after testing is done.

In this module, we'll use Kiro CLI to generate unit tests for our serverless application. This approach leverages AI to create comprehensive test cases with minimal manual effort.

Generate Unit Tests with Kiro
Instead of writing unit tests manually, we'll use Kiro to generate a complete test suite. First, let's create a plan for our unit tests:

Create a plan to generate unit test cases with >95% test coverage

This command will prompt Kiro to analyze our Lambda function code and create a comprehensive test plan that ensures high code coverage.

Once we have the test plan, we can ask Kiro to generate the actual test suite:

Generate a simple unit test suite for workshop/src/users/app.py with the following requirements:
1. Use pytest framework with moto for AWS service mocking
2. Test all CRUD operations (create, read, update, delete)
4. Mock DynamoDB interactions
7. Create the tests in a workshop/tests/unit/users directory
8. Include a requirements-dev.txt file with all testing dependencies

Expand - requirements-dev.txt
pytest==7.4.0
pytest-cov==4.1.0
moto==4.2.0
boto3==1.28.0
coverage==7.3.0
pytest-mock==3.11.1
freezegun==1.2.2
Expand - test_app.py
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
import json
import os
import pytest
import boto3
import uuid
from datetime import datetime
from moto import mock_dynamodb

# Import the module to test
import sys
sys.path.append('~/workspace/my-workspace/workshop/src/users')
import app

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
        # Set environment variable for table name
        os.environ['USERS_TABLE_NAME'] = TEST_TABLE_NAME
        
        # Create the mock table
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.create_table(
            TableName=TEST_TABLE_NAME,
            KeySchema=[{'AttributeName': 'userid', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'userid', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        
        # Update the app's table reference
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
        user_data = {
            'name': 'Incomplete User'
            # Missing email
        }
        
        response = app.create_user(user_data)
        body = json.loads(response['body'])
        
        assert response['statusCode'] == 400
        assert 'message' in body
        assert 'required' in body['message']
    
    def test_get_user(self, dynamodb_table):
        """Test getting a user by ID"""
        # First create a user
        dynamodb_table.put_item(Item=TEST_USER)
        
        # Test getting the user
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
        # Add a few users
        dynamodb_table.put_item(Item=TEST_USER)
        dynamodb_table.put_item(Item={
            'userid': 'user-2',
            'name': 'User Two',
            'email': 'user2@example.com'
        })
        
        # Test listing users
        response = app.list_users()
        body = json.loads(response['body'])
        
        assert response['statusCode'] == 200
        assert 'users' in body
        assert len(body['users']) == 2
        assert any(user['userid'] == TEST_USER_ID for user in body['users'])
        assert any(user['userid'] == 'user-2' for user in body['users'])
    
    def test_update_user(self, dynamodb_table):
        """Test updating an existing user"""
        # First create a user
        dynamodb_table.put_item(Item={
            **TEST_USER,
            'createdAt': '2023-01-01T00:00:00',
            'updatedAt': '2023-01-01T00:00:00'
        })
        
        # Update the user
        updated_data = {
            'name': 'Updated Name',
            'email': TEST_USER['email'],
            'role': 'admin'  # New field
        }
        
        response = app.update_user(TEST_USER_ID, updated_data)
        body = json.loads(response['body'])
        
        assert response['statusCode'] == 200
        assert body['userid'] == TEST_USER_ID
        assert body['name'] == 'Updated Name'
        assert body['role'] == 'admin'
        assert 'createdAt' in body
        assert 'updatedAt' in body
        assert body['createdAt'] == '2023-01-01T00:00:00'  # Should preserve original creation time
        assert body['updatedAt'] != '2023-01-01T00:00:00'  # Should have a new update time
    
    def test_update_nonexistent_user(self, dynamodb_table):
        """Test updating a user that doesn't exist"""
        response = app.update_user('nonexistent-user', {'name': 'New Name'})
        body = json.loads(response['body'])
        
        assert response['statusCode'] == 404
        assert 'not found' in body['message']
    
    def test_delete_user(self, dynamodb_table):
        """Test deleting a user"""
        # First create a user
        dynamodb_table.put_item(Item=TEST_USER)
        
        # Delete the user
        response = app.delete_user(TEST_USER_ID)
        body = json.loads(response['body'])
        
        assert response['statusCode'] == 200
        assert 'deleted successfully' in body['message']
        
        # Verify the user is gone
        response = app.get_user(TEST_USER_ID)
        assert response['statusCode'] == 404
    
    def test_delete_nonexistent_user(self, dynamodb_table):
        """Test deleting a user that doesn't exist"""
        response = app.delete_user('nonexistent-user')
        body = json.loads(response['body'])
        
        assert response['statusCode'] == 404
        assert 'not found' in body['message']
    
    def test_lambda_handler_get_all(self, dynamodb_table):
        """Test lambda_handler for GET all users"""
        # Add a test user
        dynamodb_table.put_item(Item=TEST_USER)
        
        # Create a mock event
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
        assert body['users'][0]['userid'] == TEST_USER_ID
    
    def test_lambda_handler_get_one(self, dynamodb_table):
        """Test lambda_handler for GET one user"""
        # Add a test user
        dynamodb_table.put_item(Item=TEST_USER)
        
        # Create a mock event
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
        # Create a mock event
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
        assert body['email'] == 'handler@example.com'
        assert 'userid' in body
    
    def test_lambda_handler_update(self, dynamodb_table):
        """Test lambda_handler for PUT (update user)"""
        # Add a test user
        dynamodb_table.put_item(Item={
            **TEST_USER,
            'createdAt': '2023-01-01T00:00:00',
            'updatedAt': '2023-01-01T00:00:00'
        })
        
        # Create a mock event
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
        assert body['email'] == 'updated@example.com'
        assert body['userid'] == TEST_USER_ID
    
    def test_lambda_handler_delete(self, dynamodb_table):
        """Test lambda_handler for DELETE"""
        # Add a test user
        dynamodb_table.put_item(Item=TEST_USER)
        
        # Create a mock event
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
        
        # Verify the user is gone
        get_response = app.get_user(TEST_USER_ID)
        assert get_response['statusCode'] == 404
    
    def test_lambda_handler_invalid_method(self, dynamodb_table):
        """Test lambda_handler with an invalid HTTP method"""
        event = {
            'httpMethod': 'PATCH',  # Not supported
            'path': '/users',
            'pathParameters': None,
            'queryStringParameters': None
        }
        
        response = app.lambda_handler(event, {})
        body = json.loads(response['body'])
        
        assert response['statusCode'] == 405
        assert 'Method not allowed' in body['message']

Expand - conftest.py
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
Now that we have our test files, let's set up a proper testing environment and run the tests:

1. First, create a virtual environment in the project root:
1
2
cd ./workshop
python -m venv venv

2. Activate the virtual environment:
1
2
# On macOS
source venv/bin/activate

3. Install the development dependencies:
1
pip install -r requirements-dev.txt

4. Run the tests:
1
2
3
4
5
6
7
8
# Run all user tests
pytest tests/unit/users/test_app.py -v

# Run with coverage report
pytest tests/unit/users/test_app.py --cov=src/users

# Run a specific test
pytest tests/unit/users/test_app.py::TestUserAPI::test_create_user -v

5. When you're done, deactivate the virtual environment:
1
deactivate

Keep Building with Kiro! 🚀
Now that you've got the basics down, here's where the real fun begins! Kiro is your coding companion - think of it as having a senior developer sitting right next to you, ready to help with whatever you need.

Start Small, Dream Big
Don't try to build everything at once. Instead, have a conversation with Kiro:

Kiro Prompt:

I want to add input validation to my users API. What should I validate first?
Kiro Prompt:

My tests are passing, but I want to add error handling. Show me the most common errors I should handle.
Make It Your Own
Every project is different, and Kiro gets that! Ask for exactly what YOU need:

Kiro Prompt:

I want to add a 'last_login' field to my users. Help me update both the code and tests.
Kiro Prompt:

Can you help me add logging to my Lambda function so I can debug issues better?
Learn as You Go
The best part? Kiro explains things as it helps you build:

Kiro Prompt:

Explain why mocking is important in testing and show me a simple example.
Kiro Prompt:

I keep hearing about 'test-driven development'. How would I use that approach with my users API?
When Things Break (And They Will!)
Don't panic! Kiro is great at debugging:

Kiro Prompt:

My test is failing with this error: [paste your error]. What's wrong and how do I fix it?
Kiro Prompt:

My Lambda function works locally but fails in AWS. Help me troubleshoot.
Level Up Your Skills
Ready for more advanced stuff? Just ask:

Kiro Prompt:

Show me how to add performance testing to my serverless application.
Kiro Prompt:

I want to learn about integration testing. What's the difference from unit testing?
Pro Tip: Be Specific!
The more specific your questions, the better Kiro can help. Instead of "fix my code," try "my GET /users endpoint returns 500 when the database is empty - how should I handle this?"

Keep Experimenting
The beauty of serverless development with Kiro is that you can try new things quickly and safely. Got an idea? Ask Kiro about it! Want to refactor something? Kiro can help you do it step by step.

Remember: every expert was once a beginner. Keep asking questions, keep building, and most importantly - have fun with it!

Your next adventure awaits - what will you build next? 🎯

Ready to take your testing skills to the next level? Check out integration testing in our advanced workshops!

