import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vosk import Model, KaldiRecognizer
import pyaudio
import os
from ament_index_python.packages import get_package_share_directory
import json



class SpeechToTextNode(Node):
    def __init__(self):
        super().__init__("speech_to_text_node")
        self.publisher_ = self.create_publisher(String, "speech_to_text", 10)

        # Get the model path dynamically
        package_share_directory = get_package_share_directory("speech_to_text")        
        #model_path = os.path.join(package_share_directory, "models", "vosk-model-small-sv-rhasspy-0.15")
        model_path = os.path.join(package_share_directory, "models", "vosk-model-small-en-us-0.15")


        self.get_logger().info(f"Resolved model path: {model_path}")


        # Load Vosk model
        self.get_logger().info(f"Loading Vosk model from: {model_path}")
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        #self.recognizer = KaldiRecognizer(self.model, 16000, None)

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=4000)
                                      
                                      
        self.stream.start_stream()

        # Start the speech-to-text loop
        self.get_logger().info("Speech-to-Text Node has started.")
        self.timer = self.create_timer(0.1, self.process_audio)

    def process_audio(self):
        # Read data from the microphone
        data = self.stream.read(4000, exception_on_overflow=False)

        # Perform speech recognition
        if self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.Result())
            text = result.get("text", "")
            if text:
                self.get_logger().info(f"Recognized text: {text}")

                # Publish the recognized text
                msg = String()
                msg.data = text
                self.publisher_.publish(msg)

    def destroy_node(self):
        # Stop audio stream and release resources
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SpeechToTextNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Speech-to-Text Node...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

