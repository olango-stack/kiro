# Copyright AnyCompany, Inc. or its affiliates. All Rights Reserved.

import base64
import datetime
import json
import logging
import os
import re
import uuid

from botocore.exceptions import ClientError


class _JsonFormatter(logging.Formatter):
    """Formats log records as JSON with level, timestamp, and message fields."""

    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "message": record.getMessage(),
        })


def get_logger():
    """Return a Logger configured to emit JSON-structured log lines at INFO level."""
    logger = logging.getLogger("customers")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(_JsonFormatter())
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_UUID4_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")


def validate_customer_input(body, required_fields):
    """Validate required fields and field formats in the request body.

    Returns (True, None) if valid, or (False, error_message) if invalid.
    """
    for field in required_fields:
        if field not in body or body[field] is None or body[field] == "":
            return False, f"Missing required field: {field}"

    if "email" in body and not _EMAIL_RE.match(str(body["email"])):
        return False, "Invalid email format"

    if "customer_id" in body and not _UUID4_RE.match(str(body["customer_id"])):
        return False, "Invalid customer_id format"

    return True, None


def build_response(status_code, body):
    """Construct an API Gateway proxy response dict with Content-Type: application/json."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body) if body is not None else ""
    }


def create_customer(event, ddb):
    """Handle POST /customers — create a new customer record."""
    # Parse body
    try:
        body = json.loads(event.get("body") or "")
    except json.JSONDecodeError:
        return build_response(400, {"error": "Invalid JSON body"})

    # Validate required fields
    valid, error_msg = validate_customer_input(body, ["first_name", "last_name", "email"])
    if not valid:
        return build_response(400, {"error": error_msg})

    table = os.environ["DYNAMODB_TABLE"]

    # Check email uniqueness via GSI
    response = ddb.query(
        TableName=table,
        IndexName="email-index",
        KeyConditionExpression="email = :email",
        ExpressionAttributeValues={":email": {"S": body["email"]}}
    )
    if response["Count"] > 0:
        return build_response(409, {"error": "Email already exists"})

    # Generate system fields
    customer_id = str(uuid.uuid4())
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build item (plain Python dict for response)
    item = {
        "customer_id": customer_id,
        "first_name": body["first_name"],
        "last_name": body["last_name"],
        "email": body["email"],
        "created_at": now,
        "updated_at": now,
    }
    for optional in ("phone", "company", "notes"):
        if optional in body:
            item[optional] = body[optional]

    # Build DynamoDB item (all values as {"S": ...})
    ddb_item = {k: {"S": v} for k, v in item.items()}

    try:
        ddb.put_item(
            TableName=table,
            Item=ddb_item,
            ConditionExpression="attribute_not_exists(customer_id)",
        )
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "ConditionalCheckFailedException":
            return build_response(409, {"error": "Email already exists"})
        return build_response(500, {"error": "Internal server error"})

    return build_response(201, item)


def _deserialize_item(ddb_item):
    """Convert a DynamoDB item (typed dict) to a plain Python dict (string values)."""
    return {k: v.get("S", v.get("N", str(v))) for k, v in ddb_item.items()}


def get_customer(event, ddb):
    """Handle GET /customers/{customer_id} — retrieve a single customer record."""
    path_params = event.get("pathParameters") or {}
    customer_id = path_params.get("customer_id")

    if not customer_id:
        return build_response(400, {"error": "Missing customer_id"})

    valid, error_msg = validate_customer_input({"customer_id": customer_id}, [])
    if not valid:
        return build_response(400, {"error": error_msg})

    response = ddb.get_item(
        TableName=os.environ["DYNAMODB_TABLE"],
        Key={"customer_id": {"S": customer_id}},
    )

    if "Item" not in response:
        return build_response(404, {"error": "Customer not found"})

    return build_response(200, _deserialize_item(response["Item"]))


def list_customers(event, ddb):
    """Handle GET /customers — list customers with optional pagination."""
    query_params = event.get("queryStringParameters") or {}

    # Parse limit
    try:
        limit = int(query_params.get("limit", 20))
    except (ValueError, TypeError):
        return build_response(400, {"error": "Invalid limit parameter"})

    if limit <= 0 or limit > 100:
        limit = max(1, min(limit, 100))

    # Parse next_token
    exclusive_start_key = None
    raw_token = query_params.get("next_token")
    if raw_token:
        try:
            exclusive_start_key = json.loads(base64.b64decode(raw_token))
        except Exception:
            return build_response(400, {"error": "Invalid next_token"})

    scan_kwargs = {
        "TableName": os.environ["DYNAMODB_TABLE"],
        "Limit": limit,
    }
    if exclusive_start_key:
        scan_kwargs["ExclusiveStartKey"] = exclusive_start_key

    response = ddb.scan(**scan_kwargs)

    items = [_deserialize_item(item) for item in response.get("Items", [])]

    lek = response.get("LastEvaluatedKey")
    next_token_out = base64.b64encode(json.dumps(lek).encode()).decode() if lek else None

    return build_response(200, {"customers": items, "next_token": next_token_out})


def update_customer(event, ddb):
    """Handle PUT /customers/{customer_id} — update an existing customer record."""
    # Extract and validate customer_id path parameter
    path_params = event.get("pathParameters") or {}
    customer_id = path_params.get("customer_id")

    if not customer_id:
        return build_response(400, {"error": "Missing customer_id"})

    if not _UUID4_RE.match(str(customer_id)):
        return build_response(400, {"error": "Invalid customer_id format"})

    # Parse body
    try:
        body = json.loads(event.get("body") or "")
    except json.JSONDecodeError:
        return build_response(400, {"error": "Invalid JSON body"})

    # Validate required fields
    valid, error_msg = validate_customer_input(body, ["first_name", "last_name", "email"])
    if not valid:
        return build_response(400, {"error": error_msg})

    table = os.environ["DYNAMODB_TABLE"]

    # Fetch existing record to get current email
    get_response = ddb.get_item(
        TableName=table,
        Key={"customer_id": {"S": customer_id}},
    )
    if "Item" not in get_response:
        return build_response(404, {"error": "Customer not found"})

    existing_item = get_response["Item"]
    existing_email = existing_item.get("email", {}).get("S", "")

    # Check email uniqueness only if email has changed
    if body["email"] != existing_email:
        email_check = ddb.query(
            TableName=table,
            IndexName="email-index",
            KeyConditionExpression="email = :email",
            ExpressionAttributeValues={":email": {"S": body["email"]}},
        )
        if email_check["Count"] > 0:
            return build_response(409, {"error": "Email already exists"})

    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build UpdateExpression for all updatable fields
    # customer_id and created_at are immutable — never included
    updatable = {
        "first_name": body.get("first_name"),
        "last_name": body.get("last_name"),
        "email": body.get("email"),
        "updated_at": now,
    }
    for optional in ("phone", "company", "notes"):
        if optional in body:
            updatable[optional] = body[optional]

    set_parts = []
    expr_attr_names = {}
    expr_attr_values = {}

    for i, (field, value) in enumerate(updatable.items()):
        name_key = f"#f{i}"
        value_key = f":v{i}"
        set_parts.append(f"{name_key} = {value_key}")
        expr_attr_names[name_key] = field
        expr_attr_values[value_key] = {"S": value}

    update_expression = "SET " + ", ".join(set_parts)

    try:
        update_response = ddb.update_item(
            TableName=table,
            Key={"customer_id": {"S": customer_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ConditionExpression="attribute_exists(customer_id)",
            ReturnValues="ALL_NEW",
        )
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "ConditionalCheckFailedException":
            return build_response(404, {"error": "Customer not found"})
        return build_response(500, {"error": "Internal server error"})

    item = _deserialize_item(update_response["Attributes"])
    return build_response(200, item)
