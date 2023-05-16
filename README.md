# Shared workflows

A repository for shared action workflows, best practice for new and existing repositories.

Shared workflows:
- [Automation](https://github.com/dfds/shared-workflows#automation)
	- [Build lambda and upload to S3](https://github.com/dfds/shared-workflows#build-lambda-and-upload-to-s3)
	- [Auto release](https://github.com/dfds/shared-workflows#auto-release)
	- [Enforce PR labels](https://github.com/dfds/shared-workflows#enforce-pr-labels)
- [Security](https://github.com/dfds/shared-workflows#security)
	- [Run tfsec and upload](https://github.com/dfds/shared-workflows#run-tfsec-and-upload)
	- [Gitleaks 1](https://github.com/dfds/shared-workflows#gitleaks-1)
	- [Run tfsec on pull requests](https://github.com/dfds/shared-workflows#run-tfsec-on-pull-requests)

## Automation

### Build lambda and upload to S3

Builds a Go lambda and uploads the zip file to S3 bucket.

How to invoke this shared workflow:

```yaml
name: Build lambda and upload to S3

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  build-and-upload-to-s3:
    name: build-and-upload-to-s3
    uses: dfds/shared-workflows/.github/workflows/automation-build-and-upload-to-s3.yml@master
    with:
      role-session-name: samplesessionname #Session name
      working-directory: ./working-directory #The working directory that includes the Makefile
      lambda-package-name: lambda-package.zip #The lambda package name 
      s3-location: s3-location #The S3 location to put the artifact
    secrets:
      role-to-assume: ${{ secrets.ROLE_TO_ASSUME }} #Repository secret with the AWS role to be assumed
```

### Auto release

Github Action to create a Github Release on pushes to master. Automatically tags the release and create release notes from git log. Change the semantic versioning by applying labels, **release:patch**, **release:minor**, **release:major**. Works best in conjuction with [Enforce PR labels](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#enforce-pr-labels).

[Marketplace](https://github.com/marketplace/actions/tag-release-on-push-action)

How to invoke this shared workflow:

```yaml
name: Auto release

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/automation-auto-release.yml@master
```

### Enforce PR labels

Enforce assigning labels before merging PR's. Useful for governing the use of semantic versioning labels for [Auto release](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#auto-release).

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
    uses: dfds/shared-workflows/.github/workflows/automation-enforce-release-labels.yml@master
```

## Security

### Run tfsec and upload

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
    uses: dfds/shared-workflows/.github/workflows/security-tfsec-upload.yml@master
```

### Gitleaks 1

Gitleaks is a SAST tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in git repos. You have to add GITLEAKS_LICENSE secret to your repository, it does not work with organization secrets. The license key is stored in 1Password.

[Marketplace](https://github.com/marketplace/actions/gitleaks)

How to invoke this shared workflow:

```yaml
name: Gitleaks 1

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security-gitleaks.yml@master
    secrets: inherit
```

### Run tfsec on pull requests

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
    uses: dfds/shared-workflows/.github/workflows/security-tfsec-pr-commenter.yml@master
```