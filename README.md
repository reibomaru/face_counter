## 開発環境
Python 3.5.2  
Anaconda 4.1.1  
Django 2.2.5  
OpenCV 4.1.1  

## Overview
カメラの前に顔があるとカウントをするアプリを作りました。

## Description
顔の検知にはOpenCV([公式ドキュメント](https://docs.opencv.org/4.1.1/index.html))を使いました。
アプリケーションのベースにはDjangoを用い、カウントしたデータはJSON形式に変換しJavaScriptファイルで読み込み動的に画面を変化させています。

## Demo
macのカメラの前に顔があるとカウントが増える（来客件数が増える）
![hoge](https://raw.github.com/wiki/reibomaru/face_counter/images/face_counter.gif))

## Requirement
OpenCVとNumpyをpipインストールする必要があります。

## Usage
アプリを使用するためにはmysite/staticフォルダにface_count.jsonファイルを作成する必要がありますので注意してください。

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[reibomaru](https://github.com/reibomaru)