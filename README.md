# Shared workflows

A repository for shared action workflows, best practice for new and existing repositories.

Shared workflows:
- [Gitleaks](https://github.com/dfds/shared-workflows#gitleaks)
- [Enforce PR labels](https://github.com/dfds/shared-workflows#enforce-pr-labels)
- [Auto release](https://github.com/dfds/shared-workflows#auto-release)

## Gitleaks

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

## Enforce PR labels

Enforce assigning labels before merging PR's. Usefull for generating automatic changelog and release notes with [Auto release](https://github.com/dfds/shared-workflows#auto-release).

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

## Auto release

Github Action to create a Github Release on pushes to master. Automatically tags the release and create release notes from got log. Works best in conjuction with [Enforce PR labels](https://github.com/dfds/shared-workflows#enforce-pr-labels)

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