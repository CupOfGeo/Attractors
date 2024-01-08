data "google_project" "current" {}

resource "google_cloud_run_service" "cloudrun_service" {
  name     = var.service_name
  location = var.ar_repo_location

  template {
    spec {
      containers {
        image = "${var.ar_repo_location}-docker.pkg.dev/${data.google_project.current.name}/${var.ar_repo_name}/${var.container_image}:latest"
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
  count    = var.is_public ? 1 : 0
  service  = google_cloud_run_service.cloudrun_service.name
  location = google_cloud_run_service.cloudrun_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "cloudrun_service_url" {
  description = "The URL of the cloud run service"
  value       = google_cloud_run_service.cloudrun_service.status[0].url
}
