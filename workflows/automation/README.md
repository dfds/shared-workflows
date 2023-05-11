# Automation

## Enforce PR labels

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
    uses: dfds/shared-workflows/workflows/automation/enforce-release-labels.yml@master
```

## Build lambda and upload to S3

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
    uses: dfds/shared-workflows/workflows/automation/build-and-upload-to-s3.yml@master
    with:
      role-session-name: samplesessionname #Session name
      working-directory: ./working-directory #The working directory that includes the Makefile
      lambda-package-name: lambda-package.zip #The lambda package name 
      s3-location: s3-location #The S3 location to put the artifact
    secrets:
      role-to-assume: ${{ secrets.ROLE_TO_ASSUME }} #Repository secret with the AWS role to be assumed
```

## Auto release holy moly

Github Action to create a Github Release on pushes to master. Automatically tags the release and create release notes from git log. Change the semantic versioning by applying labels, **release:patch**, **release:minor**, **release:major**. Works best in conjuction with [Enforce PR labels](https://github.com/dfds/shared-workflows/tree/master/workflows/automation#enforce-pr-labels).

[Marketplace](https://github.com/marketplace/actions/tag-release-on-push-action)

How to invoke this shared workflow:

```yaml
name: Auto release holy moly

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/workflows/automation/auto-release.yml@master
```