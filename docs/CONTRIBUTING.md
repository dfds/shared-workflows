# How to Contribute

Contributions to this project are very welcome! We follow a fairly standard pull request process for contributions.

## How to add a workflow

- Clone the repository
- Create a new branch
- Add your shared workflow in `.github/workflows` folder
- Add an example of usage in the `examples` folder

### Naming convention

The example file must be prefixed with a type/category name and a hyphen, this is used for auto generating the README.

Example:
<br />
`security-`gitleaks.yml

The workflow filename and example filename must match.

Example:
<br />
.github/workflows/`security-gitleaks.yml`
<br />
examples/`security-gitleaks.yml`

### How to structure the workflow

The only requirement in the workflow file is that it only have one trigger, the `workflow_call` event. This enables the workflow to be called programmatically, any other event triggers would cause the workflow to run within this repository.

### How to structure the example

- name
    - Name of the workflow
- description
    - **Optional** The description of the workflow
- author
    - **Optional** Link to marketplace action if this is an extension
- Inputs, secrets, triggers etc
- jobs

Example:
<br />
```yaml
name: Example workflow
description: This is an example workflow
author: https://github.com/marketplace/actions/example

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    uses: dfds/shared-workflows/.github/workflows/example.yml@master
```

The example must be completely copy-paste ready and **not** a draft or WIP. If any modifications are required by the consumer, provide this information in the description of the example.

## Updating the README

The README is automatically updated if the guidelines are respected. Those changes will be appended to your PR, please verify when the automation has run.

## Create a pull request

Do not push directly to master, this will break the automation and the README will not include the new workflow.

- Provide a short description of the change
- Verify that the README build automation ran successfully
- Wait for a reviewer to accept the PR
- Merge the PR