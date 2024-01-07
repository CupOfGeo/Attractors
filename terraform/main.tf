provider "google" {
  project = "geo-attractors"
  region  = "us-central1"
}


terraform {
  backend "gcs" {
    bucket = "geo-attractors-tfstate"
    prefix = "terraform/state"
  }
}

data "google_project" "current" {
  project_id = "geo-attractors"
}

resource "google_artifact_registry_repository" "my_ar_repo" {
  location      = "us-central1"
  repository_id = "attractors"
  format        = "DOCKER"
}

resource "google_project_iam_member" "artifact_registry_reader" {
  project = "geo-attractors"
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:service-${data.google_project.current.number}@serverless-robot-prod.iam.gserviceaccount.com"
}

resource "google_cloud_run_service" "my_cloudrun_service" {
  name     = "attractors-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/geo-attractors/${google_artifact_registry_repository.my_ar_repo.name}/attractors-fastapi:latest"
        resources {
          limits = {
            cpu    = "1000m"
            memory = "2Gi"
          }
        }
        env {
          name  = "MY_ENV_VAR"
          value = "my-value"
        }
        ports {
          container_port = 8080
        }
      }
      timeout_seconds = 300
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.my_cloudrun_service.name
  location = google_cloud_run_service.my_cloudrun_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

module "frontend" {
  source       = "./frontend"
  ar_repo_name = google_artifact_registry_repository.my_ar_repo.name
}
