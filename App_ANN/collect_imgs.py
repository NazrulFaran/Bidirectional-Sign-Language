import os
import cv2

class DataCollector:
    def __init__(self):
        self.DATA_DIR = './data'
        self.dataset_size = 100
        self.window_name = 'Data Collection'
        self.setup_directories()
        self.cap = cv2.VideoCapture(0)
        self.setup_window()
        
    def setup_directories(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(self.DATA_DIR, exist_ok=True)
        
    def setup_window(self):
        """Initialize window properties"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 800, 600)
        
    def put_text(self, frame, text, position, font_scale=0.8, color=(0, 255, 0), thickness=2):
        """Helper function to put styled text on frame"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
        
    def put_centered_text(self, frame, text, y_offset=0, font_scale=0.8, color=(0, 255, 0), thickness=2):
        """Put centered text on frame"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] + text_size[1]) // 2 + y_offset
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)
        
    def draw_instruction_box(self, frame, title, instructions):
        """Draw a beautiful instruction box"""
        height, width = frame.shape[:2]
        box_height = 120
        box_y = 20
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (20, box_y), (width-20, box_y + box_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw border
        cv2.rectangle(frame, (20, box_y), (width-20, box_y + box_height), (0, 255, 0), 2)
        
        # Add text
        self.put_text(frame, title, (40, box_y + 35), font_scale=1.0, color=(0, 255, 255))
        self.put_text(frame, instructions, (40, box_y + 75), font_scale=0.7, color=(255, 255, 255))
    
    def flip_frame_horizontal(self, frame):
        """Flip frame horizontally for mirror effect"""
        return cv2.flip(frame, 1)
        
    def draw_capture_effect(self, frame, counter):
        """Visual effect when capturing an image"""
        # Flash effect
        if counter % 2 == 0:  # Alternate between flash and normal
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (255, 255, 255), -1)
            cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        
        # Draw red circle to indicate capture
        center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
        cv2.circle(frame, (center_x, center_y), 40, (0, 0, 255), 3)
        cv2.circle(frame, (center_x, center_y), 35, (0, 0, 255), -1)
        
        # Add capture count text
        self.put_centered_text(frame, f"{counter + 1}", y_offset=0, font_scale=1.2, color=(255, 255, 255))
        
    def select_class(self):
        """Step 1: Let user select class by pressing a key"""
        print('🎯 Press any key (A-Z or 0-9) to start collecting data for that class')
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # Flip frame horizontally for mirror effect
            frame = self.flip_frame_horizontal(frame)
                
            self.draw_instruction_box(
                frame, 
                "CLASS SELECTION", 
                "Press any letter (A-Z) or number (0-9) to choose your class"
            )
            
            cv2.imshow(self.window_name, frame)
            
            key = cv2.waitKey(25) & 0xFF  # Mask to get proper key code
            if key == 27:  # ESC key
                self.cleanup()
                exit()
                
            if key != 255:  # A key was pressed
                key_char = chr(key).upper()
                if key_char.isalnum():
                    print(f'✅ Selected class: {key_char}')
                    return key_char
                    
    def confirm_collection(self, class_name):
        """Step 2: Show confirmation before starting collection"""
        print(f'📸 Ready to collect data for class: {class_name}')
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # Flip frame horizontally for mirror effect
            frame = self.flip_frame_horizontal(frame)
                
            self.draw_instruction_box(
                frame,
                f"CLASS: {class_name}",
                f"Press 'Q' to start collecting {self.dataset_size} images | ESC to cancel"
            )
            
            # Add visual countdown/ready indicator
            cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2 + 50), 30, (0, 255, 0), 2)
            self.put_centered_text(frame, "READY", y_offset=50, color=(0, 255, 0))
            
            cv2.imshow(self.window_name, frame)
            
            key = cv2.waitKey(25) & 0xFF
            if key == ord('q'):
                return True
            elif key == 27:  # ESC
                return False
                
    def collect_images(self, class_name):
        """Step 3: Collect the actual images"""
        class_dir = os.path.join(self.DATA_DIR, class_name)
        os.makedirs(class_dir, exist_ok=True)
        
        print(f'🔄 Collecting {self.dataset_size} images for class: {class_name}')
        
        counter = 0
        while counter < self.dataset_size:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # Flip frame horizontally for mirror effect (what user sees)
            display_frame = self.flip_frame_horizontal(frame.copy())
            
            # Create progress bar
            progress = (counter + 1) / self.dataset_size
            bar_width = 400
            bar_height = 20
            bar_x = (display_frame.shape[1] - bar_width) // 2
            bar_y = display_frame.shape[0] - 50
            
            # Draw progress bar background
            cv2.rectangle(display_frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
            # Draw progress
            cv2.rectangle(display_frame, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
            # Draw border
            cv2.rectangle(display_frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 2)
            
            # Add progress text
            progress_text = f'{counter + 1}/{self.dataset_size} ({progress:.0%})'
            self.put_centered_text(display_frame, progress_text, y_offset=-30, font_scale=0.7, color=(255, 255, 255))
            
            # Add class name
            self.put_centered_text(display_frame, f'Class: {class_name}', y_offset=30, font_scale=0.8, color=(0, 255, 255))
            
            # Add capture effect (visual feedback when picture is taken)
            self.draw_capture_effect(display_frame, counter)
            
            # Show the display frame (flipped)
            cv2.imshow(self.window_name, display_frame)
            
            # Save the original frame (not flipped) to maintain consistency
            cv2.imwrite(os.path.join(class_dir, f'{counter:03d}.jpg'), frame)
            counter += 1
            
            cv2.waitKey(25)
            
        print(f'✅ Completed collecting {self.dataset_size} images for class: {class_name}')
        
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        
    def run(self):
        """Main execution function"""
        try:
            # Step 1: Select class
            class_name = self.select_class()
            
            # Step 2: Confirm collection
            if not self.confirm_collection(class_name):
                print('❌ Collection cancelled')
                return
                
            # Step 3: Collect images
            self.collect_images(class_name)
            
            print('🎉 Data collection completed successfully!')
            
        except Exception as e:
            print(f'❌ Error occurred: {e}')
        finally:
            self.cleanup()

# Run the application
if __name__ == "__main__":
    collector = DataCollector()
    collector.run()