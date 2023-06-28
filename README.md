# Shared workflows

A repository for shared action workflows, best practice for new and existing repositories. We welcome contributions. See [Contributing](docs/CONTRIBUTING.md) to get started.

Shared workflows:
- [Security](https://github.com/dfds/shared-workflows#security)
	- [Run tfsec on pull requests](https://github.com/dfds/shared-workflows#run-tfsec-on-pull-requests)
	- [Run tfsec and upload](https://github.com/dfds/shared-workflows#run-tfsec-and-upload)
	- [Gitleaks](https://github.com/dfds/shared-workflows#gitleaks)
	- [Run Trivy IAC with Quality GAte](https://github.com/dfds/shared-workflows#run-trivy-iac-with-quality-gate)
- [Automation](https://github.com/dfds/shared-workflows#automation)
	- [Build lambda and upload to S3](https://github.com/dfds/shared-workflows#build-lambda-and-upload-to-s3)
	- [Multi architecture docker build](https://github.com/dfds/shared-workflows#multi-architecture-docker-build)
	- [Enforce PR labels](https://github.com/dfds/shared-workflows#enforce-pr-labels)
	- [Auto release](https://github.com/dfds/shared-workflows#auto-release)

## Security

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

### Gitleaks

Gitleaks is a SAST tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in git repos. You have to add GITLEAKS_LICENSE secret to your repository, it does not work with organization secrets. The license key is stored in 1Password.

[Marketplace](https://github.com/marketplace/actions/gitleaks)

How to invoke this shared workflow:

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

### Run Trivy IAC with Quality GAte

This Github Action will run the trivy IAC check and block if High or Critical issues are found.

[Marketplace](https://github.com/marketplace/actions/run-trivy-iac-check)

How to invoke this shared workflow:

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

## Automation

### Build lambda and upload to S3

This workflow builds lambda code and uploads the zip file to S3 bucket. The instructions for building the zip package need to be specified in a Makefile. The workflow works with Go and Python lambdas.

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

### Multi architecture docker build

All-in-one package that builds, tests, beautify and publishes a docker image for multiple architectures. This workflow uses the [Auto release](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#auto-release) workflow to create a Github Release on push to master. You have to add DOCKERHUB_USERNAME and DOCKERHUB_TOKEN secrets to your repository to use this workflow. To use the slack integration you will also have to add the SLACK_WEBHOOK secret.

How to invoke this shared workflow:

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

### Auto release

Creates a Github Release on push to master. Automatically tags the release and create release notes from git log. Change the semantic versioning by applying labels, **release:patch**, **release:minor**, **release:major**. Works best in conjuction with [Enforce PR labels](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#enforce-pr-labels).

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