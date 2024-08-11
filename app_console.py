from image_clasification import classify_new_image
from PIL import Image
from IPython.display import display

new_image_path = 'images_dataset/users_image/image17.jpg'
label = classify_new_image(new_image_path)
print(f"The new image is classified as: {label}")

image = Image.open(new_image_path)

thumbnail_size = (150, 150) 
image.thumbnail(thumbnail_size)

display(image)

print(f"The new image is classified as: {label}")    