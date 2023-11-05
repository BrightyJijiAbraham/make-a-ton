import taipy
from taipy.gui import Gui
import random
from prediction import predict
from taipy.gui import Html
from webcam import Webcam
import cv2

user_hand_sign = None
opponent_hand_sign = None
user_score = 0
opponent_score = 0


def capture_webcam():
  """Captures a frame from the webcam.

  Returns:
    A numpy array representing the captured frame.
  """

  # Create a VideoCapture object
  cap = cv2.VideoCapture(0)

  # Check if the webcam is opened successfully
  if not cap.isOpened():
    raise Exception("Could not open webcam.")

  # Capture a frame from the webcam
  ret, frame = cap.read()

  # Check if the frame is empty
  if frame is None:
    raise Exception("Could not capture frame from webcam.")

  # Release the webcam
  cap.release()

  # Return the captured frame
  return frame

def predict_user_hand_sign():
    global user_hand_sign
    # Capture a frame from the webcam
    frame = capture_webcam()
    # Predict the user's hand sign
    user_hand_sign = predict(frame)

def generate_opponent_hand_sign():
    global opponent_hand_sign
    # Generate a random hand sign for the opponent
    opponent_hand_sign = random.choice(['paper', 'rock', 'scissor'])

def calculate_score():
    global user_hand_sign
    global opponent_hand_sign
    global user_score
    global opponent_score
    # Compare the user's hand sign to the opponent's hand sign and update the scores accordingly
    if user_hand_sign == 'paper' and opponent_hand_sign == 'rock':
        user_score += 1
    elif user_hand_sign == 'rock' and opponent_hand_sign == 'scissor':
        user_score += 1
    elif user_hand_sign == 'scissor' and opponent_hand_sign == 'paper':
        user_score += 1
    else:
        opponent_score += 1

def display_results():
    global user_hand_sign
    global opponent_hand_sign
    global user_score
    global opponent_score
    # Display the results
    print('User hand sign:', user_hand_sign)
    print('Opponent hand sign:', opponent_hand_sign)
    print('User score:', user_score)
    print('Opponent score:', opponent_score)

def play():
    # Predict the user's hand sign
    predict_user_hand_sign()
    # Generate a random hand sign for the opponent
    generate_opponent_hand_sign()
    # Calculate the score
    calculate_score()
    # Display the results
    display_results()

def play1(state):
    for i in range(4):
        play()

def reset():
    global user_hand_sign
    global opponent_hand_sign
    global user_score
    global opponent_score
    # Reset the game
    user_hand_sign = None
    opponent_hand_sign = None
    user_score = 0
    opponent_score = 0


html_page = """
    <div|div box|part|

    <|play a game|button btn-success|on_action=play1|>
    
    |div>

    <|{user_hand_sign}| p|>
    <|{opponent_hand_sign}| p|>
    <|{user_score}| p|>
    <|{opponent_score}| p|>

    
"""

passed = Html("""<script>
     if ({user_score} &gt;= {opponent_score}) {
         window.location.href = "sucess";
     } else {
         window.location.href = "fail";
     }
     </script>""")



if __name__ == "__main__":

    pages = {
        "/": html_page,
        "sucess": passed
    }
    
    gui = Gui(pages=pages)
    gui.run(port=9090)
