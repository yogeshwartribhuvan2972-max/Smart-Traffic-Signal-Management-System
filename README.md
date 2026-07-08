# 🚦 Smart Traffic Signal Management System

An AI-powered adaptive traffic signal management system that uses YOLOv8, OpenCV, Flask, and dynamic traffic control logic to analyze traffic density and manage signal timings efficiently.

This project was developed as a Final Year B.Tech Project in Computer Science and Engineering (Artificial Intelligence & Machine Learning).

---

## 📌 Project Overview

Traditional traffic signal systems generally operate using fixed timing intervals, which may not adapt efficiently to changing traffic conditions.

The Smart Traffic Signal Management System aims to improve traffic management by analyzing vehicle density from multiple traffic video sources and dynamically assigning green signal durations.

The system processes traffic videos using YOLOv8 and OpenCV, counts vehicles lane-wise, and applies traffic control logic to determine signal priority and green signal duration.

A Flask-based web dashboard is used to monitor junctions, traffic lanes, vehicle counts, signal states, and timers.

---

## 🎯 Project Objectives

- Detect and count vehicles from traffic video feeds.
- Analyze lane-wise traffic density.
- Dynamically allocate green signal duration.
- Give priority to lanes with higher traffic density.
- Reduce unnecessary waiting time at traffic signals.
- Monitor multiple junctions through a web-based dashboard.
- Provide different traffic signal control modes.
- Implement emergency override logic as a prototype feature.

---

## ✨ Key Features

- 🚗 Vehicle Detection using YOLOv8
- 🎥 Traffic Video Processing using OpenCV
- 🚦 Adaptive Traffic Signal Timing
- 📊 Lane-wise Vehicle Counting
- 🛣️ Multi-Junction Traffic Monitoring
- 📹 12 Traffic Video Sources
- ⏱️ Dynamic Green Signal Duration
- ⚖️ Traffic Fairness and Waiting-Cycle Logic
- 🔴 Initial All-Red Safety Phase
- 🖥️ Flask-Based Web Dashboard
- 🎛️ Independent, Coordinated, and Manual Control Modes
- 🚑 Emergency Override Logic Prototype
- 📱 Multi-Camera and Junction Monitoring

---

## 🏙️ System Configuration

The system simulates and monitors three traffic junctions:

- Junction A
- Junction B
- Junction C

Each junction contains four traffic lanes:

- North
- South
- East
- West

Therefore, the complete system processes a total of 12 traffic video sources.

---

## 🧠 How the System Works

1. Traffic video feeds are provided as input to the system.

2. OpenCV reads and processes video frames.

3. YOLOv8 detects supported vehicle classes from each traffic lane.

4. The system calculates the number of vehicles present in each lane.

5. Traffic control logic compares lane-wise traffic density.

6. The lane with higher traffic demand is selected for signal priority.

7. Green signal duration is dynamically calculated based on vehicle count.

8. Minimum and maximum green time limits are applied.

9. Waiting-cycle and fairness logic help prevent continuous neglect of lower-density lanes.

10. Signal status, vehicle count, and timer information are displayed on the Flask web dashboard.

---

## ⏱️ Adaptive Signal Timing Logic

The project uses dynamic signal timing based on detected vehicle count.

The basic timing strategy includes:

- 1 Vehicle = 2 Seconds of Green Time
- Minimum Green Time = 5 Seconds
- Maximum Green Time = 110 Seconds

The system also applies lane priority and fairness logic to improve traffic flow management.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLOv8 | Vehicle detection |
| OpenCV | Video and frame processing |
| Flask | Web application and dashboard |
| HTML | Dashboard structure |
| CSS | Dashboard design |
| JavaScript | Dashboard interaction and updates |
| NumPy | Numerical operations |

---

## 📂 Project Structure

```text
Smart-Traffic-Signal-Management-System/
│
└── stm7/
    │
    ├── app.py
    ├── camera.py
    ├── core_logic.py
    ├── junctions_config.py
    ├── requirements.txt
    ├── run_scada.bat
    │
    ├── static/
    │   ├── script.js
    │   └── style.css
    │
    └── templates/
        └── index.html
```
---

## 📄 File Description

### `app.py`

Main Flask application responsible for running the web server, managing routes, streaming processed traffic frames, and providing traffic status information to the dashboard.

### `camera.py`

Handles traffic video processing and vehicle detection using YOLOv8 and OpenCV.

### `core_logic.py`

Contains the main traffic signal control logic, including signal priority, dynamic timing, and traffic management rules.

### `junctions_config.py`

Stores configuration details for junctions and traffic lanes.

### `templates/index.html`

Contains the main structure of the traffic monitoring dashboard.

### `static/style.css`

Contains styling and visual design for the web dashboard.

### `static/script.js`

Handles dashboard interactions and dynamic updates.

### `requirements.txt`

Contains the Python libraries required to run the project.

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yogeshwartribhuvan2972-max/Smart-Traffic-Signal-Management-System.git
```

### 2. Open the Project Directory

```bash
cd Smart-Traffic-Signal-Management-System/stm7
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Add Traffic Video Files

Add the required traffic video files inside a `videos` folder.

```text
videos/
├── A_north.mp4
├── A_south.mp4
├── A_east.mp4
├── A_west.mp4
├── B_north.mp4
├── B_south.mp4
├── B_east.mp4
├── B_west.mp4
├── C_north.mp4
├── C_south.mp4
├── C_east.mp4
└── C_west.mp4
```

### 5. Run the Application

```bash
python app.py
```

### 6. Open the Dashboard

Open the local Flask server address displayed in the terminal.

```text
http://127.0.0.1:5000
```

---
---

## 📸 Project Screenshots

### 🚦 Traffic Control Room

![Traffic Control Room](controlroom.png)

### 🔄 Coordinated Mode

![Coordinated Mode](coordinate%20mode.png)

### ⚡ Independent Mode

![Independent Mode](independent%20mode.png)
```
---
## 🎥 Project Demo

A demonstration of the complete working Smart Traffic Signal Management System is available on Google Drive.

[▶️ View Project Demo and Files](https://drive.google.com/drive/folders/12MxfN-IMHDk0aalXQ8nYp0s3n9G8sp1o)

---

## 🚑 Emergency Override Prototype

The project includes emergency override logic as a prototype traffic-control feature.

The current implementation focuses primarily on standard vehicle detection and adaptive traffic signal management.

A specialized emergency vehicle detection model can be integrated in future versions for more reliable ambulance and fire-truck detection.

---

## 📈 Future Improvements

- Real-time CCTV camera integration
- Specialized emergency vehicle detection model
- Traffic congestion prediction using Machine Learning
- Cloud-based traffic data storage
- Advanced traffic analytics dashboard
- Real-time database integration
- IoT-based physical traffic signal integration
- Mobile application for traffic monitoring
- Deployment on cloud infrastructure

---

## 🎓 Academic Project

This project was developed as a Final Year B.Tech Project in:

**Computer Science and Engineering (Artificial Intelligence & Machine Learning)**

The project demonstrates the practical application of:

- Artificial Intelligence
- Computer Vision
- Python Programming
- Web Development
- Traffic Management Logic
- Real-Time Monitoring Concepts

---

## 👨‍💻 Author

**Yogeshwar Tribhuvan**

Aspiring Data Analyst | Python | SQL | Excel | Power BI | Data Visualization | Machine Learning

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a star.
