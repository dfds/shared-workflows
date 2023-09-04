# How to Contribute

Contributions to this project are very welcome! We follow a fairly standard pull request process for contributions. It is **NOT** recommended to create a PR before a branch is ready for review, because every commit to that PR will trigger a new version of the readme.

Index:
- [Workflows](#how-to-add-a-workflow)
	- [Workflow naming convention](#workflow-naming-convention)
	- [How to structure the workflow](#how-to-structure-the-workflow)
	- [How to structure the example workflow](#how-to-structure-the-example-workflow)
  - [Modifying an existing workflow](#modifying-an-existing-workflow)
- [Actions](#how-to-add-an-action)
	- [Action naming convention](#action-naming-convention)
	- [How to structure the action](#how-to-structure-the-action)
	- [How to structure the example action](#how-to-structure-the-example-action)
  - [Modifying an existing action](#modifying-an-existing-action)
- [Updating the README](#updating-the-readme)
- [Create a pull request](#create-a-pull-request)

## How to add a workflow

- Clone the repository
- Create a new branch
- Add your shared workflow in `.github/workflows` folder
- Add an example of usage in the `examples` folder

### Workflow naming convention

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

### How to structure the example workflow

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

### Modifying an existing Workflow

If you need to modify an existing workflow please make best effort to ensure it is backwards compatible. If any new inputs are added please add them to the example action.

## How to add an action

- Clone the repository
- Create a new branch
- Add your `action.yml` in `.github/actions/action-name` folder
- Add an example of usage in the `examples` folder

### Action naming convention

The example file must be prefixed with a type/category name and a hyphen, this is used for auto generating the README.

Example:
<br />
`security-`gitleaks.yml

The action folder and example filename must match. The action filename must always be `action.yml`.

Example:
<br />
.github/actions/`security-gitleaks`/action.yml
<br />
examples/`security-gitleaks.yml`

### How to structure the action

The only requirement in the action file is that it must use composite. [Examples and explaination here](https://github.com/orgs/community/discussions/36861)

Example:
<br />
```yaml
name: Test action

runs:
  using: "composite"
  steps:
    - name: Echo hello
      shell: bash
      run: echo "Hello"
```

### How to structure the example action

To use a composite action, the example **must** first checkout the shared-workflows repository.

- name
    - Name of the action
- description
    - **Optional** The description of the workflow
- Inputs, secrets, triggers etc
- jobs

Example:
<br />
```yaml
name: Example action
description: This is an example action

on:
  push:
    branches: [ "master", "main" ]

jobs:
  shared:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@master
        with:
          repository: dfds/shared-workflows
          ref: master
          path: ./.github/tmp
      - name: Test action
        uses: ./.github/tmp/.github/actions/test-action/
```

The example must be completely copy-paste ready and **not** a draft or WIP. If any modifications are required by the consumer, provide this information in the description of the example.

### Modifying an existing Action

If you need to modify an existing action please make best effort to ensure it is backwards compatible. If any new inputs are added please add them to the example action.

## Updating the README

The README is automatically updated if the guidelines are respected. Those changes will be appended to your PR, please verify when the automation has run.

> [!WARNING]
> Please **DO NOT** update the README manually. Ensure you update the examples if you modify an existing workflow or action to have the README updated automatically.

## Create a pull request

Do not push directly to master, this will break the automation and the README will not include the new workflow or action.

- Provide a short description of the change
- Verify that the README build automation ran successfully
- Wait for a reviewer to accept the PR
- Merge the PR
