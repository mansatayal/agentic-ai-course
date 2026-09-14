import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key is missing")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"


# job description:
jd = """
Role Overview

This is a hands-on computer vision and applied ML role. Defects get described to you in
plain, non-technical language by people who aren't vision engineers. Your job is to turn
each one into a real vision problem: what camera view is needed, what evidence proves the
defect, what technique to use, and when the honest answer is "we can't inspect this." You
then take the ones worth building all the way through to a working, evaluated model running
against a real accuracy target.

Datasets come unlabelled. Defect lists come as plain descriptions, not vision problems.
Building both is part of the job. You will also write the Python services that carry frames,
detections, and results through the pipeline, so this is more than model work.

Key Responsibilities

Problem Definition & Feasibility

Translate defect descriptions given in plain, non-technical language into a defined vision
problem: required camera view, evidence needed, and technique
Identify and document cases where a defect cannot be reliably detected from the available imagery, with clear reasoning
Define success criteria for each defect class before any model development begins
Data & Annotation Operations

Own annotation guidelines and class definitions; administer the annotation platform
Review annotation quality through inter-annotator agreement checks and resolve edge cases
Maintain dataset versioning and enforce a held-out evaluation split with no leakage between training and test data
Model Development

Develop detection, segmentation, oriented-box, keypoint, and OCR models as required; no single architecture covers every defect type
Define per-class operating thresholds rather than a single global cutoff
Conduct rigorous evaluation on held-out data and maintain a documented failure-mode analysis alongside accuracy metrics
Edge Deployment

Export and quantise models (ONNX / TensorRT) for edge GPU inference
Establish latency, memory, and throughput budgets based on real frame rates and image sizes
Implement tiled inference for high-resolution frames that exceed single-pass model capacity
Pipeline Engineering

Develop and maintain production Python services covering frame ingestion, object tracking across a pass, event publishing, and result formatting
Work within an asynchronous, typed, and tested codebase using message queues and Docker
Read, extend, and debug existing services in addition to building new ones
Field Reality

Work with real-world images affected by motion blur, occlusion, poor lighting, rain, and dust; design systems that degrade predictably rather than fail silently
Undertake periodic site visits to assess real deployment conditions
Required Skills

Production-quality Python: typing, tests, packaging, git, and code that others can pick up and maintain
PyTorch, and at least one detection or segmentation model you took from data to a working,evaluated result
OpenCV and classical computer vision: geometry, calibration, colour, blur, thresholding,and the judgement to choose between classical and deep-learning approachesper-class precision/recall, a list of failure modes
Ability to design an evaluation protocol before training anything: a held-out split,
Comfortable reading and modifying code you didn't type yourself, including AI-assisted code
Docker and basic Linux
Good to Have

OCR / scene-text recognition (PaddleOCR, docTR, TrOCR, CRNN or similar)
Model export and inference optimisation (ONNX, TensorRT, quantisation)
Experience administering an annotation tool (CVAT or similar)
Basic video and codec knowledge (FFmpeg, hardware encoding)
Industrial/GigE Vision cameras, GenICam
Self-supervised pretraining (DINOv2, MAE) or anomaly detection (PatchCore)
Multi-object tracking across frames
Message queues (MQTT/AMQP) or event-driven services
Any exposure to industrial inspection or manufacturing QA
Education

B.E. / B.Tech in Computer Science, Electronics & Communication, Electrical Engineering,
or a closely related discipline.

What We Value

End-to-end ownership, from a rough defect description to a deployed, measured model
Claims backed by evidence and measurement
Full accountability for every line of code you submit
A clean handover: documented assumptions, a repeatable evaluation, code someone else can pick up
Pay: From ₹600,000.00 per year

Benefits:

Flexible schedule
Health insurance
Willingness to travel:

25% (Preferred)
Work Location: In person
"""

# resume
resume = """
MANSA AGGARWAL
New Delhi, India | 9540008398 | mansa.aggarwal.work@gmail.com | https://github.com/mansatayal | linkedin.com/in/mansaaggarwal-874a05269
SUMMARY
Computer Science graduate focused on the intersection of AI/ML and embedded systems. Experience building realtime computer vision applications and WiFi-connected embedded hardware, with a track record of shipping complete,
working projects end-to-end.
EDUCATION
B.Tech, Computer Science — M.E.R.I. College of Engineering & Technology (MDU)
PROJECTS
Gesture App | https://github.com/mansatayal/gesture-app
• Built a real-time hand gesture recognition app in Python using OpenCV, MediaPipe, and Pygame, supporting
three interactive modes from a single webcam pipeline.
• Designed a gesture-controlled drawing canvas (Draw mode) with adjustable brush sizes, an eraser, and a timed
color-selection system using a 7-swatch palette.
• Built a presentation controller (Count mode) that detects finger-count gestures across two hands simultaneously
and maps them to slide navigation (next/previous/start/stop) via PyAutoGUI, with hold-based gesture confirmation
and audio feedback.
• Optimized MediaPipe inference (model_complexity=0) for real-time performance and documented model
limitations around hand orientation in the project README.
ESP32 Weather Dashboard | https://github.com/mansatayal/esp32-weather-dashboard
• Built a self-hosted IoT dashboard on the ESP32, reading live temperature and humidity from a DHT11 sensor and
serving readings via an on-device WiFi web server.
• Handled end-to-end hardware bring-up: sensor wiring, firmware in Arduino C++, and driver/board configuration
troubleshooting.
Traffic Light Controller with LED Matrix Countdown | https://github.com/mansatayal/traffic-light-arduino
• Built a traffic signal simulator in Arduino C++ with a synced 8x8 LED matrix countdown timer for each light state,
including a custom digit bitmap font rendered via MAX7219 driver.
Machine Learning Coursework | https://github.com/mansatayal/ml-coursework
• Built and evaluated ML models across regression, classification, and deep learning tasks — including a CNN for
image classification (~83% accuracy) and ANN-based multi-class classification — using Python, scikit-learn, and
TensorFlow/Keras.
SKILLS
Languages: Python, C++
AI / ML: OpenCV, MediaPipe, TensorFlow, Keras, scikit-learn
Embedded / Hardware: Arduino, ESP32, OpenWrt (router firmware), sensor integration
Tools: Git, GitHub, VS Code, Pygame, PyAutoGUI
Coursework: Data Structures & Algorithms, Discrete Mathematics, Machine Learning
"""


# general function to just call the llm
def call_llm(system_prompt, user_prompt):
    sys_msg = {"role" : "system", "content" : system_prompt}
    user_msg = {"role" : "user", "content" : user_prompt}

    messages = [sys_msg, user_msg]

    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer



# resume skill extarction
def extract_resume_skills(resume):
    print("extracting skills from the resume ------------------ \n")
    system_prompt = """
    You're an HR assistant.
    You're responsible to extract reliable skills from the candidate's resume.

    important:
    1. make sure you're not assuming or creating information on your own only reply with whatever's given.
    2. if any links are provided check if they work correctly or not 
    3. only return the skills no other information.
    
    return in a pointwise format.
    """

    user_prompt = f"""
    Extract skills from the given resume {resume}
    """

    return call_llm(system_prompt, user_prompt)


# extract skills from the job description
def extract_jd_skills(jd):
    print("extracting skills from the jd ------------------ \n")
    system_prompt = """
    You're an HR assistant.
    You're responsible to extract reliable skills from the job description provided.

    important:
    1. make sure you're not assuming or creating information on your own only reply with whatever's given. 
    2. only return the skills no other information.

    return in a pointwise format.
    """

    user_prompt = f"""
    Extract skills from the given job description {jd}
    """

    return call_llm(system_prompt, user_prompt)




# match the resume skills with job description and return a score
def match(candidate, job_description):
    print("matching jd and candidate ------------------ \n")
    system_prompt = """
    you are a professional HR assistant. Compare the skills of the candidate with the skills required in the job description and produce a final score between 1 to 100 with a short summary about the candidate and why that score.
    important: only generate a short summary and a score nothing else
    """
    user_prompt = f"""
    compare and match the skills in job description{job_description} and candidate {candidate}
    """

    return call_llm(system_prompt, user_prompt)


candidate = extract_resume_skills(resume)
print("candidate's skills: \n", candidate)
sleep(3)

job_description = extract_jd_skills(jd)
print("required skills: \n", job_description)
sleep(3)

score = match(candidate, job_description)
print(score)
sleep(3)


