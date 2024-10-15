import cv2 as cv
import mediapipe as mp
import pyautogui
import math

# Initialize the MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Allow up to two hands


# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


# Function to start finger control
def start_finger_control():
    cam = cv.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2)  # Allow up to two hands
    screen_w, screen_h = pyautogui.size()
    sensitivity = 1

    # def calculate_distance(point1, point2):
    #     return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    prev_x, prev_y = 0, 0
    alpha = 1

    while True:
        _, frame = cam.read()
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        output = hands.process(rgb_frame)
        hand_landmarks = output.multi_hand_landmarks
        frame_h, frame_w, _ = frame.shape
        screen_middle = frame_w // 2  # Screen division at the middle

        if hand_landmarks:
            for hand in hand_landmarks:
                # Get the x-coordinate of the wrist (landmark 0) to check which side of the screen the hand is on
                wrist_x = hand.landmark[0].x * frame_w

                # Right side of the screen: hand controls mouse movement
                if wrist_x > screen_middle:
                    index_finger_tip = hand.landmark[8]  # Index finger tip
                    x = int(index_finger_tip.x * frame_w)
                    y = int(index_finger_tip.y * frame_h)

                    smooth_x = int(alpha * x + (1 - alpha) * prev_x)
                    smooth_y = int(alpha * y + (1 - alpha) * prev_y)

                    prev_x, prev_y = smooth_x, smooth_y

                    screen_x = int(smooth_x * screen_w // frame_w * sensitivity)
                    screen_y = int(smooth_y * screen_h // frame_h * sensitivity)
                    pyautogui.moveTo(screen_x, screen_y)

                    cv.circle(frame, (smooth_x, smooth_y), 5, (0, 255, 0), cv.FILLED)  # Visual feedback

                # Left side of the screen: hand controls clicking
                else:
                    thumb_tip = hand.landmark[4]
                    middle_tip = hand.landmark[12]
                    third_tip = hand.landmark[16]

                    # Calculate distances for clicking gestures
                    distance_thumb_middle = calculate_distance(thumb_tip, middle_tip)
                    distance_thumb_third = calculate_distance(thumb_tip, third_tip)

                    # Draw circles on the left hand's fingers for visual feedback
                    thumb_tip_x, thumb_tip_y = int(thumb_tip.x * frame_w), int(thumb_tip.y * frame_h)
                    middle_tip_x, middle_tip_y = int(middle_tip.x * frame_w), int(middle_tip.y * frame_h)
                    third_tip_x, third_tip_y = int(third_tip.x * frame_w), int(third_tip.y * frame_h)

                    cv.circle(frame, (thumb_tip_x, thumb_tip_y), 5, (255, 255, 0), cv.FILLED)
                    cv.circle(frame, (middle_tip_x, middle_tip_y), 5, (255, 255, 0), cv.FILLED)
                    cv.circle(frame, (third_tip_x, third_tip_y), 5, (255, 255, 255), cv.FILLED)

                    # Clicking logic for the left-hand side
                    if distance_thumb_third < 0.05:
                        pyautogui.doubleClick()  # Double click gesture
                    elif distance_thumb_middle < 0.05:
                        pyautogui.click()  # Single click gesture

        cv.imshow('Hand control mouse', frame)
        cv.waitKey(1)




    # cam = cv.VideoCapture(0)  # Start video capture
    # screen_w, screen_h = pyautogui.size()
    # prev_x, prev_y = 0, 0
    # alpha = 1  # Smoothing factor
    # sensitivity = 1
    #
    # while True:
    #     _, frame = cam.read()
    #     frame = cv.flip(frame, 1)
    #     rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    #     output = hands.process(rgb_frame)
    #     hand_landmarks = output.multi_hand_landmarks
    #     frame_h, frame_w, _ = frame.shape
    #
    #     if hand_landmarks:
    #         # Always assign the first hand for mouse movement
    #         hand_1 = hand_landmarks[0]
    #
    #         # Hand 1 for mouse movement (index finger)
    #         index_finger_tip = hand_1.landmark[8]
    #         x = int(index_finger_tip.x * frame_w)
    #         y = int(index_finger_tip.y * frame_h)
    #
    #         smooth_x = int(alpha * x + (1 - alpha) * prev_x)
    #         smooth_y = int(alpha * y + (1 - alpha) * prev_y)
    #
    #         prev_x, prev_y = smooth_x, smooth_y
    #
    #         screen_x = int(smooth_x * screen_w // frame_w * sensitivity)
    #         screen_y = int(smooth_y * screen_h // frame_h * sensitivity)
    #         pyautogui.moveTo(screen_x, screen_y)
    #
    #         cv.circle(frame, (smooth_x, smooth_y), 5, (0, 255, 0), cv.FILLED)
    #
    #         # If there are two hands, the second hand will handle clicking
    #         if len(hand_landmarks) == 2:
    #             hand_2 = hand_landmarks[1]
    #
    #             # Hand 2 for clicking (thumb and middle fingers)
    #             thumb_tip = hand_2.landmark[4]
    #             middle_tip = hand_2.landmark[12]
    #             third_tip = hand_2.landmark[16]
    #
    #             # Calculate distances for clicking gestures
    #             distance_thumb_middle = calculate_distance(thumb_tip, middle_tip)
    #             distance_thumb_third = calculate_distance(thumb_tip, third_tip)
    #
    #             # Draw circles on the second hand's fingers
    #             thumb_tip_x, thumb_tip_y = int(thumb_tip.x * frame_w), int(thumb_tip.y * frame_h)
    #             middle_tip_x, middle_tip_y = int(middle_tip.x * frame_w), int(middle_tip.y * frame_h)
    #             third_tip_x, third_tip_y = int(third_tip.x * frame_w), int(third_tip.y * frame_h)
    #
    #             cv.circle(frame, (thumb_tip_x, thumb_tip_y), 5, (255, 255, 0), cv.FILLED)
    #             cv.circle(frame, (middle_tip_x, middle_tip_y), 5, (255, 255, 0), cv.FILLED)
    #             cv.circle(frame, (third_tip_x, third_tip_y), 5, (255, 255, 255), cv.FILLED)
    #
    #             # Clicking logic for the second hand
    #             if distance_thumb_third < 0.05:
    #                 pyautogui.doubleClick()  # Double click gesture
    #             elif distance_thumb_middle < 0.05:
    #                 pyautogui.click()  # Single click gesture
    #
    #     cv.imshow('Hand control mouse', frame)
    #     cv.waitKey(1)
    # while True:
    #     _, frame = cam.read()
    #     frame = cv.flip(frame, 1)  # Flip the frame horizontally
    #     rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    #     output = hands.process(rgb_frame)
    #     hand_landmarks = output.multi_hand_landmarks
    #     frame_h, frame_w, _ = frame.shape
    #
    #     if hand_landmarks:
    #         # Always assign the first hand for mouse movement
    #         hand_1 = hand_landmarks[0]
    #
    #         # Hand 1 for mouse movement (index finger)
    #         index_finger_tip = hand_1.landmark[8]
    #         x = int(index_finger_tip.x * frame_w)
    #         y = int(index_finger_tip.y * frame_h)
    #
    #         # Smooth mouse movement
    #         smooth_x = int(alpha * x + (1 - alpha) * prev_x)
    #         smooth_y = int(alpha * y + (1 - alpha) * prev_y)
    #         prev_x, prev_y = smooth_x, smooth_y

            # Move the mouse
    #         screen_x = int(smooth_x * screen_w // frame_w)
    #         screen_y = int(smooth_y * screen_h // frame_h)
    #         pyautogui.moveTo(screen_x, screen_y)
    #
    #         cv.circle(frame, (smooth_x, smooth_y), 5, (0, 255, 0), cv.FILLED)
    #
    #         # If there are two hands, the second hand will handle clicking
    #         if len(hand_landmarks) == 2:
    #             hand_2 = hand_landmarks[1]
    #
    #             # Hand 2 for clicking (thumb and middle fingers)
    #             thumb_tip = hand_2.landmark[4]
    #             middle_tip = hand_2.landmark[12]
    #             third_tip = hand_2.landmark[16]
    #
    #             # Calculate distances for clicking gestures
    #             distance_thumb_middle = calculate_distance(thumb_tip, middle_tip)
    #             distance_thumb_third = calculate_distance(thumb_tip, third_tip)
    #
    #             # Clicking logic for the second hand
    #             if distance_thumb_third < 0.05:  # Double click gesture
    #                 pyautogui.doubleClick()
    #             elif distance_thumb_middle < 0.05:  # Single click gesture
    #                 pyautogui.click()
    #
    #     cv.imshow('Hand control mouse', frame)
    #
    #     # Exit if 'q' key is pressed
    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # cam.release()  # Release the camera
    # cv.destroyAllWindows()  # Close all OpenCV windows
    #

# Function to stop finger control (if needed)
def stop_finger_control():
    # Currently, this function does nothing since stopping is handled in the main loop.
    # If you want to implement additional cleanup or state management, do it here.
    pass


# Example of starting the finger control
if __name__ == "__main__":
    start_finger_control()
