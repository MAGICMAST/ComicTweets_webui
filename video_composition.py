#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2023/08/01 14:45
# @file:app.py
import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"

from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import numpy as np


class Main:
    def merge_video(self, picture_path_path: str, audio_path_path: str, name: str, file_path: str):
        """
        :param picture_path_list: 图片路径列表
        :param audio_path_list: 音频路径列表
        :return:
        """
        clips = []
        picture_path_list = sorted([os.path.join(picture_path_path, name) for name in os.listdir(picture_path_path) if name.endswith('.png')])
        audio_path_list = sorted([os.path.join(audio_path_path, name) for name in os.listdir(audio_path_path) if name.endswith('.mp3')])
        srt_path_list = sorted([os.path.join(audio_path_path, name) for name in os.listdir(audio_path_path) if name.endswith('.srt')])
        for index, value in enumerate(picture_path_list):
            audio_clip = AudioFileClip(audio_path_list[index])
            img_clip = ImageSequenceClip([picture_path_list[index]], audio_clip.duration)
            img_clip = img_clip.set_position(('center', 'center')).set_duration(audio_clip.duration)

            # 解析对应的SRT文件
            subtitles = self.parse_srt(srt_path_list[index])
            print(subtitles)
            # 为当前视频片段添加字幕
            subs = [self.create_text_clip(img_clip, sub['text'], start=sub['start'], duration=sub['end']-sub['start']) for sub in subtitles]
            clip_with_subs = CompositeVideoClip([img_clip] + subs)

            clip = clip_with_subs.set_audio(audio_clip)
            clips.append(clip)
            print(f"-----------生成第{index}段视频-----------")
        print(f"-----------开始合成视频-----------")
        final_clip = concatenate_videoclips(clips)
        video_path = os.path.join(file_path, name + ".mp4")
        video_path = './test.mp4'
        final_clip.write_videofile(video_path, fps=24)
        return video_path

    def parse_srt(self, srt_path):
        """
        解析SRT字幕文件
        :param srt_path: SRT文件路径
        :return: 字幕数据列表，每个字幕包含开始时间、结束时间和文本
        """
        subtitles = []
        with open(srt_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):
                start_end = lines[i+1].split(' --> ')
                start = self.srt_time_to_seconds(start_end[0].strip())
                end = self.srt_time_to_seconds(start_end[1].strip())
                text = lines[i+2].strip()
                subtitles.append({'start': start, 'end': end, 'text': text})
        return subtitles

    def srt_time_to_seconds(self, time_str):
        """
        将SRT时间格式转换为秒
        :param time_str: SRT时间字符串
        :return: 对应的秒数
        """
        hours, minutes, seconds = map(float, time_str.replace(',', '.').split(':'))
        return hours * 3600 + minutes * 60 + seconds

    def create_text_clip(self,img_clip, text, start, duration):
        """
        创建包含文字的TextClip
        :param text: 字幕文本
        :param start: 字幕开始时间
        :param duration: 字幕持续时间
        :return: TextClip对象
        """
        video_clip_height = img_clip.h # 获取视频的高度


        txt_clip = TextClip(text, fontsize=24, color='blue', font="simhei.ttf", method='label')
        txt_clip = txt_clip.set_start(start).set_duration(duration)
        txt_clip = txt_clip.set_position(lambda t: ('center', max(0.9 * video_clip_height - t * 10, 0.9 * video_clip_height)))

        return txt_clip


    def fl_up(self, gf, t):
        # 获取原始图像帧
        frame = gf(t)

        # 进行滚动效果，将图像向下滚动50像素
        height, width = frame.shape[:2]
        scroll_y = int(t * 10)  # 根据时间t计算滚动的像素数
        new_frame = np.zeros_like(frame)

        # 控制滚动的范围，避免滚动超出图像的边界
        if scroll_y < height:
            new_frame[:height - scroll_y, :] = frame[scroll_y:, :]

        return new_frame


if __name__ == '__main__':
    m = Main()
    picture_path_path = os.path.abspath(f"./image/1txt")
    audio_path_path = os.path.abspath(f"./participle/1txt")
    name = "1txt"
    save_path = os.path.abspath(f"./video/1txt")
    m.merge_video(picture_path_path, audio_path_path, name, save_path)

    
    # img_path = sorted([os.path.join(picture_path_path, name) for name in os.listdir(picture_path_path) if name.endswith('.png')])
    # for i in range(len(img_path)):
    #     img_name = os.path.split(img_path[i])[-1]
    #     img_name = img_name.split('.')[0]
    #     img = io.imread(img_path[i])##img_path[i]就是完整的单个指定文件路径了
    # print(img_path)