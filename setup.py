from setuptools import setup
import os

package_name = "speech_to_text"

# Helper function to gather all files, including from subdirectories
def recursive_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            # Compute relative path to preserve directory structure
            relative_path = os.path.relpath(full_path, directory)
            file_paths.append((os.path.join("share", package_name, directory, os.path.dirname(relative_path)), [full_path]))
    return file_paths

# Collect all files from the model directory
model_files = recursive_files("models/vosk-model-small-en-us-0.15")

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ] + model_files,  # Add collected model files
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="your_name",
    maintainer_email="your_email@example.com",
    description="A ROS2 node for speech-to-text",
    license="Apache License 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "speech_to_text_node = speech_to_text.speech_to_text_node:main",
        ],
    },
)

