

Challenge 3: Background substitution
=======================

Time to tackle some more complex tasks. You will notice that this assignment will actually require you to write less
code than before, but will need you to think harder and understand new concepts.

As usual, you can find a workplan below to help you tackle the problem. Even more so than before, read this slowly and 
carefully.

The objective
-------------
Your program should insert _new backgrounds_ onto existing pictures, and will do so using 2 different strategies:
- Background substraction.
- Chromakey.

I will explain both concepts below, then give further instructions on how to approach the challenge.

### Strategy 1: Chromakey

This strategy will require only 2 images to work:
- An image of the new background - like beachBahamas.jpg
- An image of the desired front - like Onsongo.jpg This picture should be taken in front of the old background.

Ideally we want our desired front (Professor Onsongo) to now have the new background behind him. How do we achieve this?

First, let's make sure we understand how images work: Each image we deal with here is composed of many pixels.

How many exactly? well the width of an image is measured in pixels, and so is its height, so the image will have 
width*height pixels.

Each pixel is made of a combination of r, g, and b values, which define the color of said pixel.

The way we approach the Chromakey strategy is to:
1. Create a copy of the desired front, let's call it **new image**. We will modify this image and it will be our final output.
1. Go through each pixel in the image, and ask: Is this pixel green enough?. 
1. If the pixel is green enough, then it must be from the background. Therefore we don't want them: replace that 
specific pixel with the same pixel from **the new background**
1. Otherwise, then the pixel from the **new image** must be part of the front we want, so we keep it.
1. Once you've gone through all the pixels, save and display the new image.

What does it mean to be "green enough" ? This is where you will have to get creative. You have access to the r, g, and b 
values of each pixel in the picture, see what you can do with it. Some popular approaches include:
- checking if the green value is higher than the red, and higher than the blue value.
- checking if the green value is higher than the sum of red and blue value.
- checking if the green value hits any particular threshold.

Try a few different approaches, and leave comments as to what you've tried. Submit the one that gave you the best results.

Strategy 2: Background Substraction
-----------------------------------

This strategy will require 3 images to work:
- An image of the old background - like empty_chair.jpg
- An image of the new background - like beachBahamas.jpg
- An image of the desired front - like Onsongo.jpg This picture should be taken in front of the old background.

Once again, we want our desired front (Professor Onsongo) to now have the new background behind him. 

Now the way we approach the Background Substraction strategy is to:
1. Create a copy of the desired front, let's call it **new image**. We will modify this image and it will be our final output.
1. Go through each pixel in the image, and compare it with a pixel from old background. 
1. If the two pixels are similar enough, then they must be from the old background. Therefore we don't want them: replace that 
specific pixel with the same pixel from **the new background**
1. If the two pixels are different, then the pixel from the **new image** must be part of the front we want, so we keep it.
1. Once you've gone through all the pixels, save and display the new image.

Requirements
------------

Your program should ask the user for:
- The name of the old background file
- The name of the new background file
- The name of the foreground file

Once it has all this information, your program should then
- Create and save a file using the first strategy. call that file __output_bgsub.jpg__
- Create and save a file using the second strategy. call that file __output_chroma.jpg__

Your program should then display, using aluLib, both your output images, one next to the other.
Write next to each image which one is which using the **draw_text()** function in aluLib.

Checkpoint 1 : getting familiar with CS1Image
---------------------------------------------
Inside aluLib is a class you have used in the past without being aware of it: **CS1Image**
To create a CS1Image object you can use the familiar: 
``` {.sourceCode .python}
from aluLib import *
# The variable below will store information about how to draw the Ace
img = load_image("Onsongo.jpg")

img here is in fact a CS1Image object.
```

There are some important methods available to CS1Image objects that you will probably need:
- ``img.width()`` and ``img.height()`` return an int for the width and height respectively.
- ``img.get_pixel(x, y)`` return a list, which describes the color of the pixel at position x, y in the image. The first 
element in that list is the **r** value, the second the **g** value, the third the **b** value, the fourth and last one
is the brightness but you can ignore this.
- ``img.set_pixel(x, y, r, g, b)`` modifies the pixel at position x, y to the r,g,b values provided.
- Note that the two methods above will error if you give them x, y values that are not valid.
- ``img.save(save_path)`` saves the image in the location described by save_path. for example img.save(assets/outputs/test.jpg)
will create an image called test.jpg in the folder assets/output.
- ``img.copy()`` returns a new CS1Image object that is the same as img. 

Recall as well that you can draw an image using ``draw_image(img_object, x, y)``

Start by creating a program that asks the user for the path to all the relevant images, then creates a copy of one of them, 
saves it, and displays it. You don't need to do any substitution yet, this just makes sure you are comfortable with the basics
of creating, drawing, and saving images.

Checkpoint 2: Implementing Chromakey
----------------------------------------

At this point, you should be able to create a function that implements the chromakey approach.

In order to do this, you need to check **every single picture** of the image, and ask if they are green enough.
How do we loop over all the pixels in an image? recall that there are img.width() * img.height() pixels in it.

One way to think about this is _for each possible value for the pixel width_, there are __img.height different pixels__

Or in other words: if an image is 500px wide, and 200 px high, then there are 200 pixels with an x coordinate of 0, like 
(0,0) (0,1) (0, 2) all the way to (0, 200).
similarly there are 200 pixels with an x coordinate of 1: (1, 0), (1, 1)...(1, 200)

That means that if you loop over each possible x coordinate, for each one of them, you should loop through all possible 
y coordinates.

Once you set up this loop correctly, you should be good to go with implementing the chromakey strategy.

Checkpoint 3: Implementing background substraction
--------------------------------------------------
The idea is quite similar to the above. Your new function will still have to loop through all the pixels, but this time 
instead of just looking at the pixels of one image, you will be looking at the pixels of both images, and checking if 
they are close enough.

First, let's make sure we understand why we can't just ask if the pixel's colors are the same: The answer is light! Each 
picture might have slightly different brightness. The person posing might cast a bit of a shadow. This makes it hard to
guarantee that the pixels remain exactly the same between the two images, that is fine though, we can decide what it means 
for them to be close enough.

How do we approach this? There is a technique that is very important when figuring out: vectorization.

Basically, you can treat any color as a vector, where the 3 axes represent red, blue, and green. Therefore you can use 
them to determine some kind of distance. For example if we have color 1 represented by (0.5, 0.5, 0.5), and color 
represented by (0.2, 0, 0.5), how far are those 2 colors from each other? well, the math course gives us the answer:
`distance = The square root of ((0.5-0.2) to the power of 2 + (0.5-0) to the power of 2 + (0.5-0.5) to the power of 2)`

You should be able to translate this to code quite easily, simply make sure to include the following:
```
import math
math.sqrt(4) # will return 2.0
```

Note that this only gives you a notion of distance, you should experiment to find what result should be deemed close
enough.

Design and style
----------------

Your program should be understandable with minimum possible effort.  The logic
should be as straightforward as possible.  The beauty of a program lies in its design and in its style.

### Functions

Don't be afraid to write functions that help your program out. I
mentioned a couple earlier. But you should feel free to write
more. Your functions should all be near the top of your code, not mixed in with code at the global level. This makes it easy to quickly see what functions you will be using.


### Documentation

You should include comments that tell the human reader what he or she needs
to understand in order to make sense of your program.  You should also choose descriptive variable and function names.
Meaningless names are bad, and misleading names are worse.

Grading
-------

Correctness:

-   Each strategy is implemented correctly
-   The program asks for user input and stores the information appropriately
-   The program creates and saves new files

Coding proficiency:

- You correctly use functions to organize the code's logic
- Drawing is done as per the standards of aluLib.
- Any logic in the code is handled clearly and elegantly. If statements are used appropriately.

Style:

-   Clear design and organization.
-   Good variable names, function names, and comments.
-   Functions where appropriate and not where inappropriate.
-   In this case in particular, determine why you have picked the values you've picked for thresholds in both strategies.
## Honor Code

Please make sure that you fully understand the Academic Honor System, and reach out if you need any clarifications. 


What to turn in
---------------

Make sure your git repository contains the following:
- A single python file for your submission game.
- Optionally: a second python file for the extra credit version of the game
- A text file describing the following:
    - An acknowledgement of upholding the honor code, or information if any breach occurred.
    - Any extra credits or additional features you attempted.
    - Any notes you want to bring to the attention of the grader. 


Extra Credit
------------

You can add all sorts of features to the submission for extra
credit. Make sure, however, before you charge off and do extra credit
that you have the basic game working correctly, that you've designed it
as cleanly as possible, and that you've documented it well. Remember, the extra credit points don't really count for anything.

Also, **before you start any extra credit, save your basic submission source
code, and submit that as your main submission. Also take a screenshot
for submission before working on extra credit. Start a new Python file
for any extra credit.**  If you do pursue extra credit, include a text
file in your submission that tells us what extra-credit features you've
included.