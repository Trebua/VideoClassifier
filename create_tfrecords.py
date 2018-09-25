#Denne filen bruker video2tfrecord for å konvertere mp4 til tfrecords som tydeligvis er fine å bruke??

from video2tfrecord import convert_videos_to_tfrecord #pip install video2tfrecord, pip install opencv-python
#github: https://github.com/ferreirafabio/video2tfrecord

convert_videos_to_tfrecord("data/", "tfrecords/", 1, 5, "*.mp4") 

#convert_videos_to_tfrecord(source_path, destination_path, n_videos_in_record, n_frames_per_video, "*.mp4") 
#source_path containing your .mp4 video files. Set n_frames_per_video="all" if you want all video frames to be stored in the tfrecord file (keep in mind that tfrecord can become very large).
#n_videos_in_record being the number of videos in one single tfrecord file
#n_frames_per_video being the number of frames to be stored per video 
