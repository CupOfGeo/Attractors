provider "google" {
  project = "geo-attractors"
  region  = "us-central1"
}

data "google_project" "current" {
  project_id = "geo-attractors"
}

terraform {
  backend "gcs" {
    bucket = "geo-attractors-tfstate"
    prefix = "terraform/state"
  }
}

resource "google_artifact_registry_repository" "my_ar_repo" {
  location      = "us-central1"
  repository_id = "attractors"
  format        = "DOCKER"
}

resource "google_project_iam_member" "artifact_registry_reader" {
  project = data.google_project.current.name
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:service-${data.google_project.current.number}@serverless-robot-prod.iam.gserviceaccount.com"
}


module "backend" {
  source           = "./cloudrun"
  service_name     = "attractors-backend-service"
  container_image  = "attractors-backend"
  ar_repo_name     = google_artifact_registry_repository.my_ar_repo.name
  ar_repo_location = google_artifact_registry_repository.my_ar_repo.location
  is_public        = true
}

module "frontend" {
  source           = "./cloudrun"
  service_name     = "attractors-frontend-service"
  container_image  = "attractors-frontend"
  backend_url_env  = module.backend.cloudrun_service_url
  ar_repo_name     = google_artifact_registry_repository.my_ar_repo.name
  ar_repo_location = google_artifact_registry_repository.my_ar_repo.location
  is_public        = true
}

# https://github.com/terraform-google-modules/terraform-google-github-actions-runners/blob/master/modules/gh-oidc/README.md
module "gh-federation" {
  source  = "./gh-id-federation"
  project_id  = data.google_project.current.name
}
