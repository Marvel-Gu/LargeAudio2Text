# LargeAudio2Text

## Introduction
本项目旨在通过 OpenAI 的 Whisper 模型将音频文件转录为文本。为了处理较大的音频文件，项目支持将音频分割为较小的片段，并逐段进行转录。主要满足自己将播客音频转为文字的需求。

This project aims to transcribe audio files into text using OpenAI's Whisper model. To handle large audio files, the project supports splitting the audio into smaller chunks and transcribing them individually. It mainly meets my own needs of converting podcast audio into text.

## Features  
- 支持多种音频格式（mp3, mp4, mpeg, mpga, m4a, wav, webm）。  
  Supports multiple audio formats (mp3, mp4, mpeg, mpga, m4a, wav, webm).  
- 自动分割音频文件（支持按时间长度分割）。

  Automatically splits audio files (based on duration).  
- 使用 OpenAI Whisper 模型进行高精度转录。  
  Uses the OpenAI Whisper model for high-accuracy transcription.  
- 支持南非语、阿拉伯语、亚美尼亚语、阿塞拜疆语、白俄罗斯语、波斯尼亚语、保加利亚语、加泰罗尼亚语、中文、克罗地亚语、捷克语、丹麦语、荷兰语、英语、爱沙尼亚语、芬兰语、法语、加利西亚语、德语、希腊语、希伯来语、印地语、匈牙利语、冰岛语、印尼语、意大利语、日语、卡纳达语、哈萨克语、韩语、拉脱维亚语、立陶宛语、马其顿语、马来语、马拉地语、毛利语、尼泊尔语、挪威语、波斯语、波兰语、葡萄牙语、罗马尼亚语、俄语、塞尔维亚语、斯洛伐克语、斯洛文尼亚语、西班牙语、斯瓦希里语、瑞典语、塔加洛语、泰米尔语、泰语、土耳其语、乌克兰语、乌尔都语、越南语和威尔士语（默认为中文）。  
  Supports Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh transcription (Chinese by default).

## Quick Start

### 1. Install Dependencies  
确保已安装以下工具和库：  
Ensure the following tools and libraries are installed:  
- Python 3.8 或更高版本  
  Python 3.8 or higher  
- FFmpeg（用于音频处理）  
  FFmpeg (for audio processing) 

FFmpeg下载链接: https://ffmpeg.org/download.html#build-windows

FFmpeg download link: https://ffmpeg.org/download.html#build-windows

默认使用最新版本OpenAI SDK, 如果使用旧版, 请升级:

The latest version of OpenAI SDK is used by default. If you use an older version, please upgrade:

```bash
pip install --upgrade openai
```

### 2. Configure File Paths and API Key
在代码中设置以下参数：
Set the following parameters in the code:

- ffmpeg_path 和 ffprobe_path：FFmpeg 和 FFprobe 的路径。
  ffmpeg_path and ffprobe_path: Paths to FFmpeg and FFprobe.
- OpenAI(api_key="")：你的 OpenAI API 密钥。

  OpenAI(api_key=""): Your OpenAI API key.
- audio_file_path：音频文件的路径。

  audio_file_path: Path to your audio file.

## Usage Instructions
### 1. Max Chunk Size 最大分割时长 
根据文件大小和时长, 计算出最大的分割时长

Calculate the maximum split duration based on file size and duration

### 2. Audio Splitting 音频分割
音频文件默认将根据最大分割时长分割为多个片段。但你也可以根据需要调整 chunk_size 参数。

By default, the audio file will be split into multiple segments based on the `max_chunk_size`. But you can adjust the chunk_size parameter as needed.


### 3. Transcription Parameters 转录参数

- prompt：可选参数，用于提供上下文以提高转录准确性。默认为"", 加上合适的prompt会使转录效果更好, 且帮助转录为简体字(中文默认转录成繁体字)。

prompt: An optional parameter to provide context for better transcription accuracy. The default is "".
- language：指定转录语言（默认为中文）。

language: Specifies the transcription language (default is Chinese).

### 4. Temporary File Deletion 删除临时文件
脚本会在转录完成后自动删除生成的音频片段文件。

The script will automatically delete the generated audio chunk files after transcription.