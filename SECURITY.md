# Security policy

## Reporting a vulnerability

Report security issues in this pack privately to **security@openclips.ai**. Include the affected skill or file, a description, and steps to reproduce where possible. Please do not open a public issue for security reports.

We aim to acknowledge reports within a few business days and ask for a reasonable disclosure window before details are published.

## What these skills can and cannot do

- They call the OpenClips MCP server with the permissions of the signed-in user, and nothing else. They contain no scripts and require no local binaries.
- Every credit-spending action pauses for the user's explicit approval, after showing the cost where the server can quote one and saying so where it cannot.
- Sign-in is OAuth in the browser. No skill in this pack asks for, stores or transmits a token.

## Supported versions

The latest release is supported. Security fixes are applied to that line; older tags are not maintained.
