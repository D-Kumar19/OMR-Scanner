import dir_or_camera as read_data


# To enter the Solution Images use this Location: Images/sol_img_x.PNG (x is the number of the image: 1, 2, 3)
# To enter the Question Images use this Location: Images/quest_img_y.PNG (x is the number of the image: 1, 2, 3, 4)

# this function will just get input from user if he/she is interested
# to use the webcam or already has stored images in dir to check
print('Hello, Welcome to this OMR Scanner Program. Happy Exams!')

while True:
    print('\nPress ''1'' if you have Scanned Images in your PC!')
    print('Press ''2'' if you have want to Scan Images using your Camera!')
    choice = input('Enter your Choice: ')

    if choice == '1' or choice == '2':
        break
    else:
        print('Invalid Choice. Please Enter again!')

if choice == '1':
    # read from directory
    read_data.from_dir()
elif choice == '2':
    # open camera to read
    read_data.from_camera()
