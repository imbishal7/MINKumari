from GrabzIt import GrabzItClient
from GrabzIt import GrabzItImageOptions
from PIL import Image, ImageOps

key = ''
secret = ''


def crop_image(filename):
  image = Image.open(filename).convert('L')
  image = ImageOps.invert(image)

  crop_height = 800
  num_images = (image.height // crop_height) + 1
  images = []
  for i in range(num_images):
    x0 = 0
    y0 = i * crop_height
    x1 = image.width
    y1 = min((i + 1) * crop_height, image.height)

    crop = image.crop((x0, y0, x1, y1))
    if crop.getbbox() is None:
      continue

    crop.save(f'cropped_images/output_{i}.jpg')
    images.append(f'cropped_images/output_{i}.jpg')
  return images


def get_image_from_html(html):

  grabzIt = GrabzItClient.GrabzItClient(key, secret)

  options = GrabzItImageOptions.GrabzItImageOptions()
  options.browserWidth = 400
  options.browserHeight = -1
  options.hd = True

  filename = 'scraped.jpg'
  grabzIt.HTMLToImage(html, options=options)
  grabzIt.SaveTo('temp/' + filename)

  images = crop_image('temp/' + filename)

  return images
