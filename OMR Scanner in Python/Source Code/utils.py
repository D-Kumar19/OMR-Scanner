import time
import cv2 as cv
import numpy as np
from os import path
import qr_code_scanner as qr_reader
import solution_image_reader as sol_img_reader


#################################################################
x_coord_text = 300
y_coord_text = 175

width_of_img = 300
height_of_img = 600

width_resized_img = 500
height_resized_img = 700

num_of_options = 5
num_of_questions_on_each_page = 25

total_number_of_questions = 50

prompt_for_sol_img = '\nEnter the Location of the Solution Image: '
prompt_for_quest_img = '\nEnter the Location of the Question Image: '


#################################################################


# this function will get the file from user (solution image, question image)
def get_file(prompt):
    while True:
        img_loc = input(prompt)
        path_exits = path.isfile(img_loc)
        # print(path_exits, img_loc)

        if path_exits:
            img = cv.imread(img_loc)
            break
        else:
            print('Path does not Exist!')

    return img


# this function will check if user has another question image for the same solution image to read
def read_another_quest_img():
    img = None
    while True:
        print('\nPress ''1'' if you have want to check more Question Images for same Solution Image!')
        print('Press ''2'' if you have want to Exit!')
        choice_more_quest_img = input('Enter your Choice: ')
        # print(choice_more_quest_img)

        if choice_more_quest_img == '1':
            img = get_file(prompt_for_quest_img)
            continue_or_not = True
            break
        elif choice_more_quest_img == '2':
            continue_or_not = False
            break
        else:
            print('This is an Invalid Choice!')

    # print(continue_or_not)
    # cv.imshow('Question Image', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return continue_or_not, img


# this function will get the solution image and the answers keys
def get_sol_img():
    # this function will get the path of the solution image
    sol_img = get_file(prompt_for_sol_img)
    # cv.imshow('Solution Image', sol_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # this function will read the solution image and find the boxes marked
    sol_img, first_half_sol_img, second_half_sol_img, ans, coord_img_1, mapping_coord_1, coord_img_2, mapping_coord_2 \
        = sol_img_reader.find_the_marked_boxes(sol_img)

    # print(coord_img_1, coord_img_2)
    # print(mapping_coord_1, mapping_coord_2)
    # print(ans)
    # cv.imshow('Solution Image', sol_img)
    # cv.imshow('First half of the Solution Image', first_half_sol_img)
    # cv.imshow('Second half of the Solution Image', second_half_sol_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return sol_img, ans


# this function will do the initial operations on the image for example: converting it to grayscale, blurred, canny
def initial_op_on_img(img):
    img = cv.resize(img, (width_of_img, height_of_img))
    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(grayscale_img, (5, 5), 1)
    img_canny = cv.Canny(blurred_img, 10, 50)

    # cv.imshow('Original Image', img)
    # cv.imshow('Grayscale Image', grayscale_img)
    # cv.imshow('Blurred Image', blurred_img)
    # cv.imshow('Image Canny', img_canny)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return img, img_canny


# this function will get us the corner points of the contour
def get_corner_points(contour):
    arc_length = cv.arcLength(contour, True)
    approx_shape = cv.approxPolyDP(contour, 0.02 * arc_length, True)
    # print(arc_length)
    # print(approx_shape)
    # print(len(approx_shape))

    return approx_shape


# this will get the contours whose sides are 4, so we can conclude
# it is a rectangle and later sort then according to their area
def find_and_sort_contours(img, img_canny):
    img_c = img.copy()
    img_contours = img_canny.copy()
    contours, hierarchy = cv.findContours(img_contours, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # cv.drawContours(img_c, contours, -1, (0, 255, 0), 10)
    # cv.imshow('Contours on Image', img_c)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    rect_contours = []
    for c in contours:
        contour_area = cv.contourArea(c)
        # print(contour_area)

        if contour_area > 1000:
            approx_shape = get_corner_points(c)
            if len(approx_shape) == 4:
                rect_contours.append(c)
                cv.drawContours(img_c, contours, -1, (255, 0, 0), 10)

    # print('Contours before Sorting: ')
    # print(rect_contours)
    rect_contours = sorted(rect_contours, key=cv.contourArea, reverse=True)
    # print('Contours after Sorting: ')
    # print(rect_contours)

    # cv.imshow('Rectangle Contours on Image', img_c)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return rect_contours


# this function will get the biggest first and second contour
# which will be mcq sheet, one on left and another on right
def get_two_biggest_contours(img, rect_contours):
    img_c = img.copy()
    first_half_img = get_corner_points(rect_contours[0])
    second_half_img = get_corner_points(rect_contours[1])
    # print(first_half_img)
    # print(second_half_img)
    #
    # if first_half_img.size != 0 and second_half_img.size != 0:
    #     cv.drawContours(img_c, first_half_img, -1, (0, 255, 0), 10)
    #     cv.drawContours(img_c, second_half_img, -1, (255, 0, 0), 10)
    #
    # print(first_half_img.shape)
    # print(second_half_img.shape)
    #
    # cv.imshow('Both sides of the Page', img_c)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return first_half_img, second_half_img


# this function will reorder our coordinates, so we can extract the image
def reorder_coord(biggest_contour):
    reshaped_contour = biggest_contour.reshape(4, 2)
    mapper = np.zeros((4, 1, 2), np.int32)
    summation = reshaped_contour.sum(1)
    # print(reshaped_contour)
    # print(mapper)
    # print(summation)

    mapper[0] = reshaped_contour[np.argmin(summation)]
    mapper[3] = reshaped_contour[np.argmax(summation)]

    diff = np.diff(reshaped_contour, axis=1)
    # print(diff)
    mapper[1] = reshaped_contour[np.argmin(diff)]
    mapper[2] = reshaped_contour[np.argmax(diff)]
    # print(mapper)

    return mapper


# this function will get the bird eye view of the image
def get_bird_eye_view(img, half_of_img):
    half_ordered_img = reorder_coord(half_of_img)
    coord_of_img = np.float32(half_ordered_img)
    mapping_coord = np.float32([[0, 0], [width_of_img, 0], [0, height_of_img], [width_of_img, height_of_img]])
    matrix = cv.getPerspectiveTransform(coord_of_img, mapping_coord)
    bird_eye_view = cv.warpPerspective(img, matrix, (width_of_img, height_of_img))

    # print(coord_of_img, mapping_coord)
    # cv.imshow('Bird Eye View of Image', bird_eye_view)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return coord_of_img, mapping_coord, bird_eye_view


# this will split the image by number of rows and columns
def split_the_image_in_r_and_c(img):
    img_warp_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_thresh = cv.threshold(img_warp_gray, 130, 255, cv.THRESH_BINARY_INV)[1]
    # cv.imshow('Image after GrayScale', img_warp_gray)
    # cv.imshow('Image after Threshold', img_thresh)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    options = []
    rows = np.vsplit(img_thresh, num_of_questions_on_each_page)

    for r in rows:
        # cv.imshow('Each Box', r)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        cols = np.hsplit(r, num_of_options + 1)
        cols.pop(0)
        for option in cols:
            options.append(option)
            # cv.imshow('Each Box', option)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

    return options


# this function will find the non-zero count of pixels for each image
def get_non_zero_count(options):
    col, row = 0, 0
    choices = np.zeros((num_of_questions_on_each_page, num_of_options))
    # print(choices)

    for option in options:
        non_zero_pixels = cv.countNonZero(option)
        choices[row][col] = non_zero_pixels
        # print(non_zero_pixels)
        # print(col, row)
        # print(choices[row][col])
        col += 1

        if col == num_of_options:
            row += 1
            col = 0

    # print(choices)

    return choices


# this function will find which answer was selected by student
def find_the_filled_box(options):
    ans_chosen = []
    choices = get_non_zero_count(options)

    for i in range(0, num_of_questions_on_each_page):
        row = choices[i]
        idx_of_max_value = np.argmax(row)
        ans_chosen.append(idx_of_max_value)
        # print(row)
        # print(idx_of_max_value, row[idx_of_max_value])

    # print(ans_chosen)

    return ans_chosen


# this function will put the green circle on image where student's answer is correct and red when it is incorrect
def mark_the_answers(img, start, ans, ans_of_student):
    width_of_box = int(img.shape[1] / num_of_options)
    length_of_box = int(img.shape[0] / num_of_questions_on_each_page)
    # print(width_of_box, length_of_box)

    for i in range(start, num_of_questions_on_each_page + start):
        correct_answer = ans[i]
        answer_chosen = ans_of_student[i]
        # print(correct_answer, answer_chosen)

        # green color identifies your answer is correct
        # red color identifies your answer is incorrect
        # blue color identifies correct answer for the incorrect one
        if correct_answer == answer_chosen:
            x_axis = int((correct_answer * width_of_box) + width_of_box - (correct_answer * 8))
            y_axis = int(((i - start) * length_of_box) + length_of_box - 10)
            cv.circle(img, (x_axis, y_axis), 10, (0, 255, 0), 5)
            # print(x_axis, y_axis)

        else:
            # x_axis = int((correct_answer * width_of_box) + width_of_box - (correct_answer * 8))
            # y_axis = int(((i - start) * length_of_box) + length_of_box - 10)
            # cv.circle(img, (x_axis, y_axis), 10, (255, 0, 0), 5)
            # print(x_axis, y_axis)

            x_axis = int((answer_chosen * width_of_box) + width_of_box - (answer_chosen * 8))
            y_axis = int(((i - start) * length_of_box) + length_of_box - 10)
            cv.circle(img, (x_axis, y_axis), 10, (0, 0, 255), 5)
            # print(x_axis, y_axis)

    # cv.imshow('Image after Correct and Incorrect Answers Marked', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return img


# this function will count the number of correct answers chosen by student
def count_correct_answers(ans, answer_of_student):
    score = 0
    grading = []
    for i in range(0, total_number_of_questions):
        if ans[i] == answer_of_student[i]:
            grading.append(1)
            score += 1
        else:
            grading.append(0)
    percent = (score / total_number_of_questions) * 100

    # print(score)
    # print(percent)
    # print(grading)

    return score, percent, grading


# this function will print the answer from bird eye view image to the original image
def add_weight(img, first_half_quest_img_c, start_of_loop, ans, ans_of_student, mapping_coord_1, coord_img_1):
    raw_img = np.zeros_like(first_half_quest_img_c)
    raw_img = mark_the_answers(raw_img, start_of_loop, ans, ans_of_student)
    inverse_of_matrix = cv.getPerspectiveTransform(mapping_coord_1, coord_img_1)
    inverse_warp_img = cv.warpPerspective(raw_img, inverse_of_matrix, (width_of_img, height_of_img))
    img = cv.addWeighted(img, 1, inverse_warp_img, 1, 0)

    # cv.imshow('Raw Drawing of Image', raw_img)
    # cv.imshow('Final Image after Weights', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return img


# this function will resize the final image which will be shown to user
def resize_img(img):
    img = cv.resize(img, (width_resized_img, height_resized_img))

    # cv.imshow('Final Resized Image', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return img


# this function will put result on the question image
def print_result(img, percent):
    cv.putText(img, str(int(percent)) + "%", (x_coord_text, y_coord_text), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 5)

    # cv.imshow('Final Question Image with Answers Marked', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return img


# this function will help us to show the results to the user
def show_the_results(sol_img, result_img):
    try:
        cv.imshow('Solution Image', sol_img)
        cv.imshow('Final Results', result_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    except:
        return None


# this function will get the timestamp which will be used to combine with result image to store the results
def get_time_stamp():
    time_stamp = time.strftime("%Y%m%d-%H%M%S")
    file_name = ("Final_Result-" + time_stamp + '.PNG')

    # print(time_stamp, file_name)

    return file_name


# this function will save the results image in the main directory
def save_results(img):
    value = qr_reader.read_qr_code(img)
    file_name = get_time_stamp()
    status = cv.imwrite(file_name, img)

    # print(value, file_name)
    print("Image saved Status: ", status)
