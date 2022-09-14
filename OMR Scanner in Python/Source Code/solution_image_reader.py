import utils
import cv2 as cv


# this function will read the image and give us all the marked options by student in an array
def find_the_marked_boxes(img):
    try:
        # this will do the initial operations on the image for example: converting it to grayscale, blurred, canny
        img, img_canny = utils.initial_op_on_img(img)
        img_c = img.copy()
        # cv.imshow('Original Image', img)
        # cv.imshow('Image Canny', img_canny)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        # this will get the contours which are rectangle and sort them by their area
        rect_contours = utils.find_and_sort_contours(img_c, img_canny)
        # print(rect_contours)

        # this will get the biggest first and second contour which will be mcq sheet, one on left and another on right
        first_half_img, second_half_img = utils.get_two_biggest_contours(img_c, rect_contours)
        # print(first_half_img)
        # print(second_half_img)

        # this will get the bird-eye-view of the image and will also get the coordinates
        # which later can be used to bring the marks back on original image
        coord_img_1, mapping_coord_1, first_half_img = utils.get_bird_eye_view(img_c, first_half_img)
        coord_img_2, mapping_coord_2, second_half_img = utils.get_bird_eye_view(img_c, second_half_img)
        # print(coord_img_1, mapping_coord_1)
        # print(coord_img_2, mapping_coord_2)
        # cv.imshow('Bird Eye View of First Half', first_half_img)
        # cv.imshow('Bird Eye View of Second Half', second_half_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        # this will split the image by number of rows and columns
        options_first_img = utils.split_the_image_in_r_and_c(first_half_img)
        options_second_img = utils.split_the_image_in_r_and_c(second_half_img)

        # now we have all the options, so we will just check which options was selected by the student
        ans_first_img = utils.find_the_filled_box(options_first_img)
        ans_second_img = utils.find_the_filled_box(options_second_img)
        ans = ans_first_img + ans_second_img
        # print(ans_first_img)
        # print(ans_second_img)
        # print(ans)

        return img, first_half_img, second_half_img, ans, coord_img_1, mapping_coord_1, coord_img_2, mapping_coord_2

    except:
        # print('Rectangle Contours can not be detected so move forward!'))
        return None
