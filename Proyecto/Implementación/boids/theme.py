"""Dark theme stylesheet for the dashboard."""

DARK_STYLESHEET = """
QWidget {
    background-color: #12141a;
    color: #c8d0dc;
    font-family: "Segoe UI", "DejaVu Sans", Arial, sans-serif;
    font-size: 12px;
}
QMainWindow, QSplitter {
    background-color: #0c0e13;
}
QGroupBox {
    border: 1px solid #2a2f3a;
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 8px;
    background-color: #161922;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 6px;
    color: #5fd0e0;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton {
    background-color: #1d2330;
    border: 1px solid #2f3a4d;
    border-radius: 5px;
    padding: 6px 10px;
    color: #d6e2ef;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #25304a;
    border-color: #3f6fa0;
}
QPushButton:pressed {
    background-color: #16324a;
}
QPushButton:disabled {
    color: #5a626f;
    background-color: #161a22;
    border-color: #232833;
}
QLabel[metricValue="true"] {
    color: #5fd0e0;
}
QSlider::groove:horizontal {
    height: 5px;
    background: #232a36;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #2f7fa8;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #5fd0e0;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #8be7f5;
}
QFrame[frameShape="4"] {  /* HLine */
    color: #2a2f3a;
}
QStatusBar {
    background: #0c0e13;
    color: #7a8494;
}
QScrollArea {
    border: none;
}
"""
