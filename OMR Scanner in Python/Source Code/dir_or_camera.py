import utils
import cv2 as cv
import question_image_reader as quest_img_reader


#################################################################
web_cam_reader = True
camera_no = 0

prompt_for_quest_img = '\nEnter the Location of the Question Image: '

#################################################################


# this function will check the images if they are stored in dir
def from_dir():
    # this function will get the solution image and the answers keys
    sol_img, ans = utils.get_sol_img()
    # print(ans)
    # cv.imshow('Solution Image', sol_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # this function will get the question image
    quest_img = utils.get_file(prompt_for_quest_img)
    # cv.imshow('Question Image', quest_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # this function will get us the results comparing the answer sheet and the question paper
    sol_img, result_img = quest_img_reader.get_the_results(sol_img, ans, quest_img)
    utils.show_the_results(sol_img, result_img)

    # this function will generate the timestamp and then saving the file with timestamp
    utils.save_results(result_img)

    while True:
        # this function will check if we have more question images to check for the same solution images or not
        continue_or_not, quest_img = utils.read_another_quest_img()
        # print(continue_or_not, quest_img_loc)

        if continue_or_not:
            # doing the process again which is checking the image and saving the results
            sol_img, result_img = quest_img_reader.get_the_results(sol_img, ans, quest_img)
            utils.show_the_results(sol_img, result_img)

            # this function will generate the timestamp and then saving the file with timestamp
            utils.save_results(result_img)
        else:
            print('Thanks for using this Algorithm. Have a great day!')
            break


# this function will check the images if we have to read them from camera
def from_camera():
    print('Press Esc to close the Camera!')
    print("Press 'S' to Save the Image!")

    # this function will get the solution image and the answers keys
    sol_img, ans = utils.get_sol_img()

    cap = cv.VideoCapture(camera_no)
    cap.set(10, 160)

    while True:
        success, quest_img = cap.read()

        # if we can't find camera or not able to open it then end program
        if not success:
            print("Camera failed to grab the Frame")
            break

        # this function will get us the results comparing the answer sheet and the question paper
        sol_img, result_img = quest_img_reader.get_the_results(sol_img, ans, quest_img)
        cv.imshow('Camera Input', quest_img)
        utils.show_the_results(sol_img, result_img)

        # if we press esc key camera will close
        key = cv.waitKey(1)
        if key % 256 == 27:
            print("Escape Key hit closing the Camera!")
            break

        # if we press the 's' key it will store the image
        elif cv.waitKey(1) & 0xFF == ord('s'):
            print('S Key was pressed to save the Results!')

            if result_img is None:
                print('Can not save the Results as image is Empty!')
            else:
                utils.save_results(result_img)

        cv.waitKey(300)
