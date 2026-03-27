# Copyright AnyCompany, Inc. or its affiliates. All Rights Reserved.

import io
import json
import logging
import uuid

import pytest

from src.customers.lambda_function import build_response, get_logger, validate_customer_input


# ---------------------------------------------------------------------------
# build_response
# ---------------------------------------------------------------------------

class TestBuildResponse:
    def test_returns_required_keys(self):
        result = build_response(200, {"key": "value"})
        assert set(result.keys()) == {"statusCode", "headers", "body"}

    def test_content_type_header(self):
        result = build_response(200, {})
        assert result["headers"]["Content-Type"] == "application/json"

    def test_body_is_json_string_for_dict(self):
        payload = {"name": "Alice", "age": 30}
        result = build_response(200, payload)
        assert result["body"] == json.dumps(payload)

    def test_body_is_empty_string_for_none(self):
        result = build_response(204, None)
        assert result["body"] == ""

    def test_status_code_matches_input(self):
        for code in (200, 201, 400, 404, 409, 500):
            assert build_response(code, {})["statusCode"] == code


# ---------------------------------------------------------------------------
# get_logger
# ---------------------------------------------------------------------------

class TestGetLogger:
    def test_returns_logger_instance(self):
        assert isinstance(get_logger(), logging.Logger)

    def test_logger_name_is_customers(self):
        assert get_logger().name == "customers"

    def test_calling_twice_no_duplicate_handlers(self):
        logger1 = get_logger()
        handler_count = len(logger1.handlers)
        logger2 = get_logger()
        assert logger1 is logger2
        assert len(logger2.handlers) == handler_count

    def test_log_output_is_valid_json_with_required_fields(self):
        logger = get_logger()
        # Capture output from the StreamHandler
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        from src.customers.lambda_function import _JsonFormatter
        handler.setFormatter(_JsonFormatter())
        logger.addHandler(handler)
        try:
            logger.info("test message")
            output = stream.getvalue().strip()
            record = json.loads(output)
            assert "level" in record
            assert "timestamp" in record
            assert "message" in record
            assert record["message"] == "test message"
            assert record["level"] == "INFO"
        finally:
            logger.removeHandler(handler)


# ---------------------------------------------------------------------------
# validate_customer_input
# ---------------------------------------------------------------------------

VALID_BODY = {
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice@example.com",
}

REQUIRED = ["first_name", "last_name", "email"]


class TestValidateCustomerInput:
    def test_valid_body_returns_true_none(self):
        ok, err = validate_customer_input(VALID_BODY, REQUIRED)
        assert ok is True
        assert err is None

    def test_missing_required_field_returns_false_with_field_name(self):
        body = {k: v for k, v in VALID_BODY.items() if k != "email"}
        ok, err = validate_customer_input(body, REQUIRED)
        assert ok is False
        assert "email" in err

    def test_empty_string_required_field_returns_false(self):
        body = {**VALID_BODY, "first_name": ""}
        ok, err = validate_customer_input(body, REQUIRED)
        assert ok is False
        assert err is not None

    def test_valid_email_passes(self):
        body = {**VALID_BODY, "email": "user.name+tag@sub.domain.org"}
        ok, err = validate_customer_input(body, REQUIRED)
        assert ok is True
        assert err is None

    @pytest.mark.parametrize("bad_email", ["notanemail", "user@", "@domain.com", "a@b"])
    def test_malformed_email_returns_false(self, bad_email):
        body = {**VALID_BODY, "email": bad_email}
        ok, err = validate_customer_input(body, REQUIRED)
        assert ok is False
        assert err == "Invalid email format"

    def test_valid_uuid4_passes(self):
        body = {**VALID_BODY, "customer_id": str(uuid.uuid4())}
        ok, err = validate_customer_input(body, REQUIRED)
        assert ok is True
        assert err is None

    @pytest.mark.parametrize("bad_uuid", ["not-a-uuid", "12345", ""])
    def test_malformed_uuid_returns_false(self, bad_uuid):
        body = {**VALID_BODY, "customer_id": bad_uuid}
        ok, err = validate_customer_input(body, REQUIRED)
        assert ok is False
        assert err == "Invalid customer_id format"

    def test_uuid_version1_returns_false(self):
        v1 = str(uuid.uuid1())
        body = {**VALID_BODY, "customer_id": v1}
        ok, err = validate_customer_input(body, REQUIRED)
        assert ok is False
        assert err == "Invalid customer_id format"


# ---------------------------------------------------------------------------
# create_customer
# ---------------------------------------------------------------------------

import os
from unittest.mock import MagicMock

from src.customers.lambda_function import create_customer


def make_post_event(body_dict):
    return {"body": json.dumps(body_dict)}


class TestCreateCustomer:
    def setup_method(self):
        os.environ["DYNAMODB_TABLE"] = "test-table"

    def _make_ddb(self, email_count=0):
        ddb = MagicMock()
        ddb.query.return_value = {"Count": email_count}
        ddb.put_item.return_value = {}
        return ddb

    def test_valid_payload_returns_201_with_all_fields(self):
        ddb = self._make_ddb(email_count=0)
        event = make_post_event({
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
        })
        result = create_customer(event, ddb)
        assert result["statusCode"] == 201
        body = json.loads(result["body"])
        for field in ("customer_id", "first_name", "last_name", "email", "created_at", "updated_at"):
            assert field in body, f"Missing field: {field}"

    def test_missing_required_field_returns_400(self):
        ddb = self._make_ddb()
        event = make_post_event({"first_name": "Alice", "last_name": "Smith"})  # no email
        result = create_customer(event, ddb)
        assert result["statusCode"] == 400

    def test_duplicate_email_returns_409(self):
        ddb = self._make_ddb(email_count=1)
        event = make_post_event({
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob@example.com",
        })
        result = create_customer(event, ddb)
        assert result["statusCode"] == 409

    def test_malformed_json_body_returns_400(self):
        ddb = self._make_ddb()
        event = {"body": "not valid json {{{"}
        result = create_customer(event, ddb)
        assert result["statusCode"] == 400


# ---------------------------------------------------------------------------
# get_customer
# ---------------------------------------------------------------------------

import base64

from src.customers.lambda_function import get_customer, list_customers

SAMPLE_DDB_ITEM = {
    "customer_id": {"S": "550e8400-e29b-41d4-a716-446655440000"},
    "first_name": {"S": "Jane"},
    "last_name": {"S": "Doe"},
    "email": {"S": "jane@example.com"},
    "created_at": {"S": "2024-01-15T10:30:00Z"},
    "updated_at": {"S": "2024-01-15T10:30:00Z"},
}

SAMPLE_CUSTOMER_ID = "550e8400-e29b-41d4-a716-446655440000"


class TestGetCustomer:
    def setup_method(self):
        os.environ["DYNAMODB_TABLE"] = "test-table"

    def _make_event(self, customer_id=None):
        params = {"customer_id": customer_id} if customer_id is not None else {}
        return {"pathParameters": params}

    def test_valid_id_item_found_returns_200_with_record(self):
        ddb = MagicMock()
        ddb.get_item.return_value = {"Item": SAMPLE_DDB_ITEM}
        result = get_customer(self._make_event(SAMPLE_CUSTOMER_ID), ddb)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["customer_id"] == SAMPLE_CUSTOMER_ID
        assert body["first_name"] == "Jane"
        assert body["last_name"] == "Doe"
        assert body["email"] == "jane@example.com"
        assert body["created_at"] == "2024-01-15T10:30:00Z"
        assert body["updated_at"] == "2024-01-15T10:30:00Z"

    def test_valid_id_item_not_found_returns_404(self):
        ddb = MagicMock()
        ddb.get_item.return_value = {}
        result = get_customer(self._make_event(SAMPLE_CUSTOMER_ID), ddb)
        assert result["statusCode"] == 404

    def test_missing_customer_id_returns_400(self):
        ddb = MagicMock()
        result = get_customer({"pathParameters": {}}, ddb)
        assert result["statusCode"] == 400

    def test_invalid_customer_id_format_returns_400(self):
        ddb = MagicMock()
        result = get_customer(self._make_event("not-a-valid-uuid"), ddb)
        assert result["statusCode"] == 400


# ---------------------------------------------------------------------------
# list_customers
# ---------------------------------------------------------------------------

class TestListCustomers:
    def setup_method(self):
        os.environ["DYNAMODB_TABLE"] = "test-table"

    def _make_event(self, query_params=None):
        return {"queryStringParameters": query_params or {}}

    def test_no_records_returns_200_with_empty_array_and_null_next_token(self):
        ddb = MagicMock()
        ddb.scan.return_value = {"Items": []}
        result = list_customers(self._make_event(), ddb)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["customers"] == []
        assert body["next_token"] is None

    def test_records_present_returns_200_with_deserialized_items(self):
        ddb = MagicMock()
        ddb.scan.return_value = {"Items": [SAMPLE_DDB_ITEM]}
        result = list_customers(self._make_event(), ddb)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert len(body["customers"]) == 1
        customer = body["customers"][0]
        assert customer["customer_id"] == SAMPLE_CUSTOMER_ID
        assert customer["email"] == "jane@example.com"

    def test_last_evaluated_key_produces_next_token(self):
        ddb = MagicMock()
        lek = {"customer_id": {"S": "some-id"}}
        ddb.scan.return_value = {"Items": [SAMPLE_DDB_ITEM], "LastEvaluatedKey": lek}
        result = list_customers(self._make_event(), ddb)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["next_token"] is not None
        # Verify it decodes back to the LastEvaluatedKey
        decoded = json.loads(base64.b64decode(body["next_token"]))
        assert decoded == lek

    def test_next_token_query_param_forwarded_as_exclusive_start_key(self):
        ddb = MagicMock()
        ddb.scan.return_value = {"Items": []}
        lek = {"customer_id": {"S": "some-id"}}
        token = base64.b64encode(json.dumps(lek).encode()).decode()
        result = list_customers(self._make_event({"next_token": token}), ddb)
        assert result["statusCode"] == 200
        call_kwargs = ddb.scan.call_args[1]
        assert call_kwargs.get("ExclusiveStartKey") == lek


# ---------------------------------------------------------------------------
# update_customer
# ---------------------------------------------------------------------------

from src.customers.lambda_function import update_customer

SAMPLE_UPDATE_RESPONSE = {
    "Attributes": {
        "customer_id": {"S": "550e8400-e29b-41d4-a716-446655440000"},
        "first_name": {"S": "Jane"},
        "last_name": {"S": "Updated"},
        "email": {"S": "jane@example.com"},
        "created_at": {"S": "2024-01-15T10:30:00Z"},
        "updated_at": {"S": "2024-01-15T12:00:00Z"},
    }
}


def make_put_event(customer_id, body_dict):
    return {
        "pathParameters": {"customer_id": customer_id},
        "body": json.dumps(body_dict),
    }


class TestUpdateCustomer:
    def setup_method(self):
        os.environ["DYNAMODB_TABLE"] = "test-table"

    def _make_ddb(self, existing_item=None, email_count=0):
        ddb = MagicMock()
        if existing_item is not None:
            ddb.get_item.return_value = {"Item": existing_item}
        else:
            ddb.get_item.return_value = {}
        ddb.query.return_value = {"Count": email_count}
        ddb.update_item.return_value = SAMPLE_UPDATE_RESPONSE
        return ddb

    def test_valid_update_returns_200_with_updated_fields(self):
        existing = {
            "customer_id": {"S": SAMPLE_CUSTOMER_ID},
            "first_name": {"S": "Jane"},
            "last_name": {"S": "Doe"},
            "email": {"S": "jane@example.com"},
            "created_at": {"S": "2024-01-15T10:30:00Z"},
            "updated_at": {"S": "2024-01-15T10:30:00Z"},
        }
        ddb = self._make_ddb(existing_item=existing)
        event = make_put_event(SAMPLE_CUSTOMER_ID, {
            "first_name": "Jane",
            "last_name": "Updated",
            "email": "jane@example.com",
        })
        result = update_customer(event, ddb)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["last_name"] == "Updated"
        assert body["customer_id"] == SAMPLE_CUSTOMER_ID

    def test_nonexistent_id_get_item_no_item_returns_404(self):
        ddb = self._make_ddb(existing_item=None)  # get_item returns no Item
        event = make_put_event(SAMPLE_CUSTOMER_ID, {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
        })
        result = update_customer(event, ddb)
        assert result["statusCode"] == 404

    def test_invalid_field_value_bad_email_returns_400(self):
        ddb = self._make_ddb()
        event = make_put_event(SAMPLE_CUSTOMER_ID, {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "not-an-email",
        })
        result = update_customer(event, ddb)
        assert result["statusCode"] == 400

    def test_duplicate_email_different_customer_returns_409(self):
        existing = {
            "customer_id": {"S": SAMPLE_CUSTOMER_ID},
            "first_name": {"S": "Jane"},
            "last_name": {"S": "Doe"},
            "email": {"S": "jane@example.com"},
            "created_at": {"S": "2024-01-15T10:30:00Z"},
            "updated_at": {"S": "2024-01-15T10:30:00Z"},
        }
        # email_count=1 means the new email is already taken by another customer
        ddb = self._make_ddb(existing_item=existing, email_count=1)
        event = make_put_event(SAMPLE_CUSTOMER_ID, {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "taken@example.com",  # different from existing email
        })
        result = update_customer(event, ddb)
        assert result["statusCode"] == 409

    def test_customer_id_and_created_at_unchanged_after_update(self):
        original_customer_id = SAMPLE_CUSTOMER_ID
        original_created_at = "2024-01-15T10:30:00Z"
        existing = {
            "customer_id": {"S": original_customer_id},
            "first_name": {"S": "Jane"},
            "last_name": {"S": "Doe"},
            "email": {"S": "jane@example.com"},
            "created_at": {"S": original_created_at},
            "updated_at": {"S": "2024-01-15T10:30:00Z"},
        }
        ddb = self._make_ddb(existing_item=existing)
        event = make_put_event(original_customer_id, {
            "first_name": "Jane",
            "last_name": "Updated",
            "email": "jane@example.com",
        })
        result = update_customer(event, ddb)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        # customer_id and created_at must match original values
        assert body["customer_id"] == original_customer_id
        assert body["created_at"] == original_created_at
        # Verify update_item was NOT called with customer_id or created_at in UpdateExpression
        call_kwargs = ddb.update_item.call_args[1]
        update_expr = call_kwargs["UpdateExpression"]
        attr_names = call_kwargs["ExpressionAttributeNames"]
        updated_fields = set(attr_names.values())
        assert "customer_id" not in updated_fields, "customer_id must not be in UpdateExpression"
        assert "created_at" not in updated_fields, "created_at must not be in UpdateExpression"
