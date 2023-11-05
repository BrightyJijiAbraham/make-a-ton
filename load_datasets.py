import tensorflow as tf

def load_preprocess(direct, train, test, validation):

    # Define a data generator for training data
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0/255.0,  # Rescale pixel values to the range [0, 1]
        rotation_range=20,  # Randomly rotate images by up to 20 degrees
        width_shift_range=0.2,  # Randomly shift the width of images
        height_shift_range=0.2,  # Randomly shift the height of images
        shear_range=0.2,  # Apply random shear transformations
        zoom_range=0.2,  # Apply random zoom transformations
        horizontal_flip=True,  # Randomly flip images horizontally
        fill_mode='nearest'  # Strategy to fill in newly created pixels
    )

    # Load the training data from the directory and preprocess it
    train_generator = train_datagen.flow_from_directory( 
        direct + '/' + train ,
        target_size=(150, 150),  # Resize images to a specific size
        batch_size=32,  # Set the batch size
        class_mode='categorical'  # Define the class mode (e.g., categorical for multi-class)
    )

    # Load the training data from the directory and preprocess it
    test_generator = train_datagen.flow_from_directory(
        direct + '/' + test ,
        target_size=(150, 150),  # Resize images to a specific size
        batch_size=32,  # Set the batch size
        class_mode='categorical'  # Define the class mode (e.g., categorical for multi-class)
    )

    # Load the training data from the directory and preprocess it
    validation_generator = train_datagen.flow_from_directory(
        direct + '/' + validation ,
        target_size=(150, 150),  # Resize images to a specific size
        batch_size=32,  # Set the batch size
        class_mode='categorical'  # Define the class mode (e.g., categorical for multi-class)
    )

    return train_generator, validation_generator, test_generator