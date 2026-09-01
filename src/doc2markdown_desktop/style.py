"""Dark-friendly application stylesheet."""

APP_STYLESHEET = """
QWidget { background: #171a21; color: #edf1f7; font-family: 'Segoe UI'; font-size: 10pt; }
QMainWindow { background: #171a21; }
QPushButton { background: #2e6eea; border: 0; border-radius: 6px; padding: 8px 14px;
  font-weight: 600; }
QPushButton:hover { background: #4380f0; }
QPushButton:disabled { background: #3b414d; color: #9aa4b2; }
QLineEdit, QTableWidget { background: #20252e; border: 1px solid #363e4b;
  border-radius: 5px; padding: 6px; }
QHeaderView::section { background: #252b35; border: 0; padding: 7px; font-weight: 600; }
QTableWidget { gridline-color: #363e4b; } QTableWidget::item { padding: 5px; }
#dropArea { background: #1d2635; border: 2px dashed #4d78c5; border-radius: 12px; }
#dropArea:hover { background: #22304a; border-color: #73a0ff; }
#dropTitle { font-size: 16pt; font-weight: 600; color: #e8efff; }
#dropSubtitle { font-size: 10pt; font-weight: 400; color: #aebbd0; }
#subtitle { color: #aeb7c5; } #message { color: #b9c6da; }
QProgressBar { border: 1px solid #3b4555; border-radius: 5px; text-align: center;
  background: #20252e; }
QProgressBar::chunk { background: #2e6eea; border-radius: 4px; }
"""
