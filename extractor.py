import cv2
import numpy as np
from pathlib import Path
from datetime import datetime

def extract_slides_from_video(video_path, output_dir, similarity_threshold=0.95):
    """
    Extract unique slides from a video file.
    
    Args:
        video_path (str): Path to the video file
        output_dir (str): Directory to save extracted slides
        similarity_threshold (float): Threshold for determining unique frames (0-1)
    
    Returns:
        list: Timestamps of extracted slides
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError("Error opening video file")
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Initialize variables
    unique_frames = []
    timestamps = []
    frame_number = 0
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
            
        frame_number += 1
        current_time = frame_number / fps
        
        # Convert frame to grayscale for comparison
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Check if this frame is unique
        is_unique = True
        for existing_frame in unique_frames:
            # Calculate similarity using structural similarity index
            similarity = cv2.matchTemplate(
                gray_frame, 
                cv2.cvtColor(existing_frame, cv2.COLOR_BGR2GRAY),
                cv2.TM_CCOEFF_NORMED
            )[0][0]
            
            if similarity > similarity_threshold:
                is_unique = False
                break
        
        # If frame is unique, save it
        if is_unique:
            unique_frames.append(frame)
            timestamps.append(current_time)
            
            # Format timestamp for filename
            timestamp_str = datetime.utcfromtimestamp(current_time).strftime('%H-%M-%S')
            output_file = output_path / f"slide_{len(unique_frames):03d}_{timestamp_str}.png"
            
            # Save the frame
            cv2.imwrite(str(output_file), frame)
            
        # Print progress
        if frame_number % 30 == 0:  # Update every 30 frames
            progress = (frame_number / frame_count) * 100
            print(f"Progress: {progress:.1f}%")
    
    # Clean up
    video.release()
    
    return timestamps

def main():
    # Example usage
    video_path = "presentation.mp4"
    output_dir = "extracted_slides"
    
    try:
        timestamps = extract_slides_from_video(video_path, output_dir)
        
        print("\nExtraction complete!")
        print(f"Found {len(timestamps)} unique slides")
        print("\nSlide timestamps:")
        for i, timestamp in enumerate(timestamps, 1):
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            print(f"Slide {i}: {minutes:02d}:{seconds:02d}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()