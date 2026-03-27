# Requirements Document

## Introduction

This document defines the requirements for the AnyCompany Customer Management API — an MVP serverless platform that provides secure CRUD operations for customer data. The system replaces fragmented spreadsheets and legacy systems with a single, authoritative REST API backed by AWS Lambda and API Gateway. Access is restricted to authorized users authenticated via AWS Cognito.

## MVP Scope

### In Scope
- User authentication via AWS Cognito User Pool
- Basic CRUD operations for customer records
- REST API endpoints exposed through API Gateway

### Out of Scope (Post-MVP)
- Advanced search and filtering
- Audit logging and change history
- Multi-tenancy support

## Glossary

- **API**: The Customer Management REST API exposed via AWS API Gateway
- **Authorizer**: The Lambda Authorizer function that validates Cognito-issued JWT tokens on every inbound request
- **Cognito_User_Pool**: The AWS Cognito User Pool that serves as the identity provider for the API
- **Customer**: A record representing an individual or organization managed by AnyCompany
- **Customer_ID**: A system-generated unique identifier (UUID) assigned to each Customer record
- **Customer_Lambda**: The AWS Lambda function that handles customer CRUD business logic
- **Data_Store**: The persistence layer (DynamoDB table) that stores Customer records
- **JWT**: JSON Web Token issued by the Cognito_User_Pool and used as the bearer token for authenticating API requests
- **Caller**: Any client (customer service rep, sales team member, or internal application) invoking the API

## Requirements

### Requirement 1: Customer Creation

**User Story:** As a customer service representative, I want to create a new customer record, so that I can onboard new customers into the centralized system.

#### Acceptance Criteria

1. WHEN a Caller sends a POST request to `/customers` with a valid request body, THE Customer_Lambda SHALL create a new Customer record in the Data_Store and return the created record with a generated Customer_ID and HTTP 201 status.
2. WHEN a Caller sends a POST request to `/customers` with a missing required field, THE Customer_Lambda SHALL return an HTTP 400 status with a descriptive error message identifying the missing field.
3. WHEN a Caller sends a POST request to `/customers` with an email address that already exists in the Data_Store, THE Customer_Lambda SHALL return an HTTP 409 status with an error message indicating the conflict.
4. THE Customer_Lambda SHALL assign a unique Customer_ID (UUID v4) to each newly created Customer record.

---

### Requirement 2: Customer Retrieval

**User Story:** As a sales team member, I want to retrieve customer records by ID, so that I can quickly access accurate customer information.

#### Acceptance Criteria

1. WHEN a Caller sends a GET request to `/customers/{customer_id}` with a valid Customer_ID, THE Customer_Lambda SHALL return the matching Customer record with HTTP 200 status.
2. WHEN a Caller sends a GET request to `/customers/{customer_id}` with a Customer_ID that does not exist in the Data_Store, THE Customer_Lambda SHALL return an HTTP 404 status with a descriptive error message.
3. WHEN a Caller sends a GET request to `/customers` without a Customer_ID, THE Customer_Lambda SHALL return a paginated list of all Customer records with HTTP 200 status.
4. THE Customer_Lambda SHALL return Customer records in JSON format conforming to the defined Customer schema.

---

### Requirement 3: Customer Update

**User Story:** As a customer service representative, I want to update an existing customer record, so that I can keep customer information accurate and current.

#### Acceptance Criteria

1. WHEN a Caller sends a PUT request to `/customers/{customer_id}` with a valid Customer_ID and valid request body, THE Customer_Lambda SHALL update the matching Customer record in the Data_Store and return the updated record with HTTP 200 status.
2. WHEN a Caller sends a PUT request to `/customers/{customer_id}` with a Customer_ID that does not exist in the Data_Store, THE Customer_Lambda SHALL return an HTTP 404 status with a descriptive error message.
3. WHEN a Caller sends a PUT request to `/customers/{customer_id}` with an invalid field value, THE Customer_Lambda SHALL return an HTTP 400 status with a descriptive error message identifying the invalid field.
4. THE Customer_Lambda SHALL preserve the original Customer_ID and creation timestamp when updating a Customer record.
5. WHEN a Caller sends a PUT request to `/customers/{customer_id}` with an email address that already exists in the Data_Store for a different Customer record, THE Customer_Lambda SHALL return an HTTP 409 status with an error message indicating the conflict.

---

### Requirement 4: Customer Deletion

**User Story:** As a customer service representative, I want to delete a customer record, so that I can remove outdated or erroneous entries from the system.

#### Acceptance Criteria

1. WHEN a Caller sends a DELETE request to `/customers/{customer_id}` with a valid Customer_ID that exists in the Data_Store, THE Customer_Lambda SHALL delete the matching Customer record and return HTTP 204 status with no response body.
2. WHEN a Caller sends a DELETE request to `/customers/{customer_id}` with a Customer_ID that does not exist in the Data_Store, THE Customer_Lambda SHALL return an HTTP 404 status with a descriptive error message.

---

### Requirement 5: Authentication and Authorization

**User Story:** As a system administrator, I want all API requests to be authenticated via AWS Cognito, so that only authorized users can access or modify customer data.

#### Acceptance Criteria

1. WHEN a Caller sends a request to any API endpoint without a JWT bearer token, THE Authorizer SHALL reject the request and return an HTTP 401 status.
2. WHEN a Caller sends a request with an expired JWT token issued by the Cognito_User_Pool, THE Authorizer SHALL reject the request and return an HTTP 401 status.
3. WHEN a Caller sends a request with a JWT token that fails Cognito_User_Pool signature verification, THE Authorizer SHALL reject the request and return an HTTP 403 status.
4. WHEN a Caller sends a request with a valid JWT token issued by the Cognito_User_Pool, THE Authorizer SHALL allow the request to proceed to the Customer_Lambda.
5. THE Authorizer SHALL validate JWT tokens against the Cognito_User_Pool JWKS endpoint on every inbound request to the API before the request reaches the Customer_Lambda.
6. THE Authorizer SHALL verify that the JWT token's `iss` claim matches the configured Cognito_User_Pool issuer URL and that the `aud` claim matches the configured API client ID.

---

### Requirement 6: Customer Data Schema

**User Story:** As an internal application developer, I want a consistent customer data schema, so that I can reliably integrate with the API.

#### Acceptance Criteria

1. THE Customer_Lambda SHALL enforce that every Customer record contains the following required fields: `customer_id` (UUID), `first_name` (string), `last_name` (string), `email` (string, valid email format), `created_at` (ISO 8601 timestamp), `updated_at` (ISO 8601 timestamp).
2. THE Customer_Lambda SHALL accept the following optional fields on a Customer record: `phone` (string), `company` (string), `notes` (string).
3. WHEN a Caller provides a field value that does not conform to the defined type or format, THE Customer_Lambda SHALL return an HTTP 400 status with a descriptive validation error.
4. THE Data_Store SHALL enforce that the `email` field is unique across all Customer records system-wide, such that no two Customer records may share the same email address at any point in time.

---

### Requirement 7: Error Handling and Observability

**User Story:** As a system operator, I want consistent error responses and structured logs, so that I can diagnose and resolve issues quickly.

#### Acceptance Criteria

1. IF an unhandled exception occurs in the Customer_Lambda, THEN THE Customer_Lambda SHALL return an HTTP 500 status with a generic error message and SHALL NOT expose internal stack traces to the Caller.
2. THE Customer_Lambda SHALL emit structured JSON log entries for every request, including the HTTP method, resource path, Customer_ID (when applicable), response status code, and request duration in milliseconds.
3. THE Authorizer SHALL emit a structured JSON log entry for every authorization decision, including the outcome (allow/deny) and the reason for denial when applicable.
4. WHEN a Caller sends a request with an HTTP method not supported by a given endpoint, THE API SHALL return an HTTP 405 status with a descriptive error message.
