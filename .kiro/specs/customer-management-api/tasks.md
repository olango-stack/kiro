# Implementation Plan: Customer Management API

## Overview

Incremental implementation of the serverless Customer Management API. Each task builds on the previous, starting with project scaffolding and shared utilities, then the Authorizer Lambda, then the Customer Lambda with all CRUD handlers, and finally wiring everything together with Terraform infrastructure. Tests are co-located with the code they validate.

## Tasks

- [x] 1. Scaffold project structure and shared utilities
  - Create `src/authorizer/`, `src/customers/` directories with `__init__.py` and `requirements.txt` files
  - Create `tests/unit/events/` directory with sample API Gateway proxy event JSON fixtures (one per HTTP method/route)
  - Add copyright header to every source file created in this task
  - _Requirements: 6.1, 6.2_

- [x] 2. Implement shared response and validation helpers in `src/customers/lambda_function.py`
  - [x] 2.1 Implement `build_response(status_code, body)` — returns API Gateway proxy response dict with `Content-Type: application/json`
    - _Requirements: 6.1, 7.1_
  - [x] 2.2 Implement `get_logger()` — returns a `logging.Logger` that emits JSON-structured log lines
    - _Requirements: 7.2_
  - [x] 2.3 Implement `validate_customer_input(body, required_fields)` — checks presence and non-emptiness of required fields, validates `email` format via regex, validates UUID format for `customer_id` path param when supplied
    - _Requirements: 1.2, 3.3, 6.1, 6.3_
  - [x] 2.4 Write unit tests for `build_response`, `get_logger`, and `validate_customer_input` in `tests/unit/test_customers.py`
    - Cover valid inputs, missing fields, malformed email, malformed UUID
    - _Requirements: 1.2, 6.3_

- [x] 3. Implement the Lambda Authorizer (`src/authorizer/lambda_function.py`)
  - [x] 3.1 Implement JWKS fetch with in-memory cache — fetch from `https://cognito-idp.<region>.amazonaws.com/<pool_id>/.well-known/jwks.json` using `python-jose`; cache result in module-level variable
    - _Requirements: 5.5_
  - [x] 3.2 Implement JWT validation — verify signature, `exp`, `iss`, and `aud` claims; raise `Exception("Unauthorized")` for missing/expired token; return `Deny` policy for wrong issuer/audience/signature
    - _Requirements: 5.1, 5.2, 5.3, 5.6_
  - [x] 3.3 Implement `lambda_handler` — extract Bearer token, call JWT validation, build and return IAM policy document (`Allow` or `Deny`) with `principalId` set to the `sub` claim; emit structured JSON log entry for every decision
    - _Requirements: 5.4, 5.5, 7.3_
  - [x] 3.4 Write unit tests for the Authorizer in `tests/unit/test_authorizer.py`
    - Test: valid token → Allow policy with correct `principalId`
    - Test: missing Authorization header → Exception("Unauthorized")
    - Test: expired `exp` claim → Exception("Unauthorized")
    - Test: wrong `iss` → Deny policy
    - Test: wrong `aud` → Deny policy
    - Test: invalid signature → Deny policy
    - Mock `python-jose` JWKS fetch; no live AWS calls
    - _Requirements: 5.1, 5.2, 5.3, 5.6_
  - [x] 3.5 Write property test for Property 10 in `tests/unit/test_properties.py`
    - **Property 10: Missing or expired token returns 401**
    - **Validates: Requirements 5.1, 5.2**
  - [x] 3.6 Write property test for Property 11 in `tests/unit/test_properties.py`
    - **Property 11: Wrong signature, issuer, or audience returns 403**
    - **Validates: Requirements 5.3, 5.6**

- [x] 4. Checkpoint — Ensure all authorizer tests pass
  - Run `pytest tests/unit/test_authorizer.py tests/unit/test_properties.py -v`; ask the user if questions arise.

- [x] 5. Implement Customer Lambda — Create customer (`POST /customers`)
  - [x] 5.1 Implement `create_customer(event, ddb)` — parse and validate body, query `email-index` GSI for uniqueness, call `put_item` with `attribute_not_exists(customer_id)` condition, generate UUID v4 `customer_id` and ISO 8601 timestamps, return 201 with created record
    - _Requirements: 1.1, 1.3, 1.4, 6.1, 6.2_
  - [x] 5.2 Write unit tests for `create_customer` in `tests/unit/test_customers.py`
    - Test: valid payload → 201 with all fields present
    - Test: missing required field → 400
    - Test: duplicate email → 409
    - Test: malformed JSON body → 400
    - Mock boto3 DynamoDB client
    - _Requirements: 1.1, 1.2, 1.3_
  - [x] 5.3 Write property test for Property 1 in `tests/unit/test_properties.py`
    - **Property 1: Customer creation round-trip**
    - **Validates: Requirements 1.1, 2.1, 6.2**
  - [x] 5.4 Write property test for Property 2 in `tests/unit/test_properties.py`
    - **Property 2: Invalid input is rejected with 400**
    - **Validates: Requirements 1.2, 3.3, 6.3**
  - [x] 5.5 Write property test for Property 3 in `tests/unit/test_properties.py`
    - **Property 3: Duplicate email is rejected with 409**
    - **Validates: Requirements 1.3**
  - [x] 5.6 Write property test for Property 4 in `tests/unit/test_properties.py`
    - **Property 4: Customer IDs are unique UUID v4 values**
    - **Validates: Requirements 1.4**

- [x] 6. Implement Customer Lambda — Retrieve customers (`GET /customers` and `GET /customers/{customer_id}`)
  - [x] 6.1 Implement `get_customer(event, ddb)` — extract and validate `customer_id` path param, call `get_item`, return 200 with record or 404 if not found
    - _Requirements: 2.1, 2.2, 2.4_
  - [x] 6.2 Implement `list_customers(event, ddb)` — read optional `limit` (default 20, max 100) and `next_token` (base64-decoded `ExclusiveStartKey`) query params, call `scan` with `Limit`, return 200 with `customers` array and `next_token` (base64-encoded `LastEvaluatedKey` or null)
    - _Requirements: 2.3, 2.4_
  - [x] 6.3 Write unit tests for `get_customer` and `list_customers` in `tests/unit/test_customers.py`
    - Test: valid ID → 200 with correct record
    - Test: non-existent ID → 404
    - Test: list with no records → 200 with empty array
    - Test: list with `next_token` pagination
    - Mock boto3 DynamoDB client
    - _Requirements: 2.1, 2.2, 2.3_
  - [x] 6.4 Write property test for Property 5 in `tests/unit/test_properties.py`
    - **Property 5: Non-existent customer ID returns 404**
    - **Validates: Requirements 2.2, 3.2, 4.2**
  - [x] 6.5 Write property test for Property 6 in `tests/unit/test_properties.py`
    - **Property 6: List endpoint returns all created records**
    - **Validates: Requirements 2.3**
  - [x] 6.6 Write property test for Property 7 in `tests/unit/test_properties.py`
    - **Property 7: All returned records conform to the Customer schema**
    - **Validates: Requirements 2.4, 6.1**

- [x] 7. Implement Customer Lambda — Update customer (`PUT /customers/{customer_id}`)
  - [x] 7.1 Implement `update_customer(event, ddb)` — validate path param and body, check email uniqueness on `email-index` GSI (skip if email unchanged), call `update_item` with `attribute_exists(customer_id)` condition, set `updated_at` to current UTC timestamp, preserve `customer_id` and `created_at`, return 200 with updated record or 404/409 as appropriate
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  - [x] 7.2 Write unit tests for `update_customer` in `tests/unit/test_customers.py`
    - Test: valid update → 200 with updated fields
    - Test: non-existent ID → 404
    - Test: invalid field value → 400
    - Test: duplicate email for different customer → 409
    - Test: `customer_id` and `created_at` unchanged after update
    - Mock boto3 DynamoDB client
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  - [x] 7.3 Write property test for Property 8 in `tests/unit/test_properties.py`
    - **Property 8: Update preserves immutable fields**
    - **Validates: Requirements 3.4**

- [ ] 8. Implement Customer Lambda — Delete customer (`DELETE /customers/{customer_id}`)
  - [ ] 8.1 Implement `delete_customer(event, ddb)` — validate path param, call `delete_item` with `attribute_exists(customer_id)` condition, return 204 with no body or 404 if not found
    - _Requirements: 4.1, 4.2_
  - [ ] 8.2 Write unit tests for `delete_customer` in `tests/unit/test_customers.py`
    - Test: valid existing ID → 204 with no body
    - Test: non-existent ID → 404
    - Mock boto3 DynamoDB client
    - _Requirements: 4.1, 4.2_
  - [ ] 8.3 Write property test for Property 9 in `tests/unit/test_properties.py`
    - **Property 9: Delete then get returns 404**
    - **Validates: Requirements 4.1**

- [ ] 9. Implement Customer Lambda — `lambda_handler` dispatcher and error handling
  - [ ] 9.1 Implement `lambda_handler(event, context)` — route by `httpMethod` + `resource` to the correct handler function using the dispatch table; emit structured JSON log entry per request (method, path, customer_id, status_code, duration_ms); catch all unhandled exceptions and return 500 with generic message (no stack trace)
    - _Requirements: 7.1, 7.2_
  - [ ] 9.2 Implement 405 fallback — return 405 for any method/path combination not in the dispatch table
    - _Requirements: 7.4_
  - [ ] 9.3 Write unit tests for `lambda_handler` dispatch and error handling in `tests/unit/test_customers.py`
    - Test: unhandled exception → 500 without stack trace in body
    - Test: unsupported method → 405
    - Test: log output is valid JSON with required fields
    - _Requirements: 7.1, 7.2, 7.4_
  - [ ] 9.4 Write property test for Property 12 in `tests/unit/test_properties.py`
    - **Property 12: Unhandled exceptions return 500 without stack traces**
    - **Validates: Requirements 7.1**
  - [ ] 9.5 Write property test for Property 13 in `tests/unit/test_properties.py`
    - **Property 13: Every request produces a valid structured log entry**
    - **Validates: Requirements 7.2, 7.3**

- [ ] 10. Checkpoint — Ensure all unit and property tests pass
  - Run `pytest tests/unit/ -v`; ask the user if questions arise.

- [ ] 11. Implement Terraform infrastructure (`infra/`)
  - [ ] 11.1 Write `infra/providers.tf` and `infra/versions.tf` — configure AWS provider pinned to `us-east-1`, declare required Terraform and provider version constraints
    - _Requirements: 5.4, 5.5_
  - [ ] 11.2 Write `infra/variables.tf` — declare variables for environment, Cognito User Pool ID, App Client ID, DynamoDB table name, Lambda source paths, and any other configurable values
    - _Requirements: 5.5, 5.6_
  - [ ] 11.3 Write `infra/main.tf` — define DynamoDB table `customers` (PAY_PER_REQUEST, `customer_id` partition key, `email-index` GSI with `email` partition key, KEYS_ONLY projection); define Cognito User Pool and App Client; define IAM roles and policies for both Lambda functions; define Authorizer Lambda and Customer Lambda (`aws_lambda_function`); define API Gateway REST API with `ANY /{proxy+}`, TOKEN-type Lambda Authorizer, and `AWS_PROXY` integration; configure custom gateway responses for 401 and 403
    - _Requirements: 1.3, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.4_
  - [ ] 11.4 Write `infra/outputs.tf` — output API Gateway invoke URL, Cognito User Pool ID, App Client ID, and DynamoDB table name
    - _Requirements: 5.5_
  - [ ] 11.5 Write `infra/terraform.tfvars` and `infra/envs/dev.tfvars` / `infra/envs/prod.tfvars` — populate default and environment-specific variable values
    - _Requirements: 5.5_

- [ ] 12. Implement integration tests (`tests/integration/test_api.py`)
  - [ ] 12.1 Write integration test setup — read API Gateway invoke URL, Cognito credentials, and DynamoDB table name from environment variables; obtain a valid JWT from Cognito using test user credentials; define helper to make authenticated HTTP requests
    - _Requirements: 5.4_
  - [ ] 12.2 Write integration tests for happy-path CRUD — POST creates record (201), GET by ID returns record (200), GET list returns all records with pagination (200), PUT updates record (200), DELETE removes record (204)
    - _Requirements: 1.1, 2.1, 2.3, 3.1, 4.1_
  - [ ] 12.3 Write integration tests for error cases — 400 on missing field, 409 on duplicate email, 404 on non-existent ID, 401 on missing token, 403 on invalid token
    - _Requirements: 1.2, 1.3, 2.2, 5.1, 5.3_

- [ ] 13. Final checkpoint — Ensure all tests pass
  - Run `pytest tests/unit/ -v`; ask the user if questions arise before proceeding to integration tests.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- All source files must include the copyright header per code standards
- Property tests use `hypothesis` with `@settings(max_examples=100)`; mock all AWS calls with `unittest.mock.patch`
- Integration tests require a deployed dev environment (`terraform apply -var-file=infra/envs/dev.tfvars`) and real AWS credentials
- The `src/customers/` directory is used (not `src/users/`) to match the feature name; update `structure.md` if the canonical path differs
