from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def create_model(model_number):
    """Returns a model based on the model number."""
    
    if model_number == 1:
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(4, activation='softmax')
        ])
    elif model_number == 2:
        model = Sequential([
            Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(4, activation='softmax')
        ])
    elif model_number == 3:
        model = Sequential([
            Conv2D(32, (5, 5), activation='relu', input_shape=(100, 100, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (5, 5), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(4, activation='softmax')
        ])
    else:
        raise ValueError("Invalid model number. Choose 1, 2, or 3.")
    
    return model


""" def create_model(input_shape=(100, 100, 3), num_classes=4):
    inputs = Input(shape=input_shape)

    # First branch
    branch_1 = Conv2D(32, (3, 3), activation="relu", padding="same")(inputs)
    branch_1 = MaxPooling2D(pool_size=(2, 2))(branch_1)
    branch_1 = Conv2D(64, (3, 3), activation='relu', padding='same')(branch_1)
    branch_1 = MaxPooling2D(pool_size=(2, 2))(branch_1)
    branch_1 = Conv2D(128, (3, 3), activation='relu', padding='same')(branch_1)
    branch_1 = MaxPooling2D(pool_size=(2, 2))(branch_1)
    branch_1 = Conv2D(256, (3, 3), activation='relu', padding='same')(branch_1)
    branch_1 = MaxPooling2D(pool_size=(2, 2))(branch_1)
    branch_1 = Conv2D(512, (3, 3), activation='relu', padding='same')(branch_1)
    branch_1 = MaxPooling2D(pool_size=(2, 2))(branch_1)
    branch_1 = Flatten()(branch_1)
    branch_1 = Dropout(0.5)(branch_1)

    # Second branch
    branch_2 = Conv2D(128, (5, 5), activation='relu', padding='same')(inputs)
    branch_2 = MaxPooling2D(pool_size=(3, 3))(branch_2)
    branch_2 = Conv2D(256, (5, 5), activation='relu', padding='same')(branch_2)
    branch_2 = MaxPooling2D(pool_size=(3, 3))(branch_2)
    branch_2 = Conv2D(512, (5, 5), activation='relu', padding='same')(branch_2)
    branch_2 = MaxPooling2D(pool_size=(3, 3))(branch_2)
    branch_2 = Flatten()(branch_2)
    branch_2 = Dropout(0.5)(branch_2)

    # Third branch
    branch_3 = Conv2D(128, (7, 7), activation='relu', padding='same')(inputs)
    branch_3 = MaxPooling2D(pool_size=(5, 5))(branch_3)
    branch_3 = Conv2D(256, (7, 7), activation='relu', padding='same')(branch_3)
    branch_3 = MaxPooling2D(pool_size=(5, 5))(branch_3)
    branch_3 = Flatten()(branch_3)
    branch_3 = Dropout(0.5)(branch_3)

    # Merge branches
    merged = Concatenate()([branch_1, branch_2, branch_3])

    # Dense layers
    dense_1 = Dense(256, activation='relu')(merged)
    dense_1 = Dropout(0.5)(dense_1)
    dense_2 = Dense(128, activation='relu')(dense_1)
    dense_2 = Dropout(0.5)(dense_2)

    # Output layer
    output = Dense(num_classes, activation='softmax')(dense_2)

    # Define the model
    model = Model(inputs=inputs, outputs=output)

    # Compile the model
    model.compile(optimizer=Adam(), loss=SparseCategoricalCrossentropy(), metrics=['accuracy'])



    return model """