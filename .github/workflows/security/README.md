# Shared workflows

A repository for shared action workflows, best practice for new and existing repositories.

Shared workflows:
- Security
    - [Gitleaks](https://github.com/dfds/shared-workflows/tree/master/.github/workflows/security#gitleaks)
    - [TFSec PR Commenter](https://github.com/dfds/shared-workflows/tree/master/.github/workflows/security#tfsec-pr-commenter)
    - [TFSec with upload](https://github.com/dfds/shared-workflows/tree/master/.github/workflows/security#tfsec-with-upload)

## Security

### Gitleaks

Gitleaks is a SAST tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in git repos.

[Marketplace](https://github.com/marketplace/actions/gitleaks).

How to invoke this shared workflow:

```yaml
name: Gitleaks

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/gitleaks.yml@master
```

### TFSec PR Commenter

Add comments to pull requests where tfsec checks have failed.

[Marketplace](https://github.com/marketplace/actions/run-tfsec-pr-commenter).

How to invoke this shared workflow:

```yaml
name: Run tfsec on pull requests

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/tfsec-pr-commenter.yml@master
```

### TFSec with upload

This Github Action will run the tfsec sarif check then add the report to the repo for upload.

[Marketplace](https://github.com/marketplace/actions/run-tfsec-with-sarif-upload).

How to invoke this shared workflow:

```yaml
name: Run tfsec and upload

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/tfsec-upload.yml@master
```
