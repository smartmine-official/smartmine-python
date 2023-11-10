Official Smartmine Bindings for Python
======================================

A Python library for Smartmine's API.


Setup
-----

You can install this package by using the pip tool and installing:

    pip install smartmine



Setting up a Smartmine Account
------------------------------

Register for a free Smartmine account at https://ai.smartmine.net/service/computer-vision/image-enhancement

Try Services
------------

The following services are available at Smartmine for you to try via the frontend before integrating with the API:

- `Automated subtitling and translation <https://ai.smartmine.net/service/speech-recognition/captioning>`_
- `Image Enhancement <https://ai.smartmine.net/service/computer-vision/image-enhancement>`_
- `Image Upscaling <https://ai.smartmine.net/service/computer-vision/image-super-resolution>`_
- `Image Sharpening <https://ai.smartmine.net/service/computer-vision/image-deblurring>`_
- `Image De-noising <https://ai.smartmine.net/service/computer-vision/image-denoising>`_
- `Image Restoration <https://ai.smartmine.net/service/computer-vision/image-restoration>`_


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


Running Tests
-------------

First, make sure you have your Smartmine username and password ready, then set these as environment variables, i.e.:

    export SMARTMINE_USERNAME=<username>
    export SMARTMINE_PASSWORD=<password>

Then, use `pytest` to run unit tests:

    pytest -vv --exitfirst smartmine/
