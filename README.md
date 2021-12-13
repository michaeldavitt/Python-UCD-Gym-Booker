# Python-UCD-Gym-Booker

Credit to Clarence White for the original concept (https://github.com/ClarenceWhite/Gym-Booking)


## Important
This program was operational on the 13th December 2021. It is possible that UCD's gym booking site has been updated at this point, which may cause unexpected errors in the program.


## Description
This program prompts the user for their student number and the time that they wish to book a gym slot for. The program validates that the booking time they provided is valid. Once this check has been completed, the program launches the gym booking website. The program then attempts to find a booking link corresponding to the user's requested time slot. There are two potential errors that can occur here. The first is the situation where the gym booking link has not been uploaded yet. In this situation, the program waits for a minute, then once a minute has passed it tries again. This process is repeated until the booking link is available. The program will give up after 10 attempts and will quit to prevent the while loop from running indefinately. The second error arises when the booking slots have all been filled. In this situation, the link will become unclickable, in which case the program will inform the user that there are no available slots for their selected booking time and will request that the user submits a new time.

If the booking link has been sucessfully clicked, we are taken to the page where users are required to submit their student number. The program types the student number provided by the student into the input field on the page. It is possible that the user provided an invalid student number, in which case, an error message will be generated on the page. The program looks for this error message and if it is found, prompts the user to re-enter their student number. This will be forced to continue re-entering their student number until they provide one that is valid. Once a valid student number has been provided, the program hits the confirmation button and quits.