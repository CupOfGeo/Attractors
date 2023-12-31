import subprocess

from src.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    cmd = "gunicorn 'src.application:get_app()'"
    cmd += f" -w {settings.workers_count} -b {settings.host}:{settings.port}"
    cmd += f" --log-level {settings.log_level.value.lower()}"
    if settings.reload:
        cmd += " --reload"
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
