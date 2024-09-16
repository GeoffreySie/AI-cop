import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit

class CyberSecurityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Cybersecurity Anomaly Detection App")
        self.setGeometry(200, 200, 500, 400)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Label to display instructions
        self.label = QLabel("Upload a CSV file for anomaly detection:")
        layout.addWidget(self.label)
        
        # Button to upload file
        self.upload_button = QPushButton("Upload CSV File")
        self.upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.upload_button)
        
        # TextEdit to display the result
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        # Set layout for the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def open_file_dialog(self):
        # Open file dialog to select CSV file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)
        
        if file_path:
            # Call function to detect anomalies via Flask API
            self.detect_anomalies(file_path)
    
    def detect_anomalies(self, file_path):
        try:
            # Make POST request to Flask API
            url = "http://127.0.0.1:5000/upload"
            with open(file_path, "rb") as file:
                response = requests.post(url, files={"file": file})
            
            if response.status_code == 200:
                result = response.json()
                self.result_text.setText(f"Anomalies Detected: {result['anomalies_detected']}\n"
                                         f"Total Records: {result['total_records']}")
            else:
                self.result_text.setText(f"Error: {response.json().get('error', 'Unknown error')}")
        
        except Exception as e:
            self.result_text.setText(f"Error: {str(e)}")

# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CyberSecurityApp()
    mainWindow.show()
    sys.exit(app.exec_())
