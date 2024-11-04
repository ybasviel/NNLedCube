import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist

# MNISTデータセットのロード
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# 入力層
# 16ニューロン x 4層
# 出力層
model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(16, activation='relu'),  
    Dense(16, activation='relu'),
    Dense(16, activation='relu'),
    Dense(16, activation='relu'),
    Dense(10, activation='softmax')
])

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
model.compile(optimizer, loss_fn, metrics=["accuracy"])

# モデルの訓練
model.fit(x_train, y_train, epochs=200, batch_size=512, validation_data=[x_test, y_test])

# モデルの評価
loss, accuracy = model.evaluate(x_test, y_test)
print(f'Test accuracy: {accuracy}')
print(f'loss: {loss}')

# モデルの保存
model.save('model/mnist_relu_16x4.keras')