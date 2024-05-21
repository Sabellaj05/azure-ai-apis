import time
import uuid
import matplotlib.pyplot as plt
import matplotlib as mpl

# display error and couldn't save use Agg
mpl.use('Agg')

def show_image(image):
     final_image_rgb = image[:, :, ::-1]

     plt.figure(figsize=(10, 10))
     plt.imshow(final_image_rgb)
     plt.axis('off')
     plt.show()


def unique_name(name="image", extension=".jpg"):
    timestamp = time.strftime("%d-%m-%Y")
    uid = uuid.uuid4()
    return f"{name}_{timestamp}_{uid}{extension}"
