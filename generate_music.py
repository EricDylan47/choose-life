#!/usr/bin/env python3
"""
生成简单的氛围音乐 - 低沉的环境音
模拟那种迷茫、压抑的Midwest emo氛围
"""
import wave
import struct
import math
import random
import os

def generate_ambient_drone(filename="bgm.mp3", duration=120):
    """生成环境音"""
    sample_rate = 44100
    num_samples = duration * sample_rate

    # 转换为WAV格式（更简单）
    wav_filename = filename.replace(".mp3", ".wav")

    print(f"正在生成氛围音乐: {wav_filename}")

    with wave.open(wav_filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)

        # 生成低沉的氛围音 - 混合多个低频正弦波
        for i in range(num_samples):
            t = i / sample_rate

            # 基础低音 - 非常低沉的持续音
            bass = math.sin(2 * math.pi * 55 * t) * 0.3  # 55Hz 低音A

            # 第二个低音 - 稍微不和谐
            bass2 = math.sin(2 * math.pi * 58 * t) * 0.2  # 稍微走调

            # 第三个 - 更低
            bass3 = math.sin(2 * math.pi * 40 * t) * 0.25

            # 添加一些随机波动 - 模拟lo-fi效果
            noise = random.uniform(0.98, 1.02)

            # 轻微的节奏感
            beat = (math.sin(2 * math.pi * 0.5 * t) + 1) * 0.1 + 0.9

            # 混合
            sample = (bass + bass2 + bass3) * noise * beat

            # 限制范围
            sample = max(-1.0, min(1.0, sample))

            # 写入
            packed = struct.pack('h', int(sample * 16000))
            wav_file.writeframes(packed)

            if i % (sample_rate * 10) == 0:
                print(f"  已生成 {int(t)} 秒...")

    print(f"完成! 文件保存为: {wav_filename}")
    print("注意: 生成的WAV文件可以直接播放")

    # 尝试转换为MP3（如果ffmpeg可用）
    try:
        import subprocess
        subprocess.run(["which", "ffmpeg"], check=True, capture_output=True)
        mp3_filename = filename
        subprocess.run(["ffmpeg", "-i", wav_filename, "-y", mp3_filename], check=True)
        os.remove(wav_filename)
        print(f"已转换为MP3: {mp3_filename}")
    except:
        print(f"ffmpeg不可用，已保存为WAV格式")
        return wav_filename

    return mp3_filename

if __name__ == "__main__":
    print("=" * 50)
    print("  生成氛围背景音乐")
    print("  时长: 2分钟")
    print("=" * 50)

    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgm.mp3")
    generate_ambient_drone(output, duration=120)
