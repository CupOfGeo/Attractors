<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [google_cloud_run_service.cloudrun_service](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_run_service) | resource |
| [google_cloud_run_service_iam_member.public](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_run_service_iam_member) | resource |
| [google_project.current](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/project) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ar_repo_location"></a> [ar\_repo\_location](#input\_ar\_repo\_location) | The location of the Artifact Registry repository and the cloudrun service | `string` | n/a | yes |
| <a name="input_ar_repo_name"></a> [ar\_repo\_name](#input\_ar\_repo\_name) | The name of the Artifact Registry repository | `string` | n/a | yes |
| <a name="input_container_image"></a> [container\_image](#input\_container\_image) | image in GAR | `string` | n/a | yes |
| <a name="input_is_public"></a> [is\_public](#input\_is\_public) | Should the service be public | `bool` | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | GCP region | `string` | `"us-central1"` | no |
| <a name="input_service_name"></a> [service\_name](#input\_service\_name) | cloudrun service name | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_cloudrun_service_url"></a> [cloudrun\_service\_url](#output\_cloudrun\_service\_url) | The URL of the cloud run service |
<!-- END_TF_DOCS -->
