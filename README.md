# Shared workflows and actions

A repository for shared github workflows and actions, best practice for new and existing repositories. We welcome contributions. See [Contributing](docs/CONTRIBUTING.md) to get started.

Shared workflows and actions:
- [Automation](#automation)
	- workflows
		- [Auto release](#auto-release)
		- [Build lambda and upload to S3](#build-lambda-and-upload-to-s3)
		- [Enforce PR labels](#enforce-pr-labels)
		- [Housekeeping](#housekeeping)
		- [Multi architecture docker build](#multi-architecture-docker-build)
- [Compliance](#compliance)
	- actions
		- [Checkov Github Actions Step](#checkov-github-actions-step)
- [Security](#security)
	- workflows
		- [Gitleaks](#gitleaks)
		- [Run tfsec on pull requests](#run-tfsec-on-pull-requests)
		- [Run tfsec and upload](#run-tfsec-and-upload)
		- [Run Trivy IAC with Quality GAte](#run-trivy-iac-with-quality-gate)

## Automation

### Auto release

_This is a workflow_

Creates a Github Release on push to master. Automatically tags the release and create release notes from git log. Change the semantic versioning by applying labels, **release:patch**, **release:minor**, **release:major**. Works best in conjuction with [Enforce PR labels](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#enforce-pr-labels).

[Marketplace](https://github.com/marketplace/actions/tag-release-on-push-action)

How to invoke this workflow:

```yaml
name: Auto release

on:
  push:
    branches: ["master", "main"]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/automation-auto-release.yml@master
    # Note, make sure to use `secrets: inherit` if utilizing the organizational secret `GH_RELEASE`
    # secrets: inherit

    # In order to add prefix to the tag:
    with:
      tag_prefix: "your_prefix"

```

### Build lambda and upload to S3

_This is a workflow_

This workflow builds lambda code and uploads the zip file to S3 bucket. The instructions for building the zip package need to be specified in a Makefile. The workflow works with Go and Python lambdas.

How to invoke this workflow:

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
      role-session-name: upload-crl-importer-lambda #Session name
      working-directory: ./crl-importer-lambda #The working directory that includes the Makefile
      lambda-package-name: crl-importer-lambda.zip #The lambda package name
      s3-location: dfds-ce-shared-artifacts/iam-rolesanywhere-lambdas
      go-version: "1.20" #Should be specified only for Go lambdas
      cache-dependency-path: ./crl-importer-lambda/go.mod/go.sum #Should be specified only for Go lambdas
      arguments: PACKAGE_NAME=${{ matrix.lambda-name }} #The arguments to be passed to make
    secrets:
      role-to-assume: ${{ secrets.ROLE_TO_ASSUME }} #Repository secret with the AWS role to be assumed

```

### Enforce PR labels

_This is a workflow_

Enforce assigning labels before merging PR's. Useful for governing the use of semantic versioning labels for [Auto release](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#auto-release).

[Marketplace](https://github.com/marketplace/actions/enforce-pr-labels)

How to invoke this workflow:

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

### Housekeeping

_This is a workflow_

Sets repository settings to a standard that is used across the organization.

How to invoke this workflow:

```yaml
name: Housekeeping

on:
  schedule:
    - cron: "0 6 * * *"

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/automation-multi-build.yml@master
    secrets: inherit
    with:
      # Optional, Enable delete head branch after merge
      delete_head_branch: true
      # Optional, Enable merging pull requests via squashed commit
      squash_merge: true
      # Optional, Enable branch protection on default branch
      branch_protection: true
```

### Multi architecture docker build

_This is a workflow_

All-in-one package that builds, tests, beautify and publishes a docker image for multiple architectures. This workflow uses the [Auto release](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#auto-release) workflow to create a Github Release on push to master. You have to add DOCKERHUB_USERNAME and DOCKERHUB_TOKEN secrets to your repository to use this workflow. To use the slack integration you will also have to add the SLACK_WEBHOOK secret.

How to invoke this workflow:

```yaml
name: Multi architecture docker build

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/automation-multi-build.yml@master
    secrets: inherit
    with:
      # Required
      image-repo: dfdsdk/repo-name

      # Required, options: linux/amd64,linux/arm64,linux/arm/v7,windows/amd64
      os-archs: "linux/amd64,linux/arm64,linux/arm/v7"

      # Optional, path to the test script to run inside the container
      test-script-path: ./app/test.py
      
      # Optional, the command to run the test script inside the container
      test-script-cmd: "python test.py"
      
      # Optional, the path to the readme file to use for the docker image
      # It is recommended that if you do not have a specific file for the docker image,
      # that you use the same readme as the repository
      docker-readme-path: "./DockerREADME.md"

      # Optional, sends a slack notification to the channel specified in the repository secrets
      slack-notification: true
```

## Compliance

### Checkov Github Actions Step

_This is an action_

A Github Action step that runs Checkov against a Terraform plan file. Policies are defined in dfds/iac-terraform-policies repo.

How to invoke this action:

```yaml
name: Checkov Github Actions Step

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  run_tfplan_and_validate:
    runs-on: ubuntu-latest
    name: A job to call the shared workflow
    steps:
      - uses: actions/checkout@v3
      - name: Terraform Plan and validate
        run: |
          cd terraform
          terraform init
          terraform plan -out tfplan
          terraform show -json tfplan > ../tfplan.json
      - uses: dfds/shared-workflows/.github/actions/compliance-checkov-tfplan@master
        with:
          tf-policy-repo-token: ${{ secrets.GH_REPO_READ_IAC_TERRAFORM_POLICIES }}
```

## Security

### Gitleaks

_This is a workflow_

Gitleaks is a SAST tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in git repos. You have to add GITLEAKS_LICENSE secret to your repository, it does not work with organization secrets. The license key is stored in 1Password.

[Marketplace](https://github.com/marketplace/actions/gitleaks)

How to invoke this workflow:

```yaml
name: Gitleaks

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security-gitleaks.yml@master
    secrets: inherit
```

### Run tfsec on pull requests

_This is a workflow_

Add comments to pull requests where tfsec checks have failed.

[Marketplace](https://github.com/marketplace/actions/run-tfsec-pr-commenter)

How to invoke this workflow:

```yaml
name: Run tfsec on pull requests

on:
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security-tfsec-pr-commenter.yml@master
```

### Run tfsec and upload

_This is a workflow_

This Github Action will run the tfsec sarif check then add the report to the repo for upload.

[Marketplace](https://github.com/marketplace/actions/run-tfsec-with-sarif-upload)

How to invoke this workflow:

```yaml
name: Run tfsec and upload

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security-tfsec-upload.yml@master
```

### Run Trivy IAC with Quality GAte

_This is a workflow_

This Github Action will run the trivy IAC check and block if High or Critical issues are found.

[Marketplace](https://github.com/marketplace/actions/run-trivy-iac-check)

How to invoke this workflow:

```yaml
name: Run Trivy IAC with Quality GAte

on:
  push:
    branches: [ "master", "main" ]
  pull_request:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/security-trivy-iac-check.yaml@master
```