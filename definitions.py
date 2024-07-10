from pathlib import Path


short_timeout = 10
long_timeout = 120

root_path = Path(__file__).resolve().parent
resources_folder = root_path / "resources"
driver_download_path = resources_folder / "downloads"
files_resources_folder = resources_folder / "files"
log_dir = root_path / "logs"
