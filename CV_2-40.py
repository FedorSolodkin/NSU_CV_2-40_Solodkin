import cv2
import time
import os  

class Video_Maker():
    def __init__(self, output_dir="recordings", target_fps=20.0):
        #Capturing your WEBcam
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            print("Error: Failed to open camera.")
            exit()
        
        # Initialize recording directory
        self.output_directory = output_dir 
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)  
        
        # Initialize various state variables
        self.prevTime = 0  # Stores previous timestamp for FPS calculation
        self.start_recording = False  # Recording state flag
        self.target_fps = target_fps  # Desired FPS for output video
        
        # Get camera properties for video writer configuration
        self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Video codec configuration 
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = None  # VideoWriter instance 

    def fps_(self):
        #Calculate real-time FPS based on frame timing
        self.nowTime = time.time()
        
        self.fps = 1 / (self.nowTime - self.prevTime) if (self.nowTime - self.prevTime) > 0 else 0
        self.prevTime = self.nowTime  

    def effect(self):
        #Apply image processing effects to the frame
    
        self.vid_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
     
        self.vid_gray = cv2.GaussianBlur(self.vid_gray, (5, 5), 0)

    def output(self):
        #Add UI overlays and display the video frame
        cv2.putText(self.vid_gray, f"FPS: {int(self.fps)}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Red text
        
        # Show recording status 
        self.status = "REC" if self.start_recording else "STOP"
        cv2.putText(self.vid_gray, self.status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)   
        
        # Display the processed frame in a window
        cv2.imshow('Video', self.vid_gray)

    def record_video(self):
        """Handle recording start/stop logic with file management"""
        if self.key == ord('z'):  # 'z' key toggles recording state
            self.start_recording = not self.start_recording

            if self.start_recording:
                # Find next available filename to avoid overwriting existing recordings
                self.number_of_video = 1
                while True:
                    # Format filename with zero-padding (001, 002, etc.)
                    self.filename = f"recording_{self.number_of_video:03d}.avi"
                    self.filepath = os.path.join(self.output_directory, self.filename)
                    if not os.path.exists(self.filepath):
                        break  # Found unused filename
                    self.number_of_video += 1

                # Initialize VideoWriter with camera properties
                self.out = cv2.VideoWriter(self.filepath, self.fourcc, self.target_fps, 
                                         (self.frame_width, self.frame_height))
                
                if not self.out.isOpened():
                    print("Error: Failed to create video file for recording.")
                    self.start_recording = False  # Revert state on failure
                else:
                    print(f"Started recording to file: {self.filename}")

            else:
                # Stop recording and release file resources
                if self.out is not None:
                    self.out.release()  
                    self.out = None  
                    print("Recording stopped.")

    def start_work(self):
        """Main processing loop - the core of the application"""
        while True:
            # Read frame from camera 
            self.ret, self.frame = self.video_capture.read()
            if not self.ret:
                print("Error: Failed to capture frame.")
                break
            
            # Processing pipeline: effects → FPS calculation → UI overlay
            self.effect()     
            self.fps_()       
            self.output()      
            
            # Non-blocking key input detection 
            self.key = cv2.waitKey(1) & 0xFF  
            
            # Handle recording control based on keypress
            self.record_video()

            # If recording is active, write the current processed frame to file
           
            if self.start_recording and self.out is not None:
                self.out.write(cv2.cvtColor(self.vid_gray, cv2.COLOR_GRAY2BGR))
            
            # Exit condition - 'q' key pressed
            if self.key == ord('q'):  
                break
                
        # Cleanup resources when loop exits
        self.clear_memory()

    def clear_memory(self):
        """Release all resources and cleanup"""
        # Release video file if recording was active
        if self.out is not None:
            self.out.release()  
        
        # Release camera resource
        self.video_capture.release()
        
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        
        print("Program terminated.")

if __name__=="__main__":
    video = Video_Maker()
    video.start_work()