import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import traceback
from SQL_reader import get_data, get_length
import urllib.parse


def restructure_data(data_list):
    if not data_list:
        return {}

    return {
        str(urllib.parse.unquote(item['video_id'])): {
            k: v
            for k, v in item.items() if k != 'video_id'
        }
        for item in data_list
    }


def show_data():
    with st.sidebar:
        st.title("🎥 视频数据平台")
        st.markdown("---")

        # 显示视频列表
        selected = None
        for video_name in video_data.keys():
            if st.sidebar.button(f"📹 {video_name}", key=video_name):
                selected = video_name

    # 主页面内容
    if selected:
        # 创建两列布局
        col1, col2 = st.columns([2, 1])

        with col1:
            st.title(f"📹 {selected}")
            # 显示视频
            st.video(video_data[selected]["source"], )

        with col2:
            # 显示元数据
            st.subheader("视频信息")
            metadata = video_data[selected]

            # 使用卡片样式显示元数据
            with st.container():
                st.markdown("""
                    <style>
                        .metadata-item {
                            padding: 10px;
                            background-color: #a9a9a9;
                            border-radius: 5px;
                            margin: 5px 0;
                        }
                    </style>
                """,
                            unsafe_allow_html=True)

                for key, value in metadata.items():
                    if key != "标签":
                        st.markdown(f"""
                            <div class="metadata-item">
                                <b>{key}:</b> {value}
                            </div>
                        """,
                                    unsafe_allow_html=True)

    else:
        # 默认显示的内容
        st.title("欢迎使用视频数据平台")
        st.write("请从左侧选择要查看的视频")


# 初始化session_state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'video_data' not in st.session_state:
    st.session_state.video_data = None

# 认证部分
if not st.session_state.authenticated:
    password = st.text_input("请输入数据库密码", type="password")
    if st.button("确认"):
        if password:  # 确保密码不为空
            st.session_state.password = password
            # raw_data = get_data('video_metadata', password)
            # print(raw_data)
            # if raw_data and raw_data.get('data'):  # 确保获取到数据
            #     st.session_state.video_data = restructure_data(
            #         raw_data['data'])
            st.session_state.authenticated = True
            st.rerun()  # 重新运行以更新界面
            # else:
            #     st.error("获取数据失败")
        else:
            st.warning("请输入密码")

# 主应用部分
else:
    # Define items per page
    items_per_page = 20

    # Get the total length of data
    total_length = get_length('video_metadata', st.session_state.password)
    # Calculate total pages
    total_pages = (total_length['data'][0]['num'] - 1) // items_per_page + 1

    # Get current page number from session state or initialize
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    # Determine the start index for the current page
    start_idx = (st.session_state.current_page - 1) * items_per_page

    # Fetch data for the current page
    raw_data = get_data('video_metadata', start_idx, items_per_page,
                        st.session_state.password)
    st.session_state.video_data = restructure_data(raw_data.get('data', []))
    print(st.session_state.video_data)
    video_names = st.session_state.video_data.keys()
    with st.sidebar:
        st.title("🎥 视频数据平台")
        st.markdown("---")

        st.markdown("""
            <style>
                div[data-testid="column"] {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                div[data-testid="stNumberInput"] label {
                    display: none;
                }
                
                /* Adjust button heights */
                .stButton button {
                    height: 50px;
                    padding-top: 0;
                    padding-bottom: 0;
                }
            </style>
        """,
                    unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 1, 2, 1])

        with col1:
            if st.button("◀", key="prev"):
                if st.session_state.current_page > 1:
                    st.session_state.current_page -= 1
                    st.rerun()

        with col2:
            if st.button("▶", key="next"):
                if st.session_state.current_page < total_pages:
                    st.session_state.current_page += 1
                    st.rerun()

        with col3:
            page_number = st.number_input("",
                                          min_value=1,
                                          max_value=total_pages,
                                          value=st.session_state.current_page)

        with col4:
            if st.button("跳转", key="jump"):
                if page_number != st.session_state.current_page:
                    st.session_state.current_page = page_number
                    st.rerun()
        # Display current page and total pages
        st.markdown(f"Page {st.session_state.current_page} of {total_pages}")

        # Display video list for the current page
        selected = None
        # video_names = raw_data.get('data', [])
        for video_name in video_names:
            if st.sidebar.button(f"📹 {video_name}", key=video_name):
                selected = video_name

    # 主页面内容
    if selected:
        # 视频部分
        st.title(f"📹 {st.session_state.video_data[selected]['id']}")
        # 显示视频
        st.video(st.session_state.video_data[selected]["url"])

        # 元数据部分
        st.subheader("视频信息")
        metadata = st.session_state.video_data[selected]

        # 使用卡片样式显示元数据
        st.markdown("""
            <style>
                .metadata-item {
                    padding: 10px;
                    background-color: #a9a9a9;
                    border-radius: 5px;
                    margin: 5px 0;
                }
            </style>
        """,
                    unsafe_allow_html=True)

        unseen_keys = [
            'id', 'is_valid', 'last_update', 'fps', 'dataset_id', 'url',
            'created_at', 'relpath'
        ]

        for key, value in metadata.items():
            if key.lower() == 'url':
                shortened_url = "视频链接"
                st.markdown(f"""
                    <div class="metadata-item">
                        <b>{key}:</b>
                        <a href="{value}" target="_blank" class="url-link">🎥 {shortened_url}</a>
                    </div>
                """,
                            unsafe_allow_html=True)
            if key.lower() == 'relpath':
                readable_path = urllib.parse.unquote(value)
                st.markdown(f"""
                    <div class="metadata-item">
                        <b>{key}:</b> {readable_path}
                    </div>
                """,
                            unsafe_allow_html=True)
            if key not in unseen_keys:
                st.markdown(f"""
                    <div class="metadata-item">
                        <b>{key}:</b> {value}
                    </div>
                """,
                            unsafe_allow_html=True)

    else:
        # 默认显示的内容
        st.title("欢迎使用视频数据平台")
        st.write("请从左侧选择要查看的视频")

    # 可选：添加登出按钮
    if st.sidebar.button("登出"):
        st.session_state.authenticated = False
        st.session_state.video_data = None
        st.experimental_rerun()
