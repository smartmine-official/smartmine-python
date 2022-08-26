import os
from pathlib import Path

import smartmine

smartmine.username = os.environ.get("SMARTMINE_USERNAME")
smartmine.password = os.environ.get("SMARTMINE_PASSWORD")


# Bulk process images
smartmine.bulk_process_images(
    service_name=smartmine.ServiceName.image_restoration,
    load_dir="examples/images/",
    save_dir=str(Path.home() / "Downloads"),
)
