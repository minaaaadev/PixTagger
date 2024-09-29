import json
from collections import Counter
import streamlit as st

'''
def tagserch_image_info(file_path):
    # ファイルを開いてデータを読み込む
    with open(file_path, 'r', encoding='utf-8') as f:
        images_data = json.load(f)  # ファイルオブジェクトを読み込む

    # タグをフラットにするためのリスト内包表記
    tags = [tag for item in images_data for tag in item['tags']]  # item['tag']がリストの場合に対応
    tag_count = Counter(tags)
    print(tag_count)
'''
# 'images.json' ファイルをパスとして渡す
# ファイルを開いてデータを読み込む
file_path = r""
with open(file_path, 'r', encoding='utf-8') as f:
    images_data = json.load(f)  # ファイルオブジェクトを読み込む

# タグをフラットにするためのリスト内包表記
tags = [tag for item in images_data for tag in item['tags']]  # item['tag']がリストの場合に対応
tag_count = Counter(tags)
# tag_countを多い順に
tag_count = [k for k, v in tag_count.most_common() for _ in range(v)]
print(tag_count)

st.title('tags')
st.write(tag_count)