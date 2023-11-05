
from flask import Flask, render_template, jsonify, request
import random
from prediction import predict
import cv2
import time
from keras.preprocessing.image import load_img
import secrets
import hashlib


user_hand_sign = None
opponent_hand_sign = None
user_score = 0
opponent_score = 0
i = 4
arg = []
result = []

def generate_choice():
    choices = ['paper', 'rock', 'scissor']
    return secrets.choice(choices)

def generate_game_hash(player_choice, opponent_choice, result):
    # Calculate a hash of the game data
    game_data = f"{player_choice}{opponent_choice}{result}"
    game_hash = hashlib.sha256(game_data.encode()).hexdigest()
    return game_hash


def capture_webcam():

  # Create a VideoCapture object
  time.sleep(5)
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

def predict_user_hand_sign(file = None):
    global user_hand_sign
    if file == None:
        # Capture a frame from the webcam
        frame = capture_webcam()
        # Predict the user's hand sign
        user_hand_sign = predict(frame)
    else:
        # Predict the user's hand sign
        user_hand_sign = predict(file)

def generate_opponent_hand_sign():
    global opponent_hand_sign
    # Generate a random hand sign for the opponent
    opponent_hand_sign =  generate_choice()

def calculate_score():
    global user_hand_sign
    global opponent_hand_sign
    global user_score
    global opponent_score
    global result
    # Compare the user's hand sign to the opponent's hand sign and update the scores accordingly
    if user_hand_sign == 'paper' and opponent_hand_sign == 'rock':
        user_score += 1
    elif user_hand_sign == 'rock' and opponent_hand_sign == 'scissor':
        user_score += 1
    elif user_hand_sign == 'scissor' and opponent_hand_sign == 'paper':
        user_score += 1
    elif user_hand_sign == opponent_hand_sign:
        user_score = user_score
        opponent_score = opponent_score
    else:
        opponent_score += 1

    result = [user_score,opponent_score]

def verify_result(player_choice, opponent_choice, result, game_hash):
    # Calculate a hash of the game data
    game_data = f"{player_choice}{opponent_choice}{result}"
    computed_hash = hashlib.sha256(game_data.encode()).hexdigest()

    # Compare the computed hash to the received game hash
    if computed_hash == game_hash:
        return "Result is valid"
    else:
        return "Result has been tampered with"

def display_results():
    global user_hand_sign
    global opponent_hand_sign
    global user_score
    global opponent_score
    global arg
    # Display the results
    print('User hand sign:', user_hand_sign)
    print('Opponent hand sign:', opponent_hand_sign)
    print('User score:', user_score)
    print('Opponent score:', opponent_score)

def play(file=None):
    global user_hand_sign
    global opponent_hand_sign
    global user_score
    global opponent_score
    global arg
    global i

    if file is None:
        # Predict the user's hand sign
        predict_user_hand_sign()
        # Generate a random hand sign for the opponent
        generate_opponent_hand_sign()
        # Calculate the score
        calculate_score()
        # Generate the game hash
        game_hash = generate_game_hash(user_hand_sign, opponent_hand_sign, result)  # You can replace "Result" with the actual result
        # Display the results
        display_results()
    else:
        predict_user_hand_sign(file)
        # Generate a random hand sign for the opponent
        generate_opponent_hand_sign()
        # Calculate the score
        calculate_score()
        # Generate the game hash
        game_hash = generate_game_hash(user_hand_sign, opponent_hand_sign, result)  # You can replace "Result" with the actual result
        # Display the results
        display_results()

    i -= 1
    arg = [user_hand_sign, opponent_hand_sign, user_score, opponent_score, i, game_hash, result]

def reset():
    global user_hand_sign
    global opponent_hand_sign
    global user_score
    global opponent_score
    global i
    global arg
    global result
    # Reset the game
    user_hand_sign = None
    opponent_hand_sign = None
    user_score = 0
    opponent_score = 0
    i = 4
    arg = []
    result = []

app = Flask(__name__)

@app.route('/')
def index():
    global i
    return render_template('index.html', i=i)

@app.route('/play')
def p():
    global user_score
    global opponent_score
    global i 
    play()

    if i != 0:
        return render_template("index.html", arg=arg)
    if (user_score >= opponent_score or user_score >= 2):
        reset()
        return render_template('success.html')
    else:
        reset()
        return render_template('fail.html')
    
@app.route('/api', methods=['POST'])
def api():
    global user_score
    global opponent_score
    global i 
    global arg
    global result

    imagefile = request.files['imagefile']
    classification = ['','']
    classification[0]= "images/"+ imagefile.filename
    image_path = "./static/images/" + imagefile.filename
    imagefile.save(image_path)

    image1 = load_img(image_path, target_size=(224, 224))##loading the image
    
    play(image1)

    if i != 0:
        player_choice = user_hand_sign
        opponent_choice = opponent_hand_sign
        result = [user_score,opponent_score] # You should replace this with the actual game result
        received_hash = arg[-1]  # Get the received game hash from the last element of the 'arg' list

        verification_result = verify_result(player_choice, opponent_choice, result, received_hash)

        if verification_result == "Result is valid":
            return jsonify("Result is valid")
        else:
            return jsonify("Result has been tampered with",arg)
    if user_score >= opponent_score or user_score >= 2:
        reset()
        return jsonify("success")
    else:
        reset()
        return jsonify("fail")



if __name__ == '__main__':
    app.run(debug=True , host = '192.168.6.189')
