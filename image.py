from PIL import Image

# List to store the input images
images = []

# Capture 10 images from user input
for _ in range(2):
    image_path = input("Enter image path: ")
    image = Image.open(image_path)
    images.append(image)

# Get the width and height of the input images
width, height = images[0].size

# Calculate the total width for the final image
total_width = width * len(images)

# Create a new blank image with the appropriate size
new_image = Image.new('RGB', (total_width, height))

# Paste each image onto the new image
for i, image in enumerate(images):
    new_image.paste(image, (i * width, 0))

# Display or save the new image
new_image.show()
# new_image.save("path_to_save_image.jpg")
