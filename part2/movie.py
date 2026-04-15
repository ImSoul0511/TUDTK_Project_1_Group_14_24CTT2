from moviepy import VideoFileClip, concatenate_videoclips

# Đường dẫn tới các file mp4 đã render xong
clip1 = VideoFileClip("media/videos/manim_scene_1/720p30/Scene.mp4")
clip2 = VideoFileClip("media/videos/manim_scene_2/720p30/Scene2.mp4")
clip3 = VideoFileClip("media/videos/manim_scene_2/720p30/Scene2_3D.mp4")
clip4 = VideoFileClip("media/videos/manim_scene_2/720p30/Scene2_Sigma.mp4")
clip5 = VideoFileClip("media/videos/manim_scene_3/720p30/Scene3.mp4")
clip6 = VideoFileClip("media/videos/manim_scene_3/720p30/Scene3_Rotation.mp4")
clip7 = VideoFileClip("media/videos/manim_scene_3/720p30/Scene3_Conclusion.mp4")
clip8 = VideoFileClip("media/videos/manim_scene_4/720p30/Scene4_SVD.mp4")
final_clip = concatenate_videoclips([clip1, clip2, clip3, clip4, clip5, clip6, clip7, clip8])
final_clip.write_videofile("Ket_Qua_Cuoi_Cung.mp4")