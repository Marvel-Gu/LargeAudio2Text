import os
import subprocess
from openai import OpenAI
import math

# 手动指定 ffmpeg 和 ffprobe 的路径（根据你的安装路径修改）
# Manually specify the path of ffmpeg and ffprobe (modify according to your installation path)
ffmpeg_path = ""  # e.g. "D:\\ffmpeg-7.0.2-essentials_build\\ffmpeg-7.0.2-essentials_build\\bin\\ffmpeg.exe"
ffprobe_path = ""  # e.g. "D:\\ffmpeg-7.0.2-essentials_build\\ffmpeg-7.0.2-essentials_build\\bin\\ffprobe.exe"


# 音频文件路径
# Audio file path
audio_file_path = ""


# 获取音频文件的时长（秒）
# Get the duration of the audio file (in seconds)
def get_audio_duration(file_path):
    command = [ffprobe_path, "-v", "error", "-show_entries", "format=duration", "-of",
               "default=noprint_wrappers=1:nokey=1", file_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return float(result.stdout.strip())


# 获取音频文件的大小（字节）
# Get the size of the audio file (bytes)
def get_audio_size(file_path):
    return os.path.getsize(file_path)


# 计算最大分割时长
# Calculate the max split duration
def get_max_chunk_size(audio_size_bytes, audio_duration):
    max_file_size = 25 * 1024 * 1024

    num_chunks_size = math.ceil(audio_size_bytes / max_file_size)

    chunk_size = audio_duration / num_chunks_size

    return math.ceil(chunk_size)


# 分割音频文件
# Split the audio file
def split_audio(file_path, chunk_size):
    duration = get_audio_duration(file_path)
    num_chunks = int(duration / chunk_size) + 1
    chunks = []
    for i in range(num_chunks):
        start_time = i * chunk_size
        output_file = f"audio_chunk_{i}.m4a"
        command = [
            ffmpeg_path,
            "-i", file_path,
            "-ss", str(start_time),
            "-t", str(chunk_size),
            "-c", "copy",
            output_file
        ]
        subprocess.run(command, check=True)
        chunks.append(output_file)
    return chunks


# 调用OpenAI API进行转录, prompt为可选参数，可以根据需要调整, 如果没有prompt, 默认会转换为繁体中文
# Call the OpenAI API for transcription, prompt is an optional parameter, which can be adjusted as needed.
def transcribe_audio(file_path, prompt=None):
    client = OpenAI(api_key="")  # SECRET KEY
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            prompt="",  # optional parameter, adjust as needed
            language="zh"  # optional parameter, adjust as needed
        )
    return response.text


def main():
    duration = get_audio_duration(audio_file_path)
    size = get_audio_size(audio_file_path)
    chunk_size = get_max_chunk_size(size, duration)
    # 默认为最大的可取值, 可以根据自身需求修改, 默认单位为秒
    # The default value is the maximum possible value,
    # which can be modified according to your needs. The default unit is seconds.
    # e.g. chunks = split_audio(audio_file_path,chunk_size=10*60)
    chunks = split_audio(audio_file_path, chunk_size)

    transcripts = []
    previous_transcript = None

    for i, chunk_path in enumerate(chunks):
        # 使用前一个片段的最后224个字符作为prompt
        if previous_transcript:
            prompt = previous_transcript[-224:]
        else:
            prompt = None

        transcript = transcribe_audio(chunk_path, prompt=prompt)
        transcripts.append(transcript)

        # 更新前一个片段的转录
        # Update the transcription of the previous segment
        previous_transcript = transcript

        # 删除临时文件
        # Delete temporary files
        os.remove(chunk_path)

    # 合并转录结果
    # Merge transcription results
    full_transcript = "\n".join(transcripts)
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(full_transcript)

    print("Transcription completed, results saved to transcript.txt")


if __name__ == "__main__":
    main()

