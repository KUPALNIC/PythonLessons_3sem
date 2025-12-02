from PIL import Image
import numpy as np
# считаем картинку в numpy array
img = Image.open('lunar02_raw.jpg')
data = np.array(img)

print(np.min(data), np.max(data))

strech_data = (data - np.min(data)) * 255.0 / (np.max(data) - np.min(data))
strech_img = Image.fromarray(strech_data)
Image._show(strech_img)

