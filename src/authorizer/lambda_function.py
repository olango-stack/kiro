# Copyright AnyCompany, Inc. or its affiliates. All Rights Reserved.

import os
import json
import logging
import urllib.request
from datetime import datetime

from jose import jwt, jwk, JWTError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

COGNITO_REGION = os.environ.get("COGNITO_REGION", "us-east-1")
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID", "")
COGNITO_APP_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID", "")

JWKS_URL = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com"
    f"/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
)

_JWKS_CACHE = None


def get_jwks():
    """Fetch the Cognito JWKS, returning a cached copy after the first fetch."""
    global _JWKS_CACHE
    if _JWKS_CACHE is not None:
        return _JWKS_CACHE
    with urllib.request.urlopen(JWKS_URL) as response:
        _JWKS_CACHE = json.loads(response.read().decode("utf-8"))
    return _JWKS_CACHE


def validate_token(token):
    """Validate a Cognito JWT.

    Returns the decoded claims dict on success.
    Raises Exception("Unauthorized") for missing, malformed, or expired tokens.
    Returns None for wrong issuer, audience, or signature (caller should Deny).
    """
    if not token:
        raise Exception("Unauthorized")

    expected_issuer = (
        f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    )

    jwks = get_jwks()

    try:
        claims = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=COGNITO_APP_CLIENT_ID,
            issuer=expected_issuer,
        )
        return claims
    except jwt.ExpiredSignatureError:
        raise Exception("Unauthorized")
    except JWTError:
        return None


def _build_policy(principal_id, effect, resource):
    """Return an IAM policy document dict for API Gateway."""
    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource,
                }
            ],
        },
    }


def lambda_handler(event, context):
    """Lambda Authorizer entry point.

    Extracts the Bearer token, validates it, and returns an IAM policy.
    Raises Exception("Unauthorized") for missing/expired tokens (→ 401).
    Returns a Deny policy for wrong issuer/audience/signature (→ 403).
    """
    auth_header = event.get("authorizationToken", "")
    method_arn = event.get("methodArn", "*")

    if not auth_header:
        logger.info(
            json.dumps(
                {
                    "level": "INFO",
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "outcome": "deny",
                    "reason": "missing authorization header",
                }
            )
        )
        raise Exception("Unauthorized")

    # Strip "Bearer " prefix, case-insensitive
    if auth_header.lower().startswith("bearer "):
        token = auth_header[7:]
    else:
        token = auth_header

    if not token:
        logger.info(
            json.dumps(
                {
                    "level": "INFO",
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "outcome": "deny",
                    "reason": "empty token",
                }
            )
        )
        raise Exception("Unauthorized")

    try:
        claims = validate_token(token)
    except Exception:
        # validate_token raises Exception("Unauthorized") for missing/expired tokens
        logger.info(
            json.dumps(
                {
                    "level": "INFO",
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "outcome": "deny",
                    "reason": "unauthorized",
                }
            )
        )
        raise

    if claims is None:
        # Wrong signature, issuer, or audience → Deny (403)
        logger.info(
            json.dumps(
                {
                    "level": "INFO",
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "outcome": "deny",
                    "reason": "invalid token claims",
                }
            )
        )
        return _build_policy("unknown", "Deny", method_arn)

    # Valid token → Allow
    principal_id = claims.get("sub", "unknown")
    logger.info(
        json.dumps(
            {
                "level": "INFO",
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "outcome": "allow",
                "reason": None,
            }
        )
    )
    return _build_policy(principal_id, "Allow", method_arn)
