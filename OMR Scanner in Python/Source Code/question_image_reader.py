import utils
import cv2 as cv
import solution_image_reader as sol_reader

#################################################################
start_of_loop = 0
questions_on_half_page = 25

#################################################################


# this function will take the answers and path of question image then will
# mark it and give the image on which final score will be written
def get_the_results(sol_img, ans, quest_img):
    try:
        quest_img, first_half_quest_img, second_half_quest_img, ans_of_student, coord_img_1, mapping_coord_1, \
            coord_img_2, mapping_coord_2 = sol_reader.find_the_marked_boxes(quest_img)
        first_half_quest_img_c = first_half_quest_img.copy()
        second_half_quest_img_c = second_half_quest_img.copy()
        # print(coord_img_1, coord_img_2, mapping_coord_1, mapping_coord_2)
        # print(ans_of_student)
        # cv.imshow('Question Image', quest_img)
        # cv.imshow('First half of the Question Image', first_half_quest_img)
        # cv.imshow('Second half of the Question Image', second_half_quest_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        # this will give us the array with 0 and 1. 0 for incorrect and 1 for correct answer
        score, percent, grading = utils.count_correct_answers(ans, ans_of_student)
        # print(grading)
        print('Number of correct answers are: ', score)
        print('Percentage of your correct answers is: ', percent, '%')

        # this will place marks: a green mark for correct answer and red mark for incorrect answer
        first_half_img_choices_marked = utils.mark_the_answers(first_half_quest_img, start_of_loop,
                                                               ans, ans_of_student)
        second_half_img_choices_marked = utils.mark_the_answers(second_half_quest_img, start_of_loop
                                                                + questions_on_half_page, ans, ans_of_student)
        # cv.imshow('First half of the Question Image Marked', first_half_img_choices_marked)
        # cv.imshow('Second half of the Question Image Marked', second_half_img_choices_marked)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        # this function will add weights on the image which means take all the marks from pages to original image
        quest_img = utils.add_weight(quest_img, first_half_quest_img_c, start_of_loop, ans, ans_of_student,
                                     mapping_coord_1, coord_img_1)
        # cv.imshow('Image After Adding Weights of First Half', quest_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        quest_img = utils.add_weight(quest_img, second_half_quest_img_c, start_of_loop + questions_on_half_page,
                                     ans, ans_of_student, mapping_coord_2, coord_img_2)
        # cv.imshow('Image After Adding Weights of Second Half', quest_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        # resize the image and print the results on the question image and return the results to the user
        sol_img = utils.resize_img(sol_img)
        quest_img = utils.resize_img(quest_img)
        quest_img = utils.print_result(quest_img, percent)
        # cv.imshow('Solution Image', sol_img)
        # cv.imshow('Marked Question Image', quest_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        return sol_img, quest_img

    except:
        # print('Rectangle Contours can not be detected so move forward!'))
        return None, None
