#!/bin/bash
# Clean AWS credential environment variables before running aws login
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
unset AWS_CREDENTIAL_EXPIRATION
