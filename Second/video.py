import cv2

# Load the video file or initialize the video capture from a camera
video_path = "Second\Top 7 signs youre a Programmer.mp4"
cap = cv2.VideoCapture(video_path)

# Check if the video capture was successful
if not cap.isOpened():
    print("Error opening video file or camera.")
    exit()

# Read the first frame to get the video's dimensions
ret, frame = cap.read()
if not ret:
    print("Error reading the first frame.")
    exit()

# Define the amount of horizontal shift
shift_amount = 50

# Get the video's dimensions
height, width, _ = frame.shape

# Define the codec for the output video file
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_file = cv2.VideoWriter("output.mp4", fourcc, 30.0, (width, height))

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Break the loop if the video capture is complete
    if not ret:
        break

    # Shift the frame horizontally
    shifted_frame = frame[:, shift_amount:, :]

    # Display the shifted frame
    cv2.imshow("Shifted Frame", shifted_frame)

    # Write the shifted frame to the output file
    output_file.write(shifted_frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and output file
cap.release()
output_file.release()

# Close all OpenCV windows
cv2.destroyAllWindows()


#******************************************************************************************************************
# Other way of writing code :-
# import cv2
# import numpy as np

# def horizontal_shift(frame, shift_amount):
#     rows, cols = frame.shape[:2]
#     M = np.float32([[1, 0, shift_amount], [0, 1, 0]])
#     shifted_frame = cv2.warpAffine(frame, M, (cols, rows))
#     return shifted_frame

# video_path = "Second\Top 7 signs youre a Programmer.mp4"  # Replace with the actual path to your video file
# video_capture = cv2.VideoCapture(video_path)

# while True:
#     ret, frame = video_capture.read()

#     if not ret:
#         break

#     shifted_frame = horizontal_shift(frame, shift_amount=50)  # Adjust the shift amount as desired

#     cv2.imshow("Shifted Video", shifted_frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
#         break

# video_capture.release()
# cv2.destroyAllWindows()
