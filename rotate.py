from PIL import Image
import math


def rotation_no_centering(point, angle):
    cosine_theta = math.cos(-angle)
    sine_theta = math.sin(-angle)

    x = point[0]
    y = point[1]

    new_x = cosine_theta * x - sine_theta * y
    new_y = sine_theta * x + cosine_theta * y

    return (new_x, new_y)


def rotation_fast(point, cosine_theta, sine_theta):
    x = point[0]
    y = point[1]

    dx = - cosine_theta * image.width/2 + sine_theta*image.height/2+image.width/2
    dy = - sine_theta * image.width/2 - cosine_theta * image.height/2+image.height/2

    new_x = cosine_theta * x - sine_theta * y + dx
    new_y = sine_theta * x + cosine_theta * y + dy

    return (new_x, new_y)


image = Image.open("code.image.jpg")
data = image.load()

# Calculate new canvas size
angle = .5

corners = [[-image.width/2, -image.height/2],
           [image.width/2, -image.height/2],
           [image.width/2, image.height/2],
           [-image.width/2, image.height/2]]

max_x = 0
max_y = 0

for corner in corners:
    new_corner = rotation_no_centering(corner, angle)

    if new_corner[0] > max_x:
        max_x = new_corner[0]
    if new_corner[1] > max_y:
        max_y = new_corner[1]

# Generate a new canvas that is expanded to hold the image
new_image = Image.new("RGB", (int(max_x*2), int(max_y*2)))
new_data = new_image.load()


# Remember that since we are sampling backwards, we need -angle
cosine_theta = math.cos(-angle)
sine_theta = math.sin(-angle)

# Account for the differenence in the size of the original canvas and the expanded canvas
offset_x = (image.width - new_image.width)/2
offset_y = (image.height - new_image.height)/2


# Loop over all the point and sample the original image
for y in range(new_image.height):
    for x in range(new_image.width):
        new_x, new_y = rotation_fast(
            (x + offset_x, y + offset_y), cosine_theta, sine_theta)

        new_x //= 1
        new_y //= 1

        if 0 <= new_x < image.width and 0 <= new_y < image.height:
            new_data[x, y] = data[new_x, new_y]
        else:
            new_data[x, y] = (0, 0, 0)

new_image.save("code.out.rotation.png")
