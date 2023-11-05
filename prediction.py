def predict(frame):

    import cv2
    import numpy as np
    from keras.models import load_model
    from keras.preprocessing import image

    # Load the pre-trained model
    model = load_model('model.h5')

    # Define the labels
    labels = ['paper', 'rock', 'scissor']

    label = None
    
    img = cv2.resize(frame, (150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    # Make prediction
    prediction = model.predict(img_tensor)[0]
    print(prediction)
    index = np.argmax(prediction)
    label = labels[index]

    return label