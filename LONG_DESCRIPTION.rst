Official Smartmine Bindings for Python
======================================

A Python library for Smartmine's API.


Setup
-----

You can install this package by using the pip tool and installing:

    pip install smartmine



Setting up a Smartmine Account
------------------------------

Sign up for Smartmine at https://ap.smartmine.net/pricing.

Using the Smartmine API
-----------------------

General Usage:

.. code-block:: python

    import smartmine
    from smartmine import ServiceName

    smartmine.username = input("Username: ")
    smartmine.password = input("Password: ")

    smartmine.process_image(
        service_name=ServiceName.image_restoration,
        load_path="examples/images/earth.png",
        save_path="results/earth_restored.png",
    )


Advanced Usage:

.. code-block:: python

    import os
    from pathlib import Path

    import smartmine
    from smartmine import ServiceName

    smartmine.username = os.environ.get("SMARTMINE_USERNAME")
    smartmine.password = os.environ.get("SMARTMINE_PASSWORD")


    # Bulk process images
    smartmine.bulk_process_images(
        service_name=ServiceName.image_restoration,
        load_dir="examples/images/",
        save_dir=str(Path.home() / "Downloads"),
    )
