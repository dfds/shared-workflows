# Shared workflows

A repository for shared action workflows, best practice for new and existing repositories.

Shared workflows:
- Security
    - [Gitleaks](https://github.com/dfds/shared-workflows#gitleaks)
    - [TFSec PR Commenter](https://github.com/dfds/shared-workflows#tfsec-pr-commenter)
- Automation
    - [Auto release](https://github.com/dfds/shared-workflows#auto-release)
    - [Enforce PR labels](https://github.com/dfds/shared-workflows#enforce-pr-labels)
    - [Build Go lambda and upload artifact to S3](https://github.com/dfds/shared-workflows#build-go-lambda-and-upload-artifact-to-s3)

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

Add comments to pull requests where tfsec checks have failed

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

## Automation

### Auto release

Github Action to create a Github Release on pushes to master. Automatically tags the release and create release notes from git log. Change the semantic versioning by applying labels, **release:patch**, **release:minor**, **release:major**.
Works best in conjuction with [Enforce PR labels](https://github.com/dfds/shared-workflows#enforce-pr-labels)

[Marketplace](https://github.com/marketplace/actions/tag-release-on-push-action)

How to invoke this shared workflow:

```yaml
name: Create repository release

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/auto-release.yml@master
```

### Enforce PR labels

Enforce assigning labels before merging PR's. Useful for governing the use of semantic versioning labels for [Auto release](https://github.com/dfds/shared-workflows#auto-release).

[Marketplace](https://github.com/marketplace/actions/enforce-pr-labels)

How to invoke this shared workflow:

```yaml
name: Enforce PR labels

on:
  pull_request:
    types: [labeled, unlabeled, opened, edited, synchronize]
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/enforce-release-labels.yml@master
```

### Build Go lambda and upload artifact to S3

Builds a Go lambda and uploads the zip file to S3 bucket

```yaml
name: Build lambda and upload to S3

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  build-and-upload-to-s3:
    name: build-and-upload-to-s3
    uses: dfds/shared-workflows/.github/workflows/build-and-upload-to-s3.yml@master
    with:
      role-session-name: samplesessionname #Session name
      working-directory: ./working-directory #The working directory that includes the Makefile
      lambda-package-name: lambda-package.zip #The lambda package name 
      s3-location: s3-location #The S3 location to put the artifact
    secrets:
      role-to-assume: ${{ secrets.ROLE_TO_ASSUME }} #Repository secret with the AWS role to be assumed
```

