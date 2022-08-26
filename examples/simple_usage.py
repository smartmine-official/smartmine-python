import smartmine

smartmine.username = input("Username: ")
smartmine.password = input("Password: ")

smartmine.process_image(
    service_name=smartmine.ServiceName.image_restoration,
    load_path="examples/images/earth.png",
    save_path="results/earth_restored.png",
)
