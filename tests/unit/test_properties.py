# Copyright AnyCompany, Inc. or its affiliates. All Rights Reserved.

import pytest
from unittest.mock import patch
from hypothesis import given, settings
from hypothesis import strategies as st
from jose import jwt

from src.authorizer.lambda_function import lambda_handler


FAKE_JWKS = {"keys": [{"kty": "RSA", "kid": "test-key"}]}

# Strategy for generating realistic-looking method ARNs
method_arn_st = st.builds(
    "arn:aws:execute-api:us-east-1:{}:{}/{}/{}/{}".format,
    st.from_regex(r"[0-9]{12}", fullmatch=True),
    st.from_regex(r"[a-z0-9]{6,10}", fullmatch=True),
    st.sampled_from(["dev", "prod", "staging"]),
    st.sampled_from(["GET", "POST", "PUT", "DELETE"]),
    st.sampled_from(["customers", "customers/some-id"]),
)

# Strategy for generating random token strings (not valid JWTs)
token_string_st = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters="._-"),
    min_size=1,
    max_size=200,
).filter(lambda s: s.strip() != "")


# Feature: customer-management-api, Property 10: Missing or expired token returns 401
@given(method_arn=method_arn_st)
@settings(max_examples=100)
def test_property_10_missing_token_raises_unauthorized(method_arn):
    """Validates: Requirements 5.1, 5.2

    For any API endpoint, a request with no Authorization header should raise
    Exception("Unauthorized"), which API Gateway translates to HTTP 401.
    """
    event = {"methodArn": method_arn}  # no authorizationToken key

    with pytest.raises(Exception, match="Unauthorized"):
        lambda_handler(event, None)


# Feature: customer-management-api, Property 10: Missing or expired token returns 401
@given(
    method_arn=method_arn_st,
    token=token_string_st,
)
@settings(max_examples=100)
def test_property_10_expired_token_raises_unauthorized(method_arn, token):
    """Validates: Requirements 5.1, 5.2

    For any API endpoint, a request with a token whose exp claim is in the past
    should raise Exception("Unauthorized"), which API Gateway translates to HTTP 401.
    """
    event = {"methodArn": method_arn, "authorizationToken": f"Bearer {token}"}

    with patch("src.authorizer.lambda_function.get_jwks", return_value=FAKE_JWKS), \
         patch(
             "src.authorizer.lambda_function.jwt.decode",
             side_effect=jwt.ExpiredSignatureError("Token is expired"),
         ):
        with pytest.raises(Exception, match="Unauthorized"):
            lambda_handler(event, None)

# Feature: customer-management-api, Property 11: Wrong signature, issuer, or audience returns 403
@given(
    method_arn=method_arn_st,
    token=token_string_st,
    error_msg=st.sampled_from([
        "Signature verification failed",
        "Invalid issuer",
        "Invalid audience",
        "Invalid claims",
    ]),
)
@settings(max_examples=100)
def test_property_11_invalid_jwt_claims_returns_deny_policy(method_arn, token, error_msg):
    """Validates: Requirements 5.3, 5.6

    For any API endpoint, a request bearing a JWT with wrong signature, issuer,
    or audience should return a Deny IAM policy, which API Gateway translates to HTTP 403.
    """
    from jose import JWTError

    event = {"methodArn": method_arn, "authorizationToken": f"Bearer {token}"}

    with patch("src.authorizer.lambda_function.get_jwks", return_value=FAKE_JWKS), \
         patch(
             "src.authorizer.lambda_function.jwt.decode",
             side_effect=JWTError(error_msg),
         ):
        result = lambda_handler(event, None)

    assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"


# ---------------------------------------------------------------------------
# Customer Lambda property tests (Tasks 5.3 – 5.6)
# ---------------------------------------------------------------------------

import json
import os
import re
import uuid as _uuid_mod
from unittest.mock import MagicMock

from src.customers.lambda_function import create_customer

_UUID4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)

# Helpers
def _make_ddb(email_count=0):
    ddb = MagicMock()
    ddb.query.return_value = {"Count": email_count}
    ddb.put_item.return_value = {}
    return ddb

def _post_event(body_dict):
    return {"body": json.dumps(body_dict)}


# Feature: customer-management-api, Property 1: Customer creation round-trip
@given(
    first_name=st.text(min_size=1, max_size=50).filter(str.strip),
    last_name=st.text(min_size=1, max_size=50).filter(str.strip),
    email=st.emails(),
)
@settings(max_examples=100)
def test_property_1_customer_creation_round_trip(first_name, last_name, email):
    """Validates: Requirements 1.1, 2.1, 6.2

    For any valid customer payload, POSTing to create_customer should return 201
    and a body containing all submitted fields plus customer_id, created_at, updated_at.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    ddb = _make_ddb(email_count=0)
    event = _post_event({"first_name": first_name, "last_name": last_name, "email": email})

    result = create_customer(event, ddb)

    assert result["statusCode"] == 201
    body = json.loads(result["body"])
    for field in ("customer_id", "first_name", "last_name", "email", "created_at", "updated_at"):
        assert field in body, f"Missing field: {field}"
    assert body["first_name"] == first_name
    assert body["last_name"] == last_name
    assert body["email"] == email
    assert _UUID4_PATTERN.match(body["customer_id"]), "customer_id is not a valid UUID v4"


# Feature: customer-management-api, Property 2: Invalid input is rejected with 400
@given(
    last_name=st.text(min_size=1, max_size=50),
    email=st.text(min_size=1, max_size=100),
)
@settings(max_examples=100)
def test_property_2_empty_first_name_returns_400(last_name, email):
    """Validates: Requirements 1.2, 3.3, 6.3

    A body with an empty first_name (required field missing/empty) should return 400
    without exposing stack traces.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    ddb = _make_ddb(email_count=0)
    event = _post_event({"first_name": "", "last_name": last_name, "email": email})

    result = create_customer(event, ddb)

    assert result["statusCode"] == 400
    assert "traceback" not in result["body"].lower()
    body = json.loads(result["body"])
    assert "error" in body


@given(
    first_name=st.text(min_size=1, max_size=50).filter(str.strip),
    last_name=st.text(min_size=1, max_size=50).filter(str.strip),
    bad_email=st.text(min_size=1, max_size=100).filter(lambda s: "@" not in s),
)
@settings(max_examples=100)
def test_property_2_malformed_email_returns_400(first_name, last_name, bad_email):
    """Validates: Requirements 1.2, 3.3, 6.3

    A body with a malformed email (no '@') should return 400 without exposing stack traces.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    ddb = _make_ddb(email_count=0)
    event = _post_event({"first_name": first_name, "last_name": last_name, "email": bad_email})

    result = create_customer(event, ddb)

    assert result["statusCode"] == 400
    assert "traceback" not in result["body"].lower()
    body = json.loads(result["body"])
    assert "error" in body


# Feature: customer-management-api, Property 3: Duplicate email is rejected with 409
@given(email=st.emails())
@settings(max_examples=100)
def test_property_3_duplicate_email_returns_409(email):
    """Validates: Requirements 1.3

    When ddb.query returns Count=1 (email already exists), create_customer should return 409.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    ddb = _make_ddb(email_count=1)
    event = _post_event({"first_name": "Jane", "last_name": "Doe", "email": email})

    result = create_customer(event, ddb)

    assert result["statusCode"] == 409


# Feature: customer-management-api, Property 4: Customer IDs are unique UUID v4 values
@given(
    payloads=st.lists(
        st.fixed_dictionaries({
            "first_name": st.text(min_size=1, max_size=30).filter(str.strip),
            "last_name": st.text(min_size=1, max_size=30).filter(str.strip),
            "email": st.emails(),
        }),
        min_size=5,
        max_size=5,
    )
)
@settings(max_examples=50)
def test_property_4_customer_ids_are_unique_uuid4(payloads):
    """Validates: Requirements 1.4

    For any N successful create_customer calls, all returned customer_id values
    are distinct and conform to UUID v4 format.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    customer_ids = []
    for payload in payloads:
        ddb = _make_ddb(email_count=0)
        result = create_customer(_post_event(payload), ddb)
        assert result["statusCode"] == 201
        body = json.loads(result["body"])
        customer_ids.append(body["customer_id"])

    # All IDs must be valid UUID v4
    for cid in customer_ids:
        assert _UUID4_PATTERN.match(cid), f"{cid!r} is not a valid UUID v4"

    # All IDs must be unique
    assert len(customer_ids) == len(set(customer_ids)), "Duplicate customer_id values found"


# ---------------------------------------------------------------------------
# Tasks 6.4 – 6.6: get_customer / list_customers property tests
# ---------------------------------------------------------------------------

from src.customers.lambda_function import get_customer, list_customers


def _make_ddb_item(first_name, last_name, email, customer_id):
    return {
        "customer_id": {"S": customer_id},
        "first_name": {"S": first_name},
        "last_name": {"S": last_name},
        "email": {"S": email},
        "created_at": {"S": "2024-01-15T10:30:00Z"},
        "updated_at": {"S": "2024-01-15T10:30:00Z"},
    }


def _get_event(customer_id):
    return {"pathParameters": {"customer_id": customer_id}}


def _list_event():
    return {}


# Feature: customer-management-api, Property 5: Non-existent customer ID returns 404
@given(customer_id=st.uuids(version=4).map(str))
@settings(max_examples=100)
def test_property_5_nonexistent_customer_returns_404(customer_id):
    """Validates: Requirements 2.2, 3.2, 4.2

    For any GET request targeting a customer_id that was never created,
    get_customer should return HTTP 404.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    ddb = MagicMock()
    ddb.get_item.return_value = {}  # no "Item" key — simulates not found

    result = get_customer(_get_event(customer_id), ddb)

    assert result["statusCode"] == 404


# Feature: customer-management-api, Property 6: List endpoint returns all created records
@given(
    items=st.lists(
        st.builds(
            _make_ddb_item,
            first_name=st.text(min_size=1, max_size=30).filter(str.strip),
            last_name=st.text(min_size=1, max_size=30).filter(str.strip),
            email=st.emails(),
            customer_id=st.uuids(version=4).map(str),
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=50)
def test_property_6_list_returns_all_records(items):
    """Validates: Requirements 2.3

    For any set of N customers, list_customers should return all N records
    when ddb.scan returns them in one page (no LastEvaluatedKey).
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    ddb = MagicMock()
    ddb.scan.return_value = {"Items": items}  # no LastEvaluatedKey — single page

    result = list_customers(_list_event(), ddb)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    customers = body["customers"]
    assert len(customers) == len(items)


# Feature: customer-management-api, Property 7: All returned records conform to the Customer schema
_REQUIRED_FIELDS = {"customer_id", "first_name", "last_name", "email", "created_at", "updated_at"}
_ALLOWED_FIELDS = _REQUIRED_FIELDS | {"phone", "company", "notes"}


@given(
    items=st.lists(
        st.builds(
            _make_ddb_item,
            first_name=st.text(min_size=1, max_size=30).filter(str.strip),
            last_name=st.text(min_size=1, max_size=30).filter(str.strip),
            email=st.emails(),
            customer_id=st.uuids(version=4).map(str),
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=50)
def test_property_7_returned_records_conform_to_schema(items):
    """Validates: Requirements 2.4, 6.1

    For any customer record returned by list_customers, the record must contain
    all required fields with string values and no undeclared extra fields.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"
    ddb = MagicMock()
    ddb.scan.return_value = {"Items": items}

    result = list_customers(_list_event(), ddb)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    for customer in body["customers"]:
        # All required fields must be present
        for field in _REQUIRED_FIELDS:
            assert field in customer, f"Missing required field: {field}"
        # All field values must be strings
        for field, value in customer.items():
            assert isinstance(value, str), f"Field {field!r} is not a string: {value!r}"
        # No undeclared fields
        extra = set(customer.keys()) - _ALLOWED_FIELDS
        assert not extra, f"Undeclared fields found: {extra}"


# ---------------------------------------------------------------------------
# Task 7.3: Property 8 — Update preserves immutable fields
# ---------------------------------------------------------------------------

from src.customers.lambda_function import update_customer


# Feature: customer-management-api, Property 8: Update preserves immutable fields
@given(
    customer_id=st.uuids(version=4).map(str),
    first_name=st.text(min_size=1, max_size=50).filter(str.strip),
    last_name=st.text(min_size=1, max_size=50).filter(str.strip),
    email=st.emails(),
)
@settings(max_examples=100)
def test_property_8_update_preserves_immutable_fields(customer_id, first_name, last_name, email):
    """Validates: Requirements 3.4

    For any customer record, after any PUT with a valid payload, customer_id and
    created_at should remain identical to their values at creation time.
    updated_at should be >= created_at.
    """
    os.environ["DYNAMODB_TABLE"] = "test-table"

    original_created_at = "2024-01-15T10:30:00Z"
    new_updated_at = "2024-01-15T12:00:00Z"

    existing_item = {
        "customer_id": {"S": customer_id},
        "first_name": {"S": first_name},
        "last_name": {"S": last_name},
        "email": {"S": email},
        "created_at": {"S": original_created_at},
        "updated_at": {"S": original_created_at},
    }

    ddb = MagicMock()
    ddb.get_item.return_value = {"Item": existing_item}
    ddb.query.return_value = {"Count": 0}
    ddb.update_item.return_value = {
        "Attributes": {
            "customer_id": {"S": customer_id},
            "first_name": {"S": first_name},
            "last_name": {"S": last_name},
            "email": {"S": email},
            "created_at": {"S": original_created_at},
            "updated_at": {"S": new_updated_at},
        }
    }

    event = {
        "pathParameters": {"customer_id": customer_id},
        "body": json.dumps({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }),
    }

    result = update_customer(event, ddb)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])

    # customer_id and created_at must be unchanged
    assert body["customer_id"] == customer_id
    assert body["created_at"] == original_created_at

    # updated_at must be >= created_at
    assert body["updated_at"] >= body["created_at"]

    # Verify customer_id and created_at are NOT in the UpdateExpression
    call_kwargs = ddb.update_item.call_args[1]
    updated_fields = set(call_kwargs["ExpressionAttributeNames"].values())
    assert "customer_id" not in updated_fields
    assert "created_at" not in updated_fields
