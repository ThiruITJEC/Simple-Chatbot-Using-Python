import streamlit as st
import ollama
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="🔥 TamilanAI Ultra Pro",
    page_icon="🔥",
    layout="wide"
)

# --------------------------------------------------
# GLOBAL STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stop_generation" not in st.session_state:
    st.session_state.stop_generation = False

if "bg_index" not in st.session_state:
    st.session_state.bg_index = 0

# --------------------------------------------------
# SIDEBAR CONTROL ROOM
# --------------------------------------------------
with st.sidebar:
    st.header("🎛️ TamilanAI Control Room")

    model = st.selectbox(
        "🧠 Model",
        ["gemma3:latest", "llama3:latest", "mistral:latest"]
    )

    temperature = st.slider("🔥 Creativity", 0.0, 1.5, 0.8, 0.1)
    typing_speed = st.slider("⌨️ Typing Speed", 0.005, 0.04, 0.015)
    streaming = st.toggle("⚡ Streaming Mode", True)

    bg_type = st.radio("🖼️ Background Type", ["🎥 Video", "🖼️ Image"])

    bg_video = st.selectbox(
        "🎬 Video Wallpaper",
        ["Cyber Rain", "Temple Fire"]
    )

    # Expanded Tamil-background images
    image_sources = {
        "Meenakshi Temple":
            "https://upload.wikimedia.org/wikipedia/commons/6/6b/Meenakshi_Amman_Temple_panorama.jpg",
        "Brihadeeswarar":
            "https://upload.wikimedia.org/wikipedia/commons/1/19/Brihadeeswarar_Temple.jpg",
        "Royal Sunset":
            "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
        "Cyber City":
            "https://images.unsplash.com/photo-1518770660439-4636190af475",
        "Thanjavur Temple":
            "https://upload.wikimedia.org/wikipedia/commons/0/02/Thanjavur_Brihadeeswarar_Temple_2.jpg",
        "Pongal Festival":
            "https://images.unsplash.com/photo-1618835962148-cf177563c6c0",
        "Tamil Village Sunrise":
            "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0",
        "Bharatanatyam Dance":
            "https://images.unsplash.com/photo-1594781988671-bde5b0c0f2fc",
        "Temple Corridor":
            "https://images.unsplash.com/photo-1580641362333-0f4b0b7d9f5b",
        "Ancient Tamil Inscriptions":
            "https://images.unsplash.com/photo-1612756317587-9a0e8f2094f2",
        "Palanquin Festival":
            "https://images.unsplash.com/photo-1606112219348-204d7d8b94ee",
        "Coconut Grove Sunset":
            "https://images.unsplash.com/photo-1618835962147-cf177563c6b1",
        "Classical Temple Lamp":
            "https://images.unsplash.com/photo-1605549468873-6f2f4c3e0a7d"
    }

    bg_image = st.selectbox(
        "🌄 Image Wallpaper",
        list(image_sources.keys())
    )

    st.divider()

    system_prompt = st.text_area(
        "🧠 System Instruction (ChatGPT-style)",
        value="You are TamilanAI. Speak proudly like a Tamil person. Use Tamil or Tanglish naturally. Add punch dialogues. Be motivational. Never break character.",
        height=160
    )

    if st.button("🔁 Regenerate Last"):
        if len(st.session_state.messages) >= 2:
            st.session_state.messages.pop()
            st.rerun()

    if st.button("🛑 Stop Generation"):
        st.session_state.stop_generation = True

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# BACKGROUND RENDER
# --------------------------------------------------
video_sources = {
    "Cyber Rain": "https://www.w3schools.com/howto/rain.mp4",
    "Temple Fire": "https://www.w3schools.com/howto/rain.mp4"
}

if bg_type == "🎥 Video":
    st.markdown(f"""
    <video autoplay loop muted playsinline id="bg-video">
        <source src="{video_sources[bg_video]}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)
    bg_css = """
    #bg-video {
        position: fixed;
        inset: 0;
        min-width: 100%;
        min-height: 100%;
        object-fit: cover;
        z-index: -3;
        filter: brightness(0.35) saturate(1.2);
    }
    """
else:
    st.session_state.bg_index = list(image_sources.keys()).index(bg_image)
    bg_image_url = image_sources[bg_image]
    bg_css = f"""
    .stApp {{
        background:
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)),
            url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        animation: zoomBg 40s infinite alternate;
    }}
    """

# --------------------------------------------------
# CINEMATIC CSS
# --------------------------------------------------
st.markdown(f"""
<style>
{bg_css}

@keyframes zoomBg {{
    from {{ background-size: 100%; }}
    to {{ background-size: 112%; }}
}}

.stApp::before {{
    content:"";
    position: fixed;
    inset:0;
    background-image:
        radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    animation: float 30s linear infinite;
    pointer-events:none;
}}

@keyframes float {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-120px); }}
}}

.user-box {{
    background: rgba(255,255,255,0.92);
    color: black;
    padding: 14px;
    border-radius: 14px;
    animation: fadeUp .4s ease;
}}

.assistant-box {{
    background: rgba(20,30,40,0.85);
    backdrop-filter: blur(12px);
    color: #eaffff;
    padding: 16px;
    border-radius: 18px;
    animation: fadeUp .4s ease, glow 2s infinite;
}}

@keyframes fadeUp {{
    from {{ opacity:0; transform: translateY(20px); }}
    to {{ opacity:1; transform: translateY(0); }}
}}

@keyframes glow {{
    0% {{ box-shadow: 0 0 12px rgba(0,255,200,.3); }}
    50% {{ box-shadow: 0 0 30px rgba(0,255,200,.9); }}
    100% {{ box-shadow: 0 0 12px rgba(0,255,200,.3); }}
}}

.cursor {{
    animation: blink 1s infinite;
}}

@keyframes blink {{
    50% {{ opacity: 0; }}
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Blinking animation */
@keyframes blink {
    0% {opacity: 1;}
    50% {opacity: 0;}
    100% {opacity: 1;}
}

/* Fade-in from top */
@keyframes fadeDown {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Apply to title */
.title-blink {
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    color: #ff4500;
    animation: fadeDown 1s ease forwards, blink 1s infinite;
}

/* Apply to subtitle */
.subtitle-blink {
    text-align: center;
    font-size: 1.5rem;
    color: #ffff99;
    animation: fadeDown 1.5s ease forwards, blink 1.2s infinite;
    margin-top: -10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-blink'>🔥 Pesalam Vanga AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-blink'>Time iruntha Konjam Pesittu Ponga⚡</div>", unsafe_allow_html=True)


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"<div class='user-box'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f"<div class='assistant-box'>{msg['content']}</div>", unsafe_allow_html=True)
# --------------------------------------------------
# CHAT HISTORY SIDEBAR
# --------------------------------------------------
with st.sidebar.expander("📝 Chat History", expanded=True):
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            role = "You" if msg["role"] == "user" else "TamilanAI"
            st.markdown(f"**{role}:** {msg['content']}")
    else:
        st.write("No chat history yet.")

    st.divider()
    
    # Export history
    if st.button("📄 Export Chat"):
        chat_text = "\n".join(
            [f"{'You' if m['role']=='user' else 'TamilanAI'}: {m['content']}" 
             for m in st.session_state.messages]
        )
        st.download_button(
            label="Download Chat History",
            data=chat_text,
            file_name="tamilanai_chat_history.txt",
            mime="text/plain"
        )
        


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
prompt = st.chat_input("🔥 தமிழிலோ Tanglish-லோ பேசு...")

if prompt:
    st.session_state.stop_generation = False
    st.session_state.messages.insert(0, {
        "role": "system",
        "content": system_prompt
    })
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(f"<div class='user-box'>{prompt}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        reply = ""

        if streaming:
            stream = ollama.chat(
                model=model,
                messages=st.session_state.messages,
                options={"temperature": temperature},
                stream=True
            )

            for chunk in stream:
                if st.session_state.stop_generation:
                    break
                reply += chunk["message"]["content"]
                placeholder.markdown(
                    f"<div class='assistant-box'>{reply}<span class='cursor'>▌</span></div>",
                    unsafe_allow_html=True
                )
                time.sleep(typing_speed)
        else:
            response = ollama.chat(
                model=model,
                messages=st.session_state.messages,
                options={"temperature": temperature}
            )
            reply = response["message"]["content"]

        placeholder.markdown(
            f"<div class='assistant-box'>{reply}</div>",
            unsafe_allow_html=True
        )

        st.session_state.messages.append({"role": "assistant", "content": reply})
