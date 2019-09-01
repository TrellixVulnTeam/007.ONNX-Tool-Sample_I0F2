#! -*- coding: utf-8 -*-

"""
  [main]
    python main.py --help
"""

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse
import tensorflow as tf
import urllib.request
import tarfile
import tf2onnx

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------

#---------------------------------
# クラス
#---------------------------------

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	# --- local functions ---
	"""
	  関数名: _arg_parser
	  説明：引数を解析して値を取得する
	"""
	def _arg_parser():
		parser = argparse.ArgumentParser(description='Mobile Net v1モデルをダウンロードしてONNX変換するツール', formatter_class=argparse.RawTextHelpFormatter)

		# --- 引数を追加 ---
		parser.add_argument('--save_dir', dest='save_dir', type=str, default=None, help='モデル保存先のディレクトリ', required=True)

		args = parser.parse_args()

		return args

	# --- 引数処理 ---
	args = _arg_parser()

	# --- TensorFlow ---
	print('[INFO] TensorFlow mobilenet_v1_1.0_224 downloading ...')
	save_dir = os.path.join(args.save_dir, 'mobilenet_v1_1.0_224')
	save_file = os.path.join(save_dir, 'mobilenet_v1_1.0_224.tgz')
	os.makedirs(save_dir, exist_ok=True)
	url = 'http://download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_1.0_224.tgz'
	urllib.request.urlretrieve(url, '{}'.format(save_file))

	print('[INFO] DONE')
	print('[INFO] TensorFlow mobilenet_v1_1.0_224 extracting ...')
	with tarfile.open(save_file, 'r:gz') as f:
		f.extractall(path=save_dir)
	print('[INFO] DONE')

	print('[INFO] TensorFlow mobilenet_v1_1.0_224 frozen to ONNX ...')
	with tf.Graph().as_default():
		with open(os.path.join(save_dir, 'mobilenet_v1_1.0_224_frozen.pb'), 'rb') as f:
			graph_def = tf.GraphDef()
			graph_def.ParseFromString(f.read())
			tf.import_graph_def(graph_def, name='')
		onnx_graph = tf2onnx.tfonnx.process_tf_graph(tf.get_default_graph(), \
			input_names=['input:0'], \
			output_names=['MobilenetV1/Predictions/Reshape_1:0'])
		model_proto = onnx_graph.make_model('test')
	onnx_dir = os.path.join(save_dir, 'onnx_model')
	os.makedirs(onnx_dir, exist_ok=True)
	with open(os.path.join(onnx_dir, 'model.onnx'), 'wb') as f:
		f.write(model_proto.SerializeToString())
	print('[INFO] DONE')

