import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtWidgets import QApplication

from ui.login import AutoWidget, LoginWidget, clear_settings, load_settings
from utils.logger import get_logger, install_global_exception_logger, log_system_info
from utils.theme import apply_material_app

logger = get_logger()


def create_start_window():
    if load_settings():
        try:
            return AutoWidget()
        except Exception:
            logger.exception("自动登录初始化失败，回退普通登录")
            clear_settings()
            return LoginWidget()
    return LoginWidget()


def main():
    log_system_info(logger)
    install_global_exception_logger(logger)

    app = QApplication([])
    apply_material_app(app)
    window = create_start_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
