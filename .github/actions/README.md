# Actions

### build-push-container-dh

Builds container via specified context path and pushes the built image to Docker Hub

### build-push-container-ecr

Builds container via specified context path and pushes the built image to AWS ECR. Expects AWS authentication using OIDC. See [this](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) for more information.
