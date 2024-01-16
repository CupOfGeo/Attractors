variable "location" {
  type        = string
  description = "GCP region"
  default     = "us-central1"
}

variable "ar_repo_location" {
  description = "The location of the Artifact Registry repository and the cloudrun service"
  type        = string
}

variable "ar_repo_name" {
  description = "The name of the Artifact Registry repository"
  type        = string
}

variable "container_image" {
  type        = string
  description = "image in GAR"
}

variable "service_name" {
  type        = string
  description = "cloudrun service name"
}

variable "is_public" {
  type        = bool
  description = "Should the service be public"
}

variable "backend_url_env" {
  type        = string
  description = "The URL of the backend service"
  default     = "None"
}
