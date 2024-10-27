# インポート
import librosa  
import numpy as np  

# 音声ファイルからの特徴量抽出
def process_audio(file_path):
    # 音声ファイルを読み込みます
    y, sr = librosa.load(file_path)
    
    # MFCC（メル周波数ケプストラム係数）特徴量を抽出します
    # MFCC: 音声の特徴を表す重要な指標の一つ
    # n_mfcc=13: 13個のMFCC係数を計算します
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    
    # MFCC特徴量を正規化します
    # 平均を0、標準偏差を1に調整することで、データの比較や機械学習に適した形に変換します
    mfcc = (mfcc - np.mean(mfcc)) / np.std(mfcc)
    
    # 処理された MFCC 特徴量を返します
    return mfcc

# 類似度を計算する関数
def calculate_similarity(mfcc1, mfcc2):
    # 二つのMFCC特徴量間のユークリッド距離を計算します
    # ユークリッド距離が小さいほど、二つの音声が似ていることを示します
    distance = np.linalg.norm(mfcc1 - mfcc2)
    
    # 距離の逆数を取ることで、距離が近いほど類似度が高くなるようにします
    # 0除算を避けるために小さな値（1e-10）を足しています
    similarity = 1 / (distance + 1e-10)
    
    return similarity