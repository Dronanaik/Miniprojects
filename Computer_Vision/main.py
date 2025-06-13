from gemini_locator import find_element_coordinates

# Change this to match your image and element name
image_path = "images/demo.jpg"
element_name = "username"

coordinates = find_element_coordinates(image_path, element_name)
print(f"Coordinates for '{element_name}': {coordinates}")
