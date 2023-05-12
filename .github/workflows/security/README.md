# Security

## Run tfsec and upload

This Github Action will run the tfsec sarif check then add the report to the repo for upload.

[Marketplace](https://github.com/marketplace/actions/run-tfsec-with-sarif-upload)

How to invoke this shared workflow:

```yaml
name: Run tfsec and upload

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security/tfsec-upload.yml@master
```

## Run tfsec on pull requests

Add comments to pull requests where tfsec checks have failed.

[Marketplace](https://github.com/marketplace/actions/run-tfsec-pr-commenter)

How to invoke this shared workflow:

```yaml
name: Run tfsec on pull requests

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security/tfsec-pr-commenter.yml@master
```

## Gitleaks

Gitleaks is a SAST tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in git repos.

[Marketplace](https://github.com/marketplace/actions/gitleaks)

How to invoke this shared workflow:

```yaml
name: Gitleaks

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security/gitleaks.yml@master
```