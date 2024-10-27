# インポート
import sqlite3
import os
import numpy as np
from utils.audio_processing import process_audio, mfcc_to_binary  # 特徴量抽出とバイナリ変換関数をインポート
import librosa

# データベースとテーブルを作成する関数
def initialize_database():
    conn = sqlite3.connect('cheer_songs.db')
    cursor = conn.cursor()

    # 曲情報と特徴量を格納するテーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lyrics TEXT,
            mfcc BLOB NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("データベースが初期化されました。")

# 曲をデータベースに追加する関数
def add_song_to_db(song_name, lyrics, file_path):
    conn = sqlite3.connect('cheer_songs.db')
    cursor = conn.cursor()

    # 音声ファイルから特徴量を抽出し、バイナリに変換
    mfcc = process_audio(file_path)
    mfcc_binary = mfcc_to_binary(mfcc)

    # データベースに曲情報を挿入
    cursor.execute('INSERT INTO songs (name, lyrics, mfcc) VALUES (?, ?, ?)',
                   (song_name, lyrics, mfcc_binary))
    
    conn.commit()
    conn.close()
    print(f"曲 '{song_name}' がデータベースに追加されました。")

# 複数の曲を一括で追加する関数
def add_songs_bulk(songs_info):
    initialize_database()
    for song in songs_info:
        add_song_to_db(song['name'], song['lyrics'], song['file_path'])

# サンプルデータの挿入
if __name__ == '__main__':
    # ここで曲情報（名前、歌詞、ファイルパス）を定義
    songs_info = [
        {"name": "Cheer Song 1", "lyrics": "応援歌1の歌詞", "file_path": "path/to/song1.wav"},
        {"name": "Cheer Song 2", "lyrics": "応援歌2の歌詞", "file_path": "path/to/song2.wav"},
    ]
    add_songs_bulk(songs_info)
