import json
import os
from collections import Counter

import streamlit as st
from PIL import Image
import webbrowser

st.title("PixTagger")

with st.sidebar:
    with st.echo():
        st.write("jsonをアップロード")
        uploaded_file = st.file_uploader("Choose a file", type=['json'])

        image_folder = st.text_input("Enter the image folder path:")
        if image_folder:
            if os.path.exists(image_folder):
                st.write(f"**Image folder path**: {image_folder}")
                st.success("The specified folder exists.")
            else:
                st.error("The specified folder does not exist.")


data = None
tag_count = None
if uploaded_file is not None:
    data = json.load(uploaded_file)
    tags = [tag for item in data for tag in item['tags']]
    tag_count = Counter(tags)

tab1, tab2, tab3, tab4 = st.tabs(["一覧","ID検索","ID検索","DL方法"])
with tab1:
    st.write("一覧")
    if data is not None:
        items = [item for item in data]
        st.write(f"## Number of items: {len(items)}")
        # most_common() でタグの数が多い順に並び替える
        for tag, count in tag_count.most_common():
            st.write(f"{tag}: {count}")

with tab2:
    if data is not None:
        # タグの選択 (タグが多い順にソート)
        sorted_tags = [tag for tag, count in tag_count.most_common()]
        selected_tag = st.selectbox("Select a tag", sorted_tags)

        # 選択されたタグを持つ画像を検索
        if selected_tag:
            st.write(f"## Images with tag: {selected_tag}")
            for item in data:
                if selected_tag in item['tags']:
                    image_id = item['id']
                    # 画像ファイルのパスを生成
                    image_paths = [
                        os.path.join(image_folder, f"{image_id}_p{i}.jpg")
                        for i in range(50)  # 最大50枚の画像を想定
                        if os.path.exists(os.path.join(image_folder, f"{image_id}_p{i}.jpg"))
                    ] + [
                        os.path.join(image_folder, f"{image_id}_p{i}.png")
                        for i in range(50)  # 最大50枚の画像を想定
                        if os.path.exists(os.path.join(image_folder, f"{image_id}_p{i}.png"))
                    ] + [
                        os.path.join(image_folder, f"{image_id}_p{i}.gif")
                        for i in range(50)  # 最大50枚の画像を想定
                        if os.path.exists(os.path.join(image_folder, f"{image_id}_p{i}.gif"))
                    ]

                    # 画像を表示
                    for image_path in image_paths:
                        image = Image.open(image_path)
                        st.image(image, caption=f"{image_id}")

                        # 画像を開くボタン (key引数を追加)
                        if st.button(f"画像を開く ({image_id})", key=f"open_image_{image_path}"):
                            webbrowser.open_new_tab(image_path)

                        # IDでGoogle検索するボタン (key引数を追加)
                        if st.button(f"IDでGoogle検索 ({image_id})", key=f"search_id_{image_path}"):
                            search_url = f"https://www.google.com/search?q={image_id}+pixiv"
                            webbrowser.open_new_tab(search_url)
    with tab3:
        st.write("ID検索")
        image_id = st.text_input("Enter the image ID:")
        if image_id:
            found = False
            for item in data:
                if str(item['id']) == str(image_id):
                    found = True
                    st.write(f"**ID**: {image_id}")
                    if item['tags']:
                        st.write(f"**Tags**: {', '.join(item['tags'])}")
                    else:
                        st.write("**Tags**: No tags available")

                    image_files = []
                    for i in range(100):
                        for ext in ['.png', '.jpg', '.gif']:
                            file_name = f"{image_id}_p{i}{ext}"
                            file_path = os.path.join(image_folder, file_name)

                            if os.path.exists(file_path):
                                image_files.append(file_path)

                    if image_files:
                        st.write(f"**Files**:")
                        for image_file in image_files:
                            img = Image.open(image_file)
                            st.image(img, caption=os.path.basename(image_file), use_column_width=True)
                            if st.button(f"Open {os.path.basename(image_file)}"):
                                webbrowser.open(f'file://{image_file}')
                    else:
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
                                if st.button(f"Open {os.path.basename(image_file)}"):
                                    webbrowser.open(f'file://{image_file}')
                        else:
                            st.write("No images found in the specified folder.")

                    break

            if not found:
                st.write(f"No data found for ID: {image_id}")
    with tab4:
        st.markdown("DL方法"
                    "1. 画像をクリックして開く"
                    "2. 画像を右クリックして保存"

                    )