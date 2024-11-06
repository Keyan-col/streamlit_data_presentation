import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import traceback
from SQL_reader import get_data


def restructure_data(data_list):
    if not data_list:
        return {}

    return {
        str(item['id']): {
            k: v
            for k, v in item.items() if k != 'id'
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
            raw_data = get_data('temp_video', password)
            if raw_data and raw_data.get('data'):  # 确保获取到数据
                st.session_state.video_data = restructure_data(
                    raw_data['data'])
                st.session_state.authenticated = True
                st.rerun()  # 重新运行以更新界面
            else:
                st.error("获取数据失败")
        else:
            st.warning("请输入密码")

# 主应用部分
else:
    with st.sidebar:
        st.title("🎥 视频数据平台")
        st.markdown("---")

        # 显示视频列表
        selected = None
        for video_name in st.session_state.video_data.keys():
            if st.sidebar.button(f"📹 {video_name}", key=video_name):
                selected = video_name

    # 主页面内容
    if selected:
        # 创建两列布局
        col1, col2 = st.columns([2, 1])

        with col1:
            st.title(f"📹 {selected}")
            # 显示视频
            st.video(st.session_state.video_data[selected]["source"])

        with col2:
            # 显示元数据
            st.subheader("视频信息")
            metadata = st.session_state.video_data[selected]

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
                unseen_keys = ['id', 'is_valid', 'last_update']
                for key, value in metadata.items():
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
