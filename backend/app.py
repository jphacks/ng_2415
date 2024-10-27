# インポート
from flask import Flask, request, jsonify  
from flask_cors import CORS  
import os  
import librosa  
import numpy as np 
import sqlite3  
from utils.audio_processing import process_audio, calculate_similarity  # audio_processing.pyから関数をインポートします
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO)  # ログレベルをINFOに設定します

# フロントエンドからのリクエストの許可を行う
app = Flask(__name__)  # Flaskアプリケーションを作成します
CORS(app)  # CORSを有効にし、異なるドメインからのリクエストを許可します

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('songs.db')  # 'songs.db'というSQLiteデータベースに接続します
    conn.row_factory = sqlite3.Row  # 結果を辞書形式で取得できるように設定します
    return conn  # データベース接続を返します

# 応援歌識別エンドポイント
@app.route('/api/audio', methods=['POST'])  # '/upload'へのPOSTリクエストを処理する関数を定義します
def upload_audio():
    if 'file' not in request.files:  # リクエストにファイルが含まれているか確認します
        return jsonify({"error": "ファイルが見つかりませんでした"}), 400  # ファイルがない場合、エラーを返します

    file = request.files['file']  # リクエストからファイルを取得します
    filepath = os.path.join("data", file.filename)  # ファイルの保存先パスを作成します
    file.save(filepath)  # ファイルを保存します

    try:
        result = identify_song(filepath)  # 曲を識別します
        if result:
            return jsonify(result)  # 識別結果をJSON形式で返します
        else:
            return jsonify({"error": "一致する応援歌が見つかりませんでした"}), 404  # 一致する曲がない場合、エラーを返します
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 例外が発生した場合、エラーを返します

# 歌詞取得エンドポイント
@app.route('/api/lyrics/<song_name>', methods=['GET'])  # '/lyrics/<曲名>'へのGETリクエストを処理する関数を定義します
def get_lyrics(song_name):
    conn = get_db_connection()  # データベースに接続します
    song = conn.execute('SELECT * FROM songs WHERE name = ?', (song_name,)).fetchone()  # 指定された曲名の情報を取得します
    conn.close()  # データベース接続を閉じます

    if song:
        return jsonify({"lyrics": song['lyrics']})  # 歌詞をJSON形式で返します
    else:
        return jsonify({"error": "応援歌が見つかりませんでした"}), 404  # 曲が見つからない場合、エラーを返します

# Librosaを使った応援歌識別関数
def identify_song(filepath):
    input_mfcc = process_audio(filepath)  # 入力音声のMFCC特徴量を抽出します
    
    conn = get_db_connection()  # データベースに接続します
    songs = conn.execute('SELECT * FROM songs').fetchall()  # すべての曲の情報を取得します
    conn.close()  # データベース接続を閉じます

    best_match = None
    best_similarity = float('-inf')  # 最高の類似度を負の無限大で初期化します
    similarity_threshold = 0.5  # 類似度の閾値を設定します

    for song in songs:
        song_mfcc = np.frombuffer(song['mfcc'], dtype=np.float32).reshape(13, -1)  # データベースから取得したMFCCを適切な形状に変換します
        similarity = calculate_similarity(input_mfcc, song_mfcc)  # 類似度を計算します
        
        if similarity > best_similarity:  # より高い類似度が見つかった場合
            best_similarity = similarity
            best_match = song

    if best_similarity > similarity_threshold:  # 最高の類似度が閾値を超える場合
        return {'song': best_match['name'], 'lyrics': best_match['lyrics']}
    else:
        return None  # 閾値を超える類似度がない場合、Noneを返します


#確認
@app.route('/')
def check():
    return jsonify({"message": "API is running!"}), 200  # APIが正常に動作していることを示すメッセージを返します

if __name__ == '__main__':
    app.run(debug=True)  # アプリケーションをデバッグモードで実行します