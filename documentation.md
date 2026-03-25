# Mock API Provider - Developer Changelog

## UPDATE - V2 Schema Rollout (CRITICAL)

**Date:** March 2026
**Affected Endpoints:** `/v1/get-user`

**Notice of Breaking Change:**
To better align with our new multi-tenant architecture, we have deprecated the `user_id` parameter in our JSON payloads.

**Action Required:**
All API requests must now use `account_id` instead of `user_id` when fetching user profiles. Any requests continuing to use `user_id` will be rejected with a 400 Bad Request error.
