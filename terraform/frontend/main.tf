variable "ar_repo_name" {
  description = "The name of the Artifact Registry repository"
  type        = string
}
resource "google_cloud_run_service" "cloudrun_frontend_service" {
  name     = "attractors-frontend-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/geo-attractors/${var.ar_repo_name}/attractors-frontend:latest"
        resources {
          limits = {
            cpu    = "1000m"
            memory = "1Gi"
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
  service  = google_cloud_run_service.cloudrun_frontend_service.name
  location = google_cloud_run_service.cloudrun_frontend_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
