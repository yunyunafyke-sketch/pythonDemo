import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Streamlit 的代码不是像传统后端那样一直停在某一行等待。
# 用户每次点击按钮、修改输入框、拖动滑块时，脚本都会从上到下重新执行一遍。
# 因此，想在“多次重跑”之间保留数据，就要使用 st.session_state。
# 加载 .env 中的环境变量，便于读取 API Key 等配置。
load_dotenv()

# 设置 Streamlit 页面基础信息。
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="centered"
)

# 通过自定义 CSS 调整页面背景、标题、消息气泡和侧边栏样式。
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
}

.chat-title {
    text-align: center;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
}

.chat-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 32px;
}

.stChatMessage {
    border-radius: 18px;
    padding: 12px;
}

.stTextInput > div > div > input {
    border-radius: 999px;
}

[data-testid="stSidebar"] {
    background: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

# 页面主标题与副标题。
st.markdown('<div class="chat-title">AI Chat Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">基于 OpenAI / DeepSeek 兼容接口的聊天界面</div>', unsafe_allow_html=True)

# 侧边栏用于配置模型服务、模型名称和生成参数。
with st.sidebar:
    st.header("配置")

    provider = st.selectbox(
        "模型服务",
        ["OpenAI", "DeepSeek"]
    )

    # 根据服务商设置接口地址和默认模型。
    if provider == "OpenAI":
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = None
        default_model = "gpt-4o-mini"
    else:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = "https://api.deepseek.com"
        default_model = "deepseek-chat"

    model = st.text_input("模型名称", value=default_model)

    # Temperature 越高，回复通常越发散；越低，回复通常越稳定。
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1
    )

    if st.button("清空聊天记录"):
        # st.session_state 类似“当前用户这次会话专属的临时存储区”。
        # 这里把 messages 重置为空列表，相当于清空当前聊天上下文。
        st.session_state.messages = []
        # st.rerun() 会立刻触发脚本重新执行，让页面马上显示清空后的结果。
        st.rerun()

# 如果没有读取到 API Key，直接终止程序，避免后续请求报错。
if not api_key:
    st.error(f"未检测到 {provider} API Key，请先配置环境变量。")
    # st.stop() 用来中断本次脚本执行，后面的代码不会再继续运行。
    st.stop()

# 创建兼容 OpenAI SDK 的客户端实例。
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# st.session_state 可以理解为一个字典。
# 这里判断 "messages" 这个键是否已存在：
# 1. 不存在：说明用户第一次打开页面，需要初始化聊天记录
# 2. 存在：说明之前已经聊过，本次重跑时继续沿用旧数据
if "messages" not in st.session_state:
    # messages 保存的是整个对话历史。
    # 列表中的每一项都是一个字典，格式和 OpenAI 聊天接口一致：
    # {"role": "user/assistant", "content": "消息内容"}
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "你好，我是你的 AI 助手。"
        }
    ]

# 按顺序渲染历史消息。
# 因为脚本每次都会重跑，所以页面上的聊天记录不能只靠“上一次显示结果”保留，
# 必须从 st.session_state.messages 里重新读出，再重新渲染一遍。
for message in st.session_state.messages:
    # st.chat_message(role) 会创建一个聊天气泡容器。
    # role 常见值是 "user" 和 "assistant"，Streamlit 会按角色显示不同样式。
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 底部输入框用于接收用户当前输入。
# 用户发送消息后，chat_input 会返回本次输入的字符串，然后脚本继续往下执行。
user_input = st.chat_input("输入你的问题...")

if user_input:
    # 先把用户消息写入 session_state。
    # 这样做有两个目的：
    # 1. 页面下次重跑时，这条用户消息不会丢
    # 2. 调用模型接口时，可以把完整上下文一起传给模型
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # st.empty() 会先创建一个“空位置”，后续可以不断往这个位置覆盖新内容。
        # 这里用它实现打字机式的流式输出效果。
        placeholder = st.empty()
        full_response = ""

        try:
            # 把当前完整对话历史传给模型。
            # 注意：这里的 messages 就是前面存到 st.session_state 里的上下文。
            # 没有这份上下文，模型每次都只会看到当前一句，无法连续对话。
            stream = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    placeholder.markdown(full_response + "▌")

            # 流式结束后，去掉输入中的光标效果。
            placeholder.markdown(full_response)

            # 把助手回复也写回 session_state。
            # 这样下一轮提问时，模型才能基于“前面已经回答过什么”继续聊天。
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            # 请求异常时，在页面上直接提示错误信息。
            st.error(f"请求失败：{e}")
