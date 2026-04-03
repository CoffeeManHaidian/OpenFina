from PySide6.QtGui import QColor, QPalette


GOOGLE_BLUE = "#1a73e8"
GOOGLE_BLUE_HOVER = "#1765cc"
GOOGLE_BLUE_PRESSED = "#1558b0"
GOOGLE_RED = "#ea4335"
GOOGLE_YELLOW = "#fbbc04"
GOOGLE_GREEN = "#34a853"
SURFACE = "#ffffff"
SURFACE_ALT = "#f8f9fa"
SURFACE_SUBTLE = "#f1f3f4"
OUTLINE = "#dadce0"
OUTLINE_STRONG = "#c7cdd3"
TEXT = "#202124"
TEXT_SUBTLE = "#5f6368"


def apply_material_app(app):
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(SURFACE_ALT))
    palette.setColor(QPalette.WindowText, QColor(TEXT))
    palette.setColor(QPalette.Base, QColor(SURFACE))
    palette.setColor(QPalette.AlternateBase, QColor(SURFACE_SUBTLE))
    palette.setColor(QPalette.Text, QColor(TEXT))
    palette.setColor(QPalette.Button, QColor(SURFACE))
    palette.setColor(QPalette.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.Highlight, QColor(GOOGLE_BLUE))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)


def material_widget_style():
    return f"""
    QWidget {{
        background-color: {SURFACE_ALT};
        color: {TEXT};
        font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
        font-size: 13px;
    }}
    QLabel {{
        color: {TEXT};
        background: transparent;
    }}
    QLineEdit, QComboBox, QDateTimeEdit, QSpinBox {{
        background-color: {SURFACE};
        border: 1px solid {OUTLINE};
        border-radius: 10px;
        padding: 8px 12px;
        selection-background-color: {GOOGLE_BLUE};
    }}
    QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus, QSpinBox:focus {{
        border: 1px solid {GOOGLE_BLUE};
        background-color: #fcfdff;
    }}
    QPushButton {{
        background-color: {SURFACE};
        border: 1px solid {OUTLINE};
        border-radius: 10px;
        padding: 9px 16px;
        color: {TEXT};
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {SURFACE_SUBTLE};
        border-color: {OUTLINE_STRONG};
    }}
    QPushButton:pressed {{
        background-color: #e8f0fe;
        border-color: {GOOGLE_BLUE};
    }}
    QTableWidget, QTreeWidget {{
        background-color: {SURFACE};
        border: 1px solid {OUTLINE};
        border-radius: 14px;
        gridline-color: {OUTLINE};
        selection-background-color: #e8f0fe;
        selection-color: {TEXT};
    }}
    QHeaderView::section {{
        background-color: {SURFACE_SUBTLE};
        color: {TEXT_SUBTLE};
        border: none;
        border-bottom: 1px solid {OUTLINE};
        padding: 8px;
        font-weight: 600;
    }}
    QCheckBox {{
        spacing: 8px;
        color: {TEXT_SUBTLE};
    }}
    QScrollBar:vertical {{
        width: 10px;
        background: transparent;
        margin: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: #c2c7cf;
        border-radius: 5px;
        min-height: 28px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
    QScrollBar:horizontal, QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: transparent;
        border: none;
        height: 0px;
    }}
    """


def material_dialog_style():
    return material_widget_style() + f"""
    QDialog {{
        background-color: {SURFACE_ALT};
    }}
    QDialogButtonBox QPushButton {{
        min-width: 88px;
    }}
    """


def login_widget_style():
    return f"""
    QWidget {{
        background-color: {SURFACE_ALT};
        color: {TEXT};
        font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
    }}
    #leftWidget {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #e8f0fe, stop:0.55 #d2e3fc, stop:1 #f8fbff);
        border-top-left-radius: 28px;
        border-bottom-left-radius: 28px;
    }}
    #rightWidget {{
        background-color: {SURFACE};
        border-top-right-radius: 28px;
        border-bottom-right-radius: 28px;
    }}
    #titleLb {{
        font-size: 32px;
        font-weight: 700;
        color: {TEXT};
        qproperty-alignment: 'AlignCenter';
    }}
    #subtitleLb {{
        font-size: 15px;
        color: {TEXT_SUBTLE};
        qproperty-alignment: 'AlignCenter';
        margin-top: 8px;
    }}
    #brandTitle {{
        font-size: 30px;
        font-weight: 700;
        color: {TEXT};
    }}
    #brandSubtitle {{
        font-size: 16px;
        color: {TEXT_SUBTLE};
        line-height: 1.4;
    }}
    #versionBadge {{
        color: {GOOGLE_BLUE};
        background-color: rgba(26, 115, 232, 0.12);
        border-radius: 14px;
        padding: 6px 12px;
        font-weight: 600;
    }}
    #formCard {{
        background-color: {SURFACE};
        border: 1px solid {OUTLINE};
        border-radius: 24px;
    }}
    QLabel#fieldLabel {{
        color: {TEXT_SUBTLE};
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.2px;
    }}
    QLineEdit {{
        background-color: {SURFACE};
        border: 1px solid {OUTLINE};
        border-radius: 12px;
        padding: 12px 14px;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border-color: {GOOGLE_BLUE};
        background-color: #fcfdff;
    }}
    QPushButton {{
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid {OUTLINE};
        background-color: {SURFACE};
        color: {TEXT};
    }}
    QPushButton#loginBtn, QPushButton#confirmBtn {{
        background-color: {GOOGLE_BLUE};
        border-color: {GOOGLE_BLUE};
        color: white;
    }}
    QPushButton#loginBtn:hover, QPushButton#confirmBtn:hover {{
        background-color: {GOOGLE_BLUE_HOVER};
        border-color: {GOOGLE_BLUE_HOVER};
    }}
    QPushButton#loginBtn:pressed, QPushButton#confirmBtn:pressed {{
        background-color: {GOOGLE_BLUE_PRESSED};
        border-color: {GOOGLE_BLUE_PRESSED};
    }}
    QPushButton#cancelBtn {{
        background-color: transparent;
    }}
    QPushButton#registerBtn, QPushButton#forgetBtn, QPushButton#switchBtn {{
        background-color: transparent;
        border: none;
        color: {GOOGLE_BLUE};
        padding: 4px 6px;
        font-weight: 600;
    }}
    QPushButton#registerBtn:hover, QPushButton#forgetBtn:hover, QPushButton#switchBtn:hover {{
        background-color: rgba(26, 115, 232, 0.08);
        border-radius: 8px;
    }}
    QCheckBox {{
        color: {TEXT_SUBTLE};
        spacing: 8px;
    }}
    """


def chrome_main_window_style():
    return f"""
    #ChromeStyleMainWindow {{
        background-color: {SURFACE_ALT};
    }}
    #widget {{
        background-color: {SURFACE_ALT};
        border-radius: 18px;
    }}
    #titleBar {{
        background-color: transparent;
        border-top-left-radius: 18px;
        border-top-right-radius: 18px;
        border-bottom: 1px solid {OUTLINE};
    }}
    #titleInfoWidget, #windowControls, #leftBar, #MainWidget, #RightBar, #contentContainer {{
        background-color: transparent;
    }}
    #windowTitleLabel {{
        font-size: 18px;
        font-weight: 700;
        color: {TEXT};
    }}
    #windowContextLabel {{
        font-size: 12px;
        color: {TEXT_SUBTLE};
    }}
    #btn_min, #btn_max, #btn_close {{
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        color: {TEXT_SUBTLE};
        font-size: 13px;
        font-weight: 700;
    }}
    #btn_min:hover, #btn_max:hover {{
        background-color: #e8eaed;
        color: {TEXT};
    }}
    #btn_close:hover {{
        background-color: #fce8e6;
        color: {GOOGLE_RED};
    }}
    #leftBar {{
        border-right: 1px solid {OUTLINE};
    }}
    #RightBar {{
        border-left: 1px solid {OUTLINE};
    }}
    #bookmarksTitle, #lb_Sub, #lb_Detail {{
        color: {TEXT_SUBTLE};
        font-size: 12px;
        font-weight: 700;
        padding: 0 0 8px 0;
    }}
    #leftBar QPushButton, #ladgerWidget QPushButton, #detCertificate QPushButton, #quickActions QPushButton, #detLadger QPushButton {{
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 12px;
        color: {TEXT};
        font-size: 14px;
        font-weight: 600;
        text-align: left;
        padding: 11px 14px;
    }}
    #leftBar QPushButton:hover, #ladgerWidget QPushButton:hover, #detCertificate QPushButton:hover, #quickActions QPushButton:hover, #detLadger QPushButton:hover {{
        background-color: #e8f0fe;
        color: {GOOGLE_BLUE};
    }}
    #leftBar QPushButton:pressed, #ladgerWidget QPushButton:pressed, #detCertificate QPushButton:pressed {{
        background-color: #d2e3fc;
    }}
    #wgt_SubFunc, #wgt_DetailFunc, #subHome, #ladgerWidget, #reportWidget, #detailHome, #detCertificate, #detLadger {{
        background-color: transparent;
    }}
    #welcomeLabel {{
        color: {TEXT};
        font-size: 28px;
        font-weight: 700;
    }}
    #subDescription, #detailHomeLabel {{
        color: {TEXT_SUBTLE};
        font-size: 13px;
    }}
    #lineEdit_2 {{
        background-color: {SURFACE};
        border: 1px solid {OUTLINE};
        border-radius: 12px;
        padding: 12px 14px;
    }}
    QSplitter::handle {{
        background-color: {OUTLINE};
    }}
    QSplitter::handle:hover {{
        background-color: {GOOGLE_BLUE};
    }}
    """
