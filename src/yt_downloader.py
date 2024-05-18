from pytube import YouTube
import subprocess
import os

def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")

def download_video(url):
    try:
        yt = YouTube(url,on_progress_callback=on_progress)
        video = yt.streams.filter(only_audio=True).first()
        audio_file = video.download()
        return audio_file
    except Exception as e:
        print("Error:", str(e))
        return None

def convert_to_mp3(video_file):
    try:
        audio_file = os.path.splitext(video_file)[0] + '.mp3'
        subprocess.run(['ffmpeg', '-i', video_file, audio_file])
        # Delete the mp4 file after conversion
        os.remove(video_file)
        return audio_file
    except Exception as e:
        print("Error:", str(e))
        return None

def main():
    video_url = input("Enter the YouTube video URL: ")
    video_file = download_video(video_url)
    # if video_file:
    #     audio_file = convert_to_mp3(video_file)
    #     if audio_file:
    #         print("Audio downloaded and converted successfully:", audio_file)
    #     else:
    #         print("Failed to convert audio.")
    # else:
    #     print("Failed to download video.")

if __name__ == "__main__":
    main()
