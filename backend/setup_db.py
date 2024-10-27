import sqlite3
import os
from utils.audio_processing import process_audio

def get_lyrics(song_name):
    lyrics_database = {
        "song_1": "どんぐり ころころ どんぶりこ おいけにはまって さあたいへん どじょうがでてきて こんにちは ぼっちゃん いっしょに あそびましょう どんぐり ころころ よろこんで しばらくいっしょに あそんだが やっぱり おやまが こいしいと ないては どじょうを こまらせた",
        "song_2": "秋の夕日に照る山紅葉 濃いも薄いも 数ある中に 松をいろどる楓や蔦は 山のふもとの裾模様 渓の流に散り浮く紅葉 波にゆられて 離れて寄って 赤や黄色の色さまざまに 水の上にも織る錦",
        "song_3": "夕焼け 小焼けで 日が暮れて 山のお寺の 鐘が鳴る おててつないで みなかえろう からすと いっしょに かえりましょ 子供が かえった あとからは まるい大きな お月さま 小鳥が夢を 見るころは 空には きらきら 金の星"
    }
    return lyrics_database.get(song_name, "歌詞が見つかりませんでした")

def setup_database():
    db_path = 'songs.db'

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lyrics TEXT,
            mfcc BLOB NOT NULL
        )
    ''')

    # 応援歌の音声ファイルが保存されているディレクトリ
    songs_directory = '../data/'  # setup_db.py から見た data/ の相対パス

    # ディレクトリが存在しない場合は作成
    if not os.path.exists(songs_directory):
        os.makedirs(songs_directory)
        print(f"{songs_directory} ディレクトリを作成しました。")

    # 音声ファイルの登録
    for filename in os.listdir(songs_directory):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            song_path = os.path.join(songs_directory, filename)
            song_name = os.path.splitext(filename)[0]  # ファイル名から拡張子を除いた部分を曲名とする
            lyrics = get_lyrics(song_name)

            # 曲名が既に存在する場合はスキップ
            c.execute('SELECT * FROM songs WHERE name = ?', (song_name,))
            if c.fetchone():
                print(f"既に登録済みの曲名: {song_name}。スキップします。")
                continue

            # MFCC 特徴量の抽出
            mfcc = process_audio(song_path)

            # バイナリデータに変換
            fingerprint = mfcc.tobytes()

            # データベースに挿入
            c.execute('''
                INSERT INTO songs (name, lyrics, audio_path, mfcc)
                VALUES (?, ?, ?, ?)
            ''', (song_name, lyrics, song_path, fingerprint))
            print(f"登録済み: {song_name}")

    # 変更を保存して接続を閉じる
    conn.commit()
    conn.close()
    print("データベースの初期化が完了しました。")

if __name__ == "__main__":
    setup_database()