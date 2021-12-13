# Import selenium and time modules 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import time
import sys

# Global Variables

# PATH for the chrome webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Tuple of valid booking times
VALID_TIMES = ("06:00",
"07:00",
"08:15",
"09:30",
"10:45",
"12:00",
"13:15",
"14:30",
"15:45",
"17:00",
"18:15",
"19:30",
"20:45")


# Class representing a person booking a gym slot
class GymBooker():

    def __init__(self, student_num, booking_time):
        self.__student_num = student_num
        self.__booking_time = booking_time
        self.__booking_site = "https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK"
        self.__driver = webdriver.Chrome(PATH)


    def __sleep(self, len=3):
        """Method for sleeping while page elements load"""
        # Sleep while page elements load
        time.sleep(len)


    def load_booking_site(self):
        """Method for launching the gym booking website"""
        # Launch gym booking website
        self.__driver.get(self.__booking_site)
        self.__sleep()


    def find_a_slot(self):
        """Method for finding an available booking slot"""

        # Counter for keeping track of attempts
        attempts = 0

        # Infinite while loop which will continue trying to book until a booking link appears
        while True:
            attempts += 1

            try: 
                # xpath used to isolate the booking link
                xpath = f"//tr/td/table/tbody/tr[./td[text()=\"{self.__booking_time}\"]][1]/td[6]/a"

                # Click booking link and exit while loop
                booking_link = self.__driver.find_element_by_xpath(xpath)
                booking_link.click()
                break

            except NoSuchElementException:
                # Refresh the page if the booking link isn't up yet and try again
                print(f"Booking link is not available yet. Will try again in 10 seconds. Attempt: {attempts}")
                if attempts > 10:
                    print("Giving up...")
                    self.quit()
                
                self.__driver.refresh()
                self.__sleep(10)

            except ElementNotInteractableException:
                # If this exception is triggered, this implies that the bookings are full, so the program prompts the user for another booking time
                print("Booking Full. No more slots available")
                self.__booking_time = get_booking_time()

        self.__sleep()


    def accept_cookies(self):
        """Method for accepting cookies on the gym booking site"""
        # Accept cookies
        cookie = self.__driver.find_element_by_id("onetrust-accept-btn-handler")
        cookie.send_keys(Keys.RETURN)
        self.__sleep()


    def enter_student_number(self):
        """Method for entering your student number into the booking system"""
        attempts = 0

        while True:
            attempts += 1
            
            # Enter student number
            student_num_input = self.__driver.find_element_by_name("MEMBER_NO")
            student_num_input.send_keys(self.__student_num)
            student_num_input.send_keys(Keys.RETURN)
            self.__sleep()

            try:
                # Check if an error text appears, implying that the user did not input a valid student number
                error_text = self.__driver.find_element_by_class_name("errortext")

                # Get a new student number if the error text appears
                if error_text:
                    print("Invalid Student Number. Attempts: {attempts}")

                    if attempts > 10:
                        print("Giving Up...")
                        self.quit()

                    self.__student_num = get_student_num()

            except NoSuchElementException:
                # If this exception is raised, this implies that the student number was valid, so the program can continue
                print("Student number entry successful")
                break


    def confirm_booking(self):
        """Method for confirming the booking"""
        # Confirm booking
        confirm_booking = self.__driver.find_element_by_class_name("menubutton")
        confirm_booking.send_keys(Keys.RETURN)
        self.__sleep()


    def quit(self):
        """Method for quitting the driver and exiting the program
        
        The program will be exited if either the booking was successful, or there were no available slots
        """
        self.__driver.quit()
        sys.exit()
        

# Functions for obtaining the required arguments for the GymBooker class

def get_student_num():
    """Function requests user for a valid student number and returns the output
    
    Valid in this context means that the student number is an integer
    """
    attempts = 0

    while True:
        attempts += 1

        try:
            # Prompt the user for a student number
            student_num = input("Please enter your student number: ")

            # Try convert the student number to an integer to see if it is valid
            print(int(student_num))


        except ValueError:
            # If this exception is raised, the user will be prompted for another student number
            print(f"Invalid Student Number. Attempts: {attempts}")

            # The system eventually gives up if the user does not submit a valid student number
            if attempts > 10:
                print("Giving up...")
                sys.exit()

            continue

        break

    return student_num


def show_booking_times():
    # Show the user a list of valid booking times
    print("Valid Booking Times:")
    for time in VALID_TIMES:
        print(time, end=" ")
    
    print("\n")


def get_booking_time():
    # Prompt the user for a booking time    
    booking_time = input("When would you like to book a slot: ")

    while booking_time not in VALID_TIMES:
        print("Error: Invalid time")
        show_booking_times()
        booking_time = input("When would you like to book a slot: ")

    return booking_time


if __name__ == "__main__":
    # Get the student number and desired booking time for the GymBooker class
    student_num = get_student_num()
    show_booking_times()
    booking_time = get_booking_time()
        
    # Create a gym booker class instance
    new_booker = GymBooker(student_num, booking_time)
    new_booker.load_booking_site()
    new_booker.find_a_slot()
    new_booker.accept_cookies()
    new_booker.enter_student_number()
    new_booker.confirm_booking()
    new_booker.quit()