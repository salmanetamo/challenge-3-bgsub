from aluLib import *
import math


# This function uses the chromakey strategy to substitute the background of the image and
# sets it to the new background provided
def chromakey(new_background, desired_front):
    # Loading our two images using the provided file names
    new_background_img = load_image(new_background)
    desired_front_img = load_image(desired_front)

    # Copying the desired front
    new_image = desired_front_img.copy()

    # Looping through each pixel of our new image and change it if need be
    for pixel_x in range(new_image.width()):
        for pixel_y in range(new_image.height()):
            # Getting the pixel at the current position for both of the images
            pixel_new_image = new_image.get_pixel(pixel_x, pixel_y)
            pixel_new_background = new_background_img.get_pixel(pixel_x, pixel_y)

            # Checking if current pixel is green enough, by comparing its green value with its red and blue values
            if pixel_new_image[1] > pixel_new_image[0] and pixel_new_image[1] > pixel_new_image[2]:
                # Setting current pixel in new image to same pixel in new background image
                new_image.set_pixel(pixel_x, pixel_y, pixel_new_background[0],
                                    pixel_new_background[1], pixel_new_background[2], pixel_new_background[3])

    # Saving our image
    new_image.save('output_chroma.jpg')


# This function uses the background substraction strategy to substitute the background of the image and
# sets it to the new background provided
def background_substraction(old_background, new_background, desired_front):
    # Loading our three images using the provided file names
    old_background_img = load_image(old_background)
    new_background_img = load_image(new_background)
    desired_front_img = load_image(desired_front)

    # Copying the desired front
    new_image = desired_front_img.copy()

    # Looping through each pixel of our new image and change it if need be
    for pixel_x in range(new_image.width()):
        for pixel_y in range(new_image.height()):
            # Getting the pixel at the current position for all three images
            pixel_new_img = new_image.get_pixel(pixel_x, pixel_y)
            pixel_old_bg = old_background_img.get_pixel(pixel_x, pixel_y)
            pixel_new_background = new_background_img.get_pixel(pixel_x, pixel_y)

            # Computing the distance between current pixel in old background and pixel in new image
            similarity_distance = math.sqrt(math.pow(pixel_old_bg[0] - pixel_new_img[0], 2) +
                                            math.pow(pixel_old_bg[1] - pixel_new_img[1], 2) +
                                            math.pow(pixel_old_bg[2] - pixel_new_img[2], 2) +
                                            math.pow(pixel_old_bg[3] - pixel_new_img[3], 2))

            # Checking if the two pixels are similar enough
            if similarity_distance < 0.325:
                # Setting current pixel in new image to same pixel in new background image
                new_image.set_pixel(pixel_x, pixel_y, pixel_new_background[0],
                                    pixel_new_background[1], pixel_new_background[2], pixel_new_background[3])

    # Saving our image
    new_image.save('output_bgsub.jpg')


# This function gets the different file names from the users and
# draws the images using the two strategies above
def main():
    print('Please enter the following: \n')

    # Prompting the users for the different image names
    old_background = input('Old background image: ')
    new_background = input('New background image: ')
    desired_front = input('Foreground image: ')

    # Creating images using both substitution strategy
    chromakey(new_background, desired_front)
    background_substraction(old_background, new_background, desired_front)

    # Drawing image from chromakey strategy with its label
    draw_image(load_image('output_chroma.jpg'), 5, 5)
    draw_text('Output chromakey', 205, 660)

    # Drawing image from background substraction strategy with its label
    draw_image(load_image('output_bgsub.jpg'), 650, 5)
    draw_text('Output background substraction', 805, 660)


start_graphics(main, width=1200, height=700)

