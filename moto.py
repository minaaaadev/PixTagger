import json
import os
import streamlit as st
from PIL import Image
import webbrowser


# 画像ファイル名とタグを表示する関数
def display_image_info(image_id, json_path, image_folder):
    # JSONファイルを開いてデータを読み込む
    with open(json_path, 'r', encoding='utf-8') as json_file:
        images_data = json.load(json_file)

    # 対応する画像が見つかったかどうかのフラグ
    found = False

    for image_data in images_data:
        # IDが一致する場合にファイル名とタグを表示
        if str(image_data['id']) == str(image_id):
            found = True
            # タグを表示
            st.write(f"**ID**: {image_id}")
            if image_data['tags']:
                st.write(f"**Tags**: {', '.join(image_data['tags'])}")
            else:
                st.write("**Tags**: No tags available")

            # 連番ファイル名を表示
            image_files = []
            for i in range(100):  # 最大100枚まで対応（必要に応じて調整可能）
                for ext in ['.png', '.jpg']:  # 拡張子を順に確認
                    file_name = f"{image_id}_p{i}{ext}"
                    file_path = os.path.join(image_folder, file_name)

                    # ファイルが存在するかチェック
                    if os.path.exists(file_path):
                        image_files.append(file_path)

            # 画像ファイルが見つかった場合は表示
            if image_files:
                st.write(f"**Files**:")
                for image_file in image_files:
                    img = Image.open(image_file)
                    st.image(img, caption=os.path.basename(image_file), use_column_width=True)
                    # クリックして画像を開く
                    if st.button(f"Open {os.path.basename(image_file)}"):
                        webbrowser.open(f'file://{image_file}')
            else:
                # 単一ファイルを確認
                for ext in ['.png', '.jpg']:
                    file_name = f"{image_id}_p0{ext}"
                    file_path = os.path.join(image_folder, file_name)
                    if os.path.exists(file_path):
                        image_files.append(file_path)

                if image_files:
                    st.write(f"**Files**:")
                    for image_file in image_files:
                        img = Image.open(image_file)
                        st.image(img, caption=os.path.basename(image_file), use_column_width=True)
                        # クリックして画像を開く
                        if st.button(f"Open {os.path.basename(image_file)}"):
                            webbrowser.open(f'file://{image_file}')
                else:
                    st.write("No images found in the specified folder.")

            break

    if not found:
        st.write(f"No data found for ID: {image_id}")


# Streamlitアプリのメイン部分
def main():
    st.title("Pixiv Image Viewer")

    # JSONファイルのパスと画像フォルダのパスを設定
    json_path = r"/Users/mikuru/Downloads/Bookmark list-total 87-from piximanのブックマーク - pixiv-2024／9／27 12：18：27.json"  # JSONファイルのパス
    image_folder = r"/Users/mikuru/Downloads/piximanのブックマーク - pixiv"  # 画像フォルダのパス

    # ユーザーにidを入力してもらう
    image_id = st.text_input("Enter the image ID:")

    # IDが入力された場合に画像情報を表示
    if image_id:
        display_image_info(image_id, json_path, image_folder)


# Streamlitアプリを実行
if __name__ == "__main__":
    main()
