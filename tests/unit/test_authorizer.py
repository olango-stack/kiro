# Copyright AnyCompany, Inc. or its affiliates. All Rights Reserved.

import pytest
from unittest.mock import patch
from jose import jwt, JWTError

from src.authorizer.lambda_function import lambda_handler


FAKE_JWKS = {"keys": [{"kty": "RSA", "kid": "test-key"}]}
FAKE_CLAIMS = {"sub": "user-123", "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_test", "aud": "test-client"}
FAKE_METHOD_ARN = "arn:aws:execute-api:us-east-1:123456789012:abc123/dev/GET/customers"


def make_event(token=None, method_arn=FAKE_METHOD_ARN):
    event = {"methodArn": method_arn}
    if token is not None:
        event["authorizationToken"] = token
    return event


class TestLambdaHandlerAllowPolicy:
    def test_valid_token_returns_allow_policy_with_correct_principal(self):
        """Valid token → Allow policy with principalId set to sub claim."""
        with patch("src.authorizer.lambda_function.get_jwks", return_value=FAKE_JWKS), \
             patch("src.authorizer.lambda_function.jwt.decode", return_value=FAKE_CLAIMS):
            result = lambda_handler(make_event("Bearer valid.token.here"), None)

        assert result["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert result["principalId"] == "user-123"
        assert result["policyDocument"]["Statement"][0]["Resource"] == FAKE_METHOD_ARN


class TestLambdaHandlerUnauthorized:
    def test_missing_authorization_token_raises_unauthorized(self):
        """Missing authorizationToken → raises Exception('Unauthorized')."""
        with pytest.raises(Exception, match="Unauthorized"):
            lambda_handler(make_event(), None)

    def test_empty_authorization_token_raises_unauthorized(self):
        """Empty authorizationToken → raises Exception('Unauthorized')."""
        with pytest.raises(Exception, match="Unauthorized"):
            lambda_handler(make_event(""), None)

    def test_expired_token_raises_unauthorized(self):
        """Expired token (ExpiredSignatureError) → raises Exception('Unauthorized')."""
        with patch("src.authorizer.lambda_function.get_jwks", return_value=FAKE_JWKS), \
             patch("src.authorizer.lambda_function.jwt.decode", side_effect=jwt.ExpiredSignatureError("expired")):
            with pytest.raises(Exception, match="Unauthorized"):
                lambda_handler(make_event("Bearer expired.token.here"), None)


class TestLambdaHandlerDenyPolicy:
    def test_wrong_issuer_returns_deny_policy(self):
        """Wrong iss (JWTError) → Deny policy."""
        with patch("src.authorizer.lambda_function.get_jwks", return_value=FAKE_JWKS), \
             patch("src.authorizer.lambda_function.jwt.decode", side_effect=JWTError("wrong issuer")):
            result = lambda_handler(make_event("Bearer wrong.iss.token"), None)

        assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_wrong_audience_returns_deny_policy(self):
        """Wrong aud (JWTError) → Deny policy."""
        with patch("src.authorizer.lambda_function.get_jwks", return_value=FAKE_JWKS), \
             patch("src.authorizer.lambda_function.jwt.decode", side_effect=JWTError("wrong audience")):
            result = lambda_handler(make_event("Bearer wrong.aud.token"), None)

        assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_invalid_signature_returns_deny_policy(self):
        """Invalid signature (JWTError) → Deny policy."""
        with patch("src.authorizer.lambda_function.get_jwks", return_value=FAKE_JWKS), \
             patch("src.authorizer.lambda_function.jwt.decode", side_effect=JWTError("invalid signature")):
            result = lambda_handler(make_event("Bearer bad.sig.token"), None)

        assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"
