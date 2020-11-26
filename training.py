import dlib

#学習用のオプション変数の生成.
options = dlib.simple_object_detector_training_options()

#認識はSVMアルゴリズムを使っている。それのコストパラメータを設定.
options.C = 3

#学習処理を行うときの実行スレッドの数.
options.num_threads = 8

#左右反転のイメージは生成しない（鯉が一方向に進むだけなので）
options.add_left_right_image_flips = False

#学習処理の経過を出力する（ターミナルで確認可能）
options.be_verbose = True

#矩形のXMLデータから学習データを作成.
dlib.train_simple_object_detector("do_not_park_and_stop/traning.xml", "detector_do_not_park_and_stop.svm", options)

#学習データから認識オブジェクトの作成.
detector = dlib.simple_object_detector("detector_do_not_park_and_stop.svm")