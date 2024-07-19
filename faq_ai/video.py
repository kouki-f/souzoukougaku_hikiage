import cv2
from ffpyplayer.player import MediaPlayer

def PlayVideoWithSound(video_path, start_time, end_time, video_text):
    def get_audio_player(video_path):
        return MediaPlayer(video_path)

    # 動画を読み込み
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    # 音声プレイヤーを作成
    player = get_audio_player(video_path)
    
    # 動画のフレームレートを取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 開始位置と終了位置のフレーム数を計算
    start_frame = int(start_time * fps)
    print(start_frame)
    end_frame = int(end_time * fps)
    
    # 開始位置にシーク
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    # 音声の開始位置にシーク
    player.seek(start_time, relative=False)
    
    # 現在のフレーム位置を取得
    current_frame = start_frame
    
    while cap.isOpened() and current_frame <= end_frame:
        ret, frame = cap.read()
        frame_resized = cv2.resize(frame, (int(int(width)/2), int(int(height)/2)))
        if not ret:
            break

        add_text(frame, video_text)
        # フレームを表示
        cv2.imshow('Video', frame_resized)
        
        # 音声を再生
        audio_frame, val = player.get_frame()
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
        
        # フレームを進める
        current_frame += 1
        
        # qキーが押されたら終了
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break
    
    # キャプチャを解放してウィンドウを閉じる
    cap.release()
    cv2.destroyAllWindows()
    player.close_player()

def add_text(img, text):
    # 文字を追加する位置 (x, y)
    position = (500, 500)

    # フォントの種類
    font = cv2.FONT_HERSHEY_SIMPLEX

    # フォントサイズ
    font_scale = 5

    # 文字の色 (B, G, R) 形式
    color = (255, 0, 0)

    # 文字の太さ
    thickness = 2

    # 画像に文字を追加する
    cv2.putText(img, text, position, font, font_scale, color, thickness)

if __name__ == "__main__":
    PlayVideoWithSound("data/00617.mp4", 770, 803, "aiueo")