import numpy as np
import cv2
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.datasets import mnist
import time 
from led_cube import LedCube


# モデルのロード
model = load_model('model/mnist_relu_16x4.keras')

def map_to_int_range(arr):
    min_val = np.min(arr)
    max_val = np.max(arr)

    # 0-127にスケーリング
    mapped_arr = (arr - min_val) / (max_val - min_val) * 127
    mapped_arr = np.round(mapped_arr).astype(int)

    return mapped_arr



def test_model(input_data, output_mode:str = '0-127'):

    img = cv2.resize(input_data[0], (500, 500))
    cv2.imshow('input', img)

    if cv2.waitKey(33) & 0xFF:
        pass

    # y方向にappend
    reshaped_output = np.empty((4, 0, 4), dtype=np.float32) 

    # 各中間層の出力を取得して表示
    # 中間層は1-4
    for layer_index in range(1, 5):
        hidden_layer_model = Model(inputs=model.inputs, outputs=model.layers[layer_index].output)
        hidden_layer_output = hidden_layer_model.predict(input_data)

        # y方向にappend
        reshaped_output = np.append(reshaped_output, hidden_layer_output.reshape((4, 1, 4)), axis=1)
    
    
    flattened_output = reshaped_output.flatten()

    output_probability = model.predict(input_data)
    predicted_class = np.argmax(output_probability, axis=1)
    print(f'{predicted_class=}')

    # 発火判定
    if output_mode == '0-127':
        # 0-127にスケーリング
        int_output = map_to_int_range(flattened_output)

        print(int_output)

        return int_output
    
    elif output_mode == 'boolean':
        # 0かそれ以外
        binary_output = (flattened_output > 0).astype(int) * 127

        print(binary_output)
        
        return binary_output
    



if __name__ == "__main__":

    enable_serial = True
    is_input_random = True
    infinit_mode = False

    if enable_serial:
        led = LedCube('/dev/ttyUSB0')
    
    # MNISTデータセットのロード
    (_, _), (x_test, y_test) = mnist.load_data()
    x_test = x_test / 255.0

    if not is_input_random:
        target_digit = 9
        indices = np.where(y_test == target_digit)

        x_test = x_test[indices]
        y_test = y_test[indices]

    if enable_serial:
        led_density = []
        for x in range(128):
            led_density.append(0 if x%2==0 else 127)
        
        buff = ''.join(chr(density) for density in led_density)
        
        led.write(led_density)
        
    time.sleep(2)

    for index in range(100):
        data = test_model(x_test[index].reshape(1,28,28), '0-127')
        
        if enable_serial:
            led.write(data)
        
        time.sleep(0.5)
        
    while infinit_mode:
        for index in range(len(x_test)):
            data = test_model(x_test[index].reshape(1,28,28), '0-127')
            
            if enable_serial:
                led.write(data)
            
            time.sleep(0.5)

    if enable_serial:
        led.close()