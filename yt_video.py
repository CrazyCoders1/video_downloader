import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

st.title("🎬 YouTube Downloader with Quality Selection")

url = st.text_input("Paste YouTube link here:")

if url:
    try:
        # Extract video info without downloading
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Show video details
        st.image(info["thumbnail"], width=300)
        st.subheader(info["title"])
        st.write(f"👤 Uploader: {info.get('uploader', 'Unknown')}")
        st.write(f"⏱ Duration: {int(info['duration']//60)} min {int(info['duration']%60)} sec")
        st.write(f"👁 Views: {info.get('view_count', 'N/A')}")

        # Ask video or audio
        option = st.radio("Download as:", ["Video", "Audio"])

        quality_choice = None

        if option == "Video":
            formats = [f for f in info["formats"] if f.get("height")]
            qualities = [f"{f['height']}p - {f['ext']} ({round(f['filesize']/1024/1024,1) if f.get('filesize') else '?'} MB)" for f in formats]
            quality_choice = st.selectbox("Choose video quality:", qualities, index=len(qualities)-1)
            selected_format = formats[qualities.index(quality_choice)]["format_id"]

        else:  # Audio
            formats = [f for f in info["formats"] if f.get("acodec") != "none" and f.get("vcodec") == "none"]
            qualities = [f"{f['abr']} kbps - {f['ext']} ({round(f['filesize']/1024/1024,1) if f.get('filesize') else '?'} MB)" for f in formats if f.get("abr")]
            quality_choice = st.selectbox("Choose audio quality:", qualities)
            selected_format = formats[qualities.index(quality_choice)]["format_id"]

        # Download button
        if st.button("Download"):
            ydl_opts = {
                "format": selected_format,
                "outtmpl": "download.%(ext)s"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            for f in os.listdir():
                if f.startswith("download."):
                    st.success("✅ Download complete!")
                    with open(f, "rb") as file:
                        st.download_button("⬇️ Save File", file, file_name=f)
                    break

    except Exception as e:
        st.error(f"Error: {e}")
