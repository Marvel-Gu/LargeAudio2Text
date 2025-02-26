import os
import openai
import subprocess


# 手动指定 ffmpeg 和 ffprobe 的路径（根据你的安装路径修改）
# Manually specify the path of ffmpeg and ffprobe (modify according to your installation path)
ffmpeg_path = ""  # eg. "D:\\ffmpeg-7.0.2-essentials_build\\ffmpeg-7.0.2-essentials_build\\bin\\ffmpeg.exe"
ffprobe_path = ""  # eg. "D:\\ffmpeg-7.0.2-essentials_build\\ffmpeg-7.0.2-essentials_build\\bin\\ffprobe.exe

# 设置OpenAI API密钥
# Set OpenAI API key
openai.api_key = ""

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


# 分割音频文件, 这里的分割需要根据你的音频文件大小和时长来决定(仅支持mp3, mp4, mpeg, mpga, m4a, wav, and webm类型), 因为whisper仅支持小于 25 MB 的文件
# Split the audio file. The split here needs to be determined according to the size and duration of your audio file
# (only supports mp3, mp4, mpeg, mpga, m4a, wav, and webm types), because whisper only supports files smaller than 25 MB
def split_audio(file_path, chunk_size=10 * 60):  # 每段10分钟（单位：秒）, 根据需要调整 Each segment is 10 minutes (unit: seconds), adjust as needed
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
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            file=audio_file,
            model="whisper-1",
            response_format="text",
            prompt="以下是普通话的句子。",
            language="zh"
        )
    return transcript


def main():
    # 分割音频
    chunks = split_audio(audio_file_path)

    # 初始化转录结果
    transcripts = []
    previous_transcript = None

    # 转录每个音频片段
    for i, chunk_path in enumerate(chunks):
        # 使用前一个片段的最后224个字符作为prompt
        if previous_transcript:
            prompt = previous_transcript[-224:]
        else:
            prompt = None

        # 调用API进行转录
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