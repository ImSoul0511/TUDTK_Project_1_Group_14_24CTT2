from moviepy import VideoFileClip, concatenate_videoclips

def main():
    """
    Chạy kịch bản ghép video.

    Args:
        None

    Returns:
        None
    """
    # Đường dẫn tới các file mp4 1080p60 đã render xong
    clip1 = VideoFileClip("media/videos/manim_scene_1/1080p60/Scene_1.mp4")
    clip2 = VideoFileClip("media/videos/manim_scene_1/1080p60/Scene_2.mp4")
    
    clip3 = VideoFileClip("media/videos/manim_scene_2/1080p60/Scene_3.mp4")
    clip4 = VideoFileClip("media/videos/manim_scene_2/1080p60/Scene_4.mp4")
    clip5 = VideoFileClip("media/videos/manim_scene_2/1080p60/Scene_5.mp4")
    
    clip6 = VideoFileClip("media/videos/manim_scene_3/1080p60/Scene_6.mp4")
    clip7 = VideoFileClip("media/videos/manim_scene_3/1080p60/Scene_7.mp4")
    clip8 = VideoFileClip("media/videos/manim_scene_3/1080p60/Scene_8.mp4")
    
    clip9 = VideoFileClip("media/videos/manim_scene_4/1080p60/Scene_9.mp4")
    clip10 = VideoFileClip("media/videos/manim_scene_4/1080p60/Scene_10.mp4")
    clip11 = VideoFileClip("media/videos/manim_scene_4/1080p60/Scene_11.mp4")
    
    clip12 = VideoFileClip("media/videos/manim_scene_5/1080p60/Scene_12.mp4")
    clip13 = VideoFileClip("media/videos/manim_scene_5/1080p60/Scene_13.mp4")
    
    final_clip = concatenate_videoclips([
        clip1, clip2, clip3, clip4, clip5, 
        clip6, clip7, clip8, clip9, clip10, 
        clip11, clip12, clip13
    ])
    final_clip.write_videofile("Result.mp4")

if __name__ == "__main__":
    main()