# 安田さんのTTSモデルの利用方法

**導入**  
導入時に以下のコマンドで各種ライブラリを導入する。
- pip install style-bert-vits2  
- pip install soundfile  
- pip install playsound  

また、PyTorchを導入するときは、実行環境によってコマンドが異なる。
そのため、以下URLを参照し、自身の環境にあったものを選択して「Run this Command」をコピーし、ターミナル上でペーストする。
- https://pytorch.org/get-started/locally/  
  
**必要ファイルのダウンロード**  
「model_assets/yasuda」ディレクトリ上に  
- config.json  
- style_vectors.npy  
があることを確認する。  
以下URLより「yasuda_e100_s3462.safetensors」ファイルをダウンロードし、同ディレクトリ上に配置を行う。  
- https://drive.google.com/file/d/1aYRf36GNbVgU7Iw9vFcwE86wqgnqXodC/view?usp=sharing  

その後、tts_main.pyをimportして、main関数に読み上げさせたい文章を与えることで、実行が出来る。  
「run.py」にサンプルコードを記述する。  
  
**注意点**  
- tts_main.py 29行目のdevice変数に与えるものとして、  
CPUで処理させる場合は"cpu"  
GPUで処理させる場合は"cuda"  
を与える。  

- tts_main.pyのbert_models関数では、BERTモデルがない場合はモデルのダウンロードを行う。  
そのため、初回実行時は動作時間が長くなる。  
また、同じ理由によりモバイル回線での実行には注意が必要。  