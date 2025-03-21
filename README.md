# souzoukougaku_hikiage
引き揚げ証言のQ&amp;Abot

## アプリの利用方法
Releasesより最新版のインストーラをダウンロードし，手順に従うことでアプリをインストールできます．  

## プログラムの利用方法
- https://github.com/ramsrigouthamg/Questgen.ai  
- https://github.com/kouki-f/souzoukougaku_hikiage/blob/main/output_voice/howtorun.md  
上記のリポジトリ内のREADMEを参考にして環境構築を行う必要がある.  

- https://drive.google.com/drive/folders/1NnLnkQbxN02Wfk9rjcqQAtzYwNqDUizr?usp=sharing  
容量が大きくgithubに上げられなかったファイルはリンク内のGDriveに残している．  

-「ja_core_news_md」ファイルは「_internal」フォルダに格納する．  
-「00617.mp4」ファイルは「data」フォルダに格納する．  
-「style_bert_vits2」フォルダは，pythonのライブラリを纏めているフォルダ内に入れる． 

Microsoft Store版のPythonを用いている場合，以下のディレクトリに入れれば動くと思う．  
- C:\Users\ {ユーザー名}\AppData\Local\Packages\PythonSoftwareFoundation\Python311_{ランダムな英数字列}\LocalCache\local-packagesz


## 注意点など
gui_flet.pyを実行することでプログラムが開始する．  
pygameライブラリはv2.4.0でないとランタイムエラーが発生する。  
python3.11を使用して開発を行った．その他のバージョンだと互換性の問題で動作しない事が多くあった．  


## 要改善点
- GUI上からのDB編集機能が乏しい．追加は出来るが，上書きや削除が不可能，  
- 検索システムの精度が不十分．同じような文脈でも文章のニュアンスによって全く異なる回答が得られる場合がある．  
- そもそもデータ量がかなり不十分.  
- GUIの表示などを含めた設定機能がない．そのため，ウィンドウサイズや全画面表示など，表示方法はプログラムを直接弄る必要性あり  
- 容量が大きく，現在は約2.5GBとなっている．ローカルで全部動作させているため，通信を必要としないこととトレードオフだとは考えているが，もし可能であれば改善できるに越したことはない．
- style_bert_vits2のライブラリを直接弄っているため，pipで落としても期待した動作にはならない．現在はGDriveに格納しているため，それを使う形になっている．  
- 製作者が開発当時フロントエンド開発の知識に乏しかったので，一つのプログラムに殆どのスクリプトが記述されており，可読性が若干怪しい.  
