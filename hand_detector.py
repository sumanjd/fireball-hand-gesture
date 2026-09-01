import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    """Detects hand pose and tracks hand gestures"""
    
    def __init__(self, static_image_mode=False, max_num_hands=2, confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=confidence,
            min_tracking_confidence=confidence
        )
        self.previous_state = None
        
    def detect(self, frame):
        """
        Detect hands in frame
        Returns: list of hand data with landmarks and info
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        hands_data = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, 
                results.multi_handedness
            ):
                hand_info = {
                    'landmarks': hand_landmarks,
                    'handedness': handedness.classification[0].label,
                    'confidence': handedness.classification[0].score,
                    'positions': self._get_hand_positions(hand_landmarks, frame)
                }
                hands_data.append(hand_info)
        
        return hands_data, results
    
    def _get_hand_positions(self, landmarks, frame):
        """Extract hand landmark positions in pixel coordinates"""
        h, w, c = frame.shape
        positions = {}
        
        for idx, landmark in enumerate(landmarks.landmark):
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            z = landmark.z
            positions[idx] = {'x': x, 'y': y, 'z': z}
        
        return positions
    
    def get_hand_center(self, hand_data):
        """Get center point of hand (palm center)"""
        positions = hand_data['positions']
        palm_landmarks = [0, 5, 9, 13, 17]  # Wrist and finger bases
        
        x_coords = [positions[i]['x'] for i in palm_landmarks]
        y_coords = [positions[i]['y'] for i in palm_landmarks]
        
        center_x = int(np.mean(x_coords))
        center_y = int(np.mean(y_coords))
        
        return (center_x, center_y)
    
    def is_hand_open(self, hand_data, threshold=0.05):
        """
        Detect if hand is open (palm facing camera)
        Uses distance between fingertips and palm center
        """
        positions = hand_data['positions']
        
        # Fingertip landmarks
        fingertips = [4, 8, 12, 16, 20]  # Thumb, index, middle, ring, pinky
        palm_center = self.get_hand_center(hand_data)
        
        distances = []
        for tip in fingertips:
            dx = positions[tip]['x'] - palm_center[0]
            dy = positions[tip]['y'] - palm_center[1]
            dist = np.sqrt(dx**2 + dy**2)
            distances.append(dist)
        
        # Hand is open if fingertips are spread out
        avg_distance = np.mean(distances)
        return avg_distance > 30  # Pixel threshold
    
    def detect_throw_gesture(self, hand_data, prev_hand_data):
        """
        Detect throwing gesture (quick hand acceleration)
        Returns: True if throw detected, velocity vector
        """
        if prev_hand_data is None:
            return False, (0, 0)
        
        curr_center = self.get_hand_center(hand_data)
        prev_center = self.get_hand_center(prev_hand_data)
        
        # Calculate velocity
        vx = (curr_center[0] - prev_center[0]) * 2  # Amplify velocity
        vy = (curr_center[1] - prev_center[1]) * 2
        
        velocity = np.sqrt(vx**2 + vy**2)
        
        # Throw detected if hand moves quickly (velocity > threshold)
        throw_threshold = 15
        is_throw = velocity > throw_threshold
        
        return is_throw, (vx, vy)
    
    def draw_hand(self, frame, hand_data, draw_landmarks=True):
        """Draw hand landmarks on frame"""
        if draw_landmarks:
            landmarks = hand_data['landmarks']
            h, w, c = frame.shape
            
            # Draw circles at each landmark
            for position in hand_data['positions'].values():
                cv2.circle(
                    frame, 
                    (position['x'], position['y']), 
                    4, 
                    (0, 255, 0), 
                    -1
                )
        
        return frame
    
    def release(self):
        """Release resources"""
        self.hands.close()


class HandGestureTracker:
    """Tracks hand gestures over time"""
    
    def __init__(self, history_size=5):
        self.history = []
        self.history_size = history_size
        self.throwing = False
        self.throw_velocity = (0, 0)
    
    def update(self, hand_data):
        """Update tracking history"""
        self.history.append(hand_data)
        if len(self.history) > self.history_size:
            self.history.pop(0)
    
    def get_hand_velocity(self):
        """Get current hand velocity"""
        if len(self.history) < 2:
            return (0, 0)
        
        latest = self.history[-1]
        previous = self.history[-2]
        
        latest_pos = (latest['positions'][9]['x'], latest['positions'][9]['y'])
        prev_pos = (previous['positions'][9]['x'], previous['positions'][9]['y'])
        
        vx = (latest_pos[0] - prev_pos[0])
        vy = (latest_pos[1] - prev_pos[1])
        
        return (vx, vy)
