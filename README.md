# NeuralNetwork LedCube

## 概要
NeuralNetworkの中間層の出力をLEDの発光で可視化したオモチャ

- nn: mnistを例にモデルを作成し、推論時にarduinoへ中間層の出力を渡す
- arduino: 受け取ったデータにしたがってLEDを光らせるだけ

## Software

```shell
python train.py
python test.py
```

## Hardware

- シフトレジスタ(74HC595)x2で8x8=4x4x4=64のLEDを制御
- 回路を組む都合でLEDの配線と座標系がぐちゃぐちゃになってしまったので無理やり補正した
    ```cpp
    uint8_t getLayerBitDensity(uint8_t data[64], uint8_t index, uint8_t density){
        switch(index){
            case 0:
                return ((data[63]>density)<<7 | (data[62]>density)<<6 | (data[59]>density)<<5 | (data[58]>density)<<4 | (data[55]>density)<<3 | (data[54]>density)<<2 | (data[50]>density)<<1 | (data[51]>density));
            case 1:
                return ((data[47]>density)<<7 | (data[46]>density)<<6 | (data[43]>density)<<5 | (data[42]>density)<<4 | (data[39]>density)<<3 | (data[38]>density)<<2 | (data[34]>density)<<1 | (data[35]>density));
            case 2:
                return ((data[31]>density)<<7 | (data[30]>density)<<6 | (data[27]>density)<<5 | (data[26]>density)<<4 | (data[23]>density)<<3 | (data[22]>density)<<2 | (data[18]>density)<<1 | (data[19]>density));
    ....
    ```

## 参考
- [@gen10nal(タクリュー) Kerasでの中間層出力の取得について #DeepLearning - Qiita](https://qiita.com/gen10nal/items/66de8bd9bdf55405083d)
- [4x4x4 LED Cube (Arduino Uno) : 7 Steps (with Pictures) - Instructables](https://www.instructables.com/4x4x4-LED-Cube-Arduino-Uno/)