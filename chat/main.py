import random
from agents.god import do
from pynput import keyboard
import asyncio
from qasync import QEventLoop  # Import QEventLoop for asyncio integration with PyQt

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy, QDesktopWidget, QSizeGrip
)
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize
from PyQt5.QtGui import QColor, QFont, QPainter, QBrush, QPen, QIcon, QPixmap, QFontMetrics

# --- Constants ---
APP_NAME = "PyQt AI Chat"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
ICON_SIZE = 60
# Max pixels mouse can move during press/release to be considered a click
CLICK_MOVE_THRESHOLD = 5

# Using darker color scheme as requested
DARK_BACKGROUND = "#000000"  # Black background
DARK_WIDGET_BACKGROUND = "#1D1616"  # Very dark widget background
TEXT_COLOR = "#e0e0e0"  # Slightly off-white for better readability
USER_BUBBLE_COLOR = "#0c4a6e"  # Darker blue for user messages
AI_BUBBLE_COLOR = "#212121"  # Darker gray for AI messages
ACCENT_COLOR = "#0284c7"  # More vibrant accent color
BORDER_RADIUS = 12
SHADOW_COLOR = QColor(0, 0, 0, 100)  # Stronger shadow

# --- Helper: Chat Bubble Widget (Enhanced) ---


class ChatBubble(QWidget):
    def __init__(self, text, is_user, parent=None):
        super().__init__(parent)
        self.is_user = is_user

        # Create main layout with proper margins
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 2, 5, 2)
        self.layout.setSpacing(0)

        # Text content
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setFont(QFont("Segoe UI", 10))

        # Calculate optimal width based on text content
        font_metrics = QFontMetrics(self.label.font())
        text_width = min(font_metrics.horizontalAdvance(
            text) + 30, int(WINDOW_WIDTH * 0.65))
        text_width = max(text_width, 80)  # Minimum width

        self.label.setMinimumWidth(text_width)
        self.label.setMaximumWidth(int(WINDOW_WIDTH * 0.65))

        bubble_color = USER_BUBBLE_COLOR if is_user else AI_BUBBLE_COLOR
        text_color = TEXT_COLOR

        self.label.setStyleSheet(f"""
            background-color: {bubble_color};
            color: {text_color};
            border-radius: {BORDER_RADIUS - 2}px;
            padding: 8px 12px;
        """)

        # Add shadow effect to the bubble
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(1, 1)
        self.label.setGraphicsEffect(shadow)

        # Position the bubble based on sender
        if is_user:
            self.layout.addStretch(1)
            self.layout.addWidget(self.label)
            self.layout.setContentsMargins(20, 2, 5, 2)  # Add right margin
        else:
            self.layout.addWidget(self.label)
            self.layout.addStretch(1)
            self.layout.setContentsMargins(5, 2, 20, 2)  # Add left margin

        self.adjustSize()

# --- Floating Icon Widget (Fixed Click/Drag) ---


class FloatingIcon(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(ICON_SIZE, ICON_SIZE)

        self._drag_offset = QPoint()  # For dragging calculation
        self._mouse_press_pos = QPoint()  # To detect click vs drag
        self._is_dragging = False  # State flag

        # Visual representation with gradient and rounded background for text
        self.label = QLabel("AI", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.label.setGeometry(0, 0, ICON_SIZE, ICON_SIZE)
        self.label.setStyleSheet(f"""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                            stop:0 {ACCENT_COLOR}, stop:1 #064e7c);
            color: {TEXT_COLOR};
            border-radius: {ICON_SIZE // 2}px; /* Make it circular */
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(SHADOW_COLOR)
        shadow.setOffset(2, 2)
        self.label.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = event.globalPos() - self.pos()
            self._mouse_press_pos = event.globalPos()
            self._is_dragging = False
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            moved_distance = (event.globalPos() -
                              self._mouse_press_pos).manhattanLength()
            if moved_distance > CLICK_MOVE_THRESHOLD:
                self._is_dragging = True
            self.move(event.globalPos() - self._drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self._is_dragging:
                self.clicked.emit()
            self._is_dragging = False
            self._mouse_press_pos = QPoint()
            event.accept()

# --- Main Chat Window (Enhanced) ---


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = QPoint()
        self.is_minimized_to_icon = False
        self.typing_animation_timer = QTimer(self)
        self.typing_dots_count = 0
        self.last_position = QPoint()
        self.is_maximized = False
        self.normal_geometry = None
        self.resizing = False
        self.resize_edge = None

        # Set window attributes to keep it visible across virtual desktops
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        # Linux-specific attribute to keep across desktops
        self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop, True)

        self.init_ui()
        self.create_floating_icon()
        # Add hotkey setup
        self.setup_hotkey()

        # Center window initially
        self.center_on_screen()
        self.last_position = self.pos()

    def center_on_screen(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def init_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self._initial_size = QSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.resize(self._initial_size)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.container_frame = QFrame(self)
        self.container_frame.setObjectName("containerFrame")
        self.container_frame.setStyleSheet(f"""
            #containerFrame {{
                background-color: {DARK_BACKGROUND};
                border-radius: {BORDER_RADIUS}px;
                border: 1px solid #3a3a3a;
            }}
        """)
        self.main_layout.addWidget(self.container_frame)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(SHADOW_COLOR)
        shadow.setOffset(0, 3)
        self.container_frame.setGraphicsEffect(shadow)

        self.content_layout = QVBoxLayout(self.container_frame)
        self.content_layout.setContentsMargins(8, 8, 8, 8)
        self.content_layout.setSpacing(8)

        # --- Custom Title Bar ---
        self.title_bar = QFrame(self)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("background-color: transparent;")
        title_bar_layout = QHBoxLayout(self.title_bar)
        title_bar_layout.setContentsMargins(10, 0, 5, 0)
        title_bar_layout.setSpacing(5)

        title_label = QLabel(APP_NAME, self.title_bar)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setStyleSheet(
            f"color: #cccccc; background-color: transparent;")

        self.minimize_button = QPushButton("—", self.title_bar)
        self.minimize_button.setFixedSize(24, 24)
        self.minimize_button.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.minimize_button.setCursor(Qt.PointingHandCursor)
        self.minimize_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_WIDGET_BACKGROUND}; color: {TEXT_COLOR};
                border-radius: 12px; border: 1px solid #444444;
            }}
            QPushButton:hover {{ background-color: #555555; }}
            QPushButton:pressed {{ background-color: #404040; }}
        """)
        self.minimize_button.clicked.connect(self.toggle_minimize)

        # Remove the square maximize button as requested

        self.close_button = QPushButton("✕", self.title_bar)
        self.close_button.setFixedSize(24, 24)
        self.close_button.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_WIDGET_BACKGROUND}; color: {TEXT_COLOR};
                border-radius: 12px; border: 1px solid #444444;
            }}
            QPushButton:hover {{ background-color: #c42b1c; }}
            QPushButton:pressed {{ background-color: #a41b0c; }}
        """)
        self.close_button.clicked.connect(self.close)

        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(self.minimize_button)
        title_bar_layout.addWidget(self.close_button)

        self.content_layout.addWidget(self.title_bar)

        # --- Add a separator line ---
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #3a3a3a; max-height: 1px;")
        self.content_layout.addWidget(separator)

        # --- Chat Area ---
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none; 
                background-color: {DARK_BACKGROUND};
            }}
            QScrollBar:vertical {{
                border: none; 
                background: {DARK_WIDGET_BACKGROUND}; 
                width: 8px;
                margin: 0px 0px 0px 0px; 
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: #555555; 
                min-height: 20px; 
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #777777;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none; 
                background: none; 
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ 
                background: none; 
            }}
        """)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet(f"background-color: {DARK_BACKGROUND};")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(5, 5, 5, 5)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.chat_container)
        self.content_layout.addWidget(self.scroll_area)

        # --- Typing Indicator ---
        self.typing_indicator = QLabel("", self)
        self.typing_indicator.setFont(QFont("Segoe UI", 10))
        self.typing_indicator.setStyleSheet(
            f"color: #9e9e9e; padding-left: 12px; background-color: transparent;")
        self.typing_indicator.setFixedHeight(20)
        self.typing_indicator.hide()
        self.content_layout.addWidget(self.typing_indicator)
        self.typing_animation_timer.timeout.connect(
            self.update_typing_animation)

        # --- Input Area ---
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 5, 0, 3)
        self.input_layout.setSpacing(8)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setFont(QFont("Segoe UI", 10))
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_WIDGET_BACKGROUND}; 
                color: {TEXT_COLOR};
                border-radius: {BORDER_RADIUS}px; 
                border: 1px solid #444444;
                padding: 8px 12px; 
                min-height: 25px;
            }}
            QLineEdit:focus {{ 
                border: 1px solid {ACCENT_COLOR}; 
            }}
        """)
        self.input_field.returnPressed.connect(self.send_message)

        # Make sure the input field can receive focus (fix for the focus issue)
        self.input_field.setFocusPolicy(Qt.StrongFocus)

        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_COLOR}; 
                color: {TEXT_COLOR};
                border-radius: {BORDER_RADIUS}px; 
                padding: 8px 15px;
                border: none; 
                min-height: 25px;
            }}
            QPushButton:hover {{ 
                background-color: #0369a1; 
            }}
            QPushButton:pressed {{ 
                background-color: #075985; 
            }}
        """)
        self.send_button.clicked.connect(self.send_message)

        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_button)
        self.content_layout.addLayout(self.input_layout)

        # --- Add size grip for resizing (bottom right corner) ---
        self.size_grip = QSizeGrip(self)
        self.size_grip.setStyleSheet("width: 16px; height: 16px;")
        self.content_layout.addWidget(
            self.size_grip, 0, Qt.AlignBottom | Qt.AlignRight)

        self.resize(self._initial_size)

        # Add initial AI message
        self.add_message("Hello! How can I assist you today?", is_user=False)

    def create_floating_icon(self):
        self.floating_icon = FloatingIcon()
        self.floating_icon.clicked.connect(self.toggle_restore)
        # Make the floating icon stay on all virtual desktops
        self.floating_icon.setWindowFlags(
            self.floating_icon.windowFlags() |
            Qt.X11BypassWindowManagerHint  # Helps with desktop switching
        )

    def add_message(self, text, is_user):
        bubble = ChatBubble(text, is_user, self.chat_container)
        self.chat_layout.addWidget(bubble)
        self.chat_layout.invalidate()
        self.chat_container.adjustSize()
        QTimer.singleShot(50, self.scroll_to_bottom)

        # Set focus to input field after receiving or sending a message
        self.input_field.setFocus()

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return
        self.add_message(user_text, is_user=True)
        self.input_field.clear()
        self.start_typing_indicator()
        # Schedule the AI response asynchronously
        asyncio.ensure_future(self.handle_ai_response(user_text))

    async def handle_ai_response(self, user_text):
        await self.ai_response(user_text)

    async def ai_response(self, user_text):
        response = await self.generate_ai_response(user_text)
        self.add_message(response, is_user=False)
        self.stop_typing_indicator()
        self.scroll_to_bottom()

        # Make sure the input field has focus after AI responds
        self.input_field.setFocus()

    async def generate_ai_response(self, prompt):
        return await do(prompt)

    def start_typing_indicator(self):
        self.typing_dots_count = 0
        self.typing_indicator.setText("AI is thinking.")
        self.typing_indicator.show()
        self.typing_animation_timer.start(400)

    def update_typing_animation(self):
        self.typing_dots_count = (self.typing_dots_count + 1) % 4
        dots = "." * self.typing_dots_count
        self.typing_indicator.setText(f"AI is thinking{dots}")

    def stop_typing_indicator(self):
        self.typing_animation_timer.stop()
        self.typing_indicator.hide()

    def toggle_minimize(self):
        if not self.is_minimized_to_icon:
            self.is_minimized_to_icon = True
            self.last_position = self.pos()
            self.hide()
            self._show_icon_after_hide(self.last_position)

    def _show_icon_after_hide(self, window_pos):
        # Position icon roughly centered where the window was
        icon_x = window_pos.x() + self.width() // 2 - ICON_SIZE // 2
        icon_y = window_pos.y() + self.height() // 2 - ICON_SIZE // 2

        screen_geometry = QDesktopWidget().availableGeometry()
        icon_x = max(screen_geometry.left(), min(
            icon_x, screen_geometry.right() - ICON_SIZE))
        icon_y = max(screen_geometry.top(), min(
            icon_y, screen_geometry.bottom() - ICON_SIZE))

        self.floating_icon.move(icon_x, icon_y)
        self.floating_icon.show()

    def toggle_restore(self):
        if self.is_minimized_to_icon:
            self.is_minimized_to_icon = False
            icon_pos = self.floating_icon.pos()
            self.floating_icon.hide()

            # Calculate window position based on icon position
            new_x = icon_pos.x() + ICON_SIZE // 2 - self.width() // 2
            new_y = icon_pos.y() + ICON_SIZE // 2 - self.height() // 2

            # Keep window within screen bounds
            screen_geometry = QDesktopWidget().availableGeometry()
            new_x = max(screen_geometry.left(), min(
                new_x, screen_geometry.right() - self.width()))
            new_y = max(screen_geometry.top(), min(
                new_y, screen_geometry.bottom() - self.height()))

            # Move the window before showing it
            self.move(new_x, new_y)
            self.show()
            self.activateWindow()
            self.raise_()

            # Set focus to input field after restoring
            QTimer.singleShot(100, self.input_field.setFocus)

    # --- Method to toggle visibility via shortcut ---
    def toggle_visibility_shortcut(self):
        # Use QTimer to ensure GUI updates happen in the main thread
        QTimer.singleShot(0, self._perform_toggle)

    def _perform_toggle(self):
        if self.isVisible() and not self.is_minimized_to_icon:
            self.toggle_minimize()
        elif not self.isVisible() and self.is_minimized_to_icon:
            self.toggle_restore()
        # Optional: Handle case where window is hidden but not minimized (e.g., closed)
        # else:
        #     print("Window state not handled by toggle.")

    # --- Setup global hotkey ---
    def setup_hotkey(self):
        try:
            # Define the hotkey (e.g., Ctrl+Alt+C)
            self.hotkey_listener = keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+c': self.toggle_visibility_shortcut
            })
            self.hotkey_listener.start()
            print("Hotkey 'Ctrl+Alt+C' registered successfully.")
        except Exception as e:
            print(f"Failed to register hotkey: {e}")
            print("Try running the script with administrator privileges.")

    # --- Custom resizing implementation for edge dragging ---
    def get_resize_edge(self, pos):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        # Define resize zones (distance from edge)
        edge_size = 12

        # Determine which edge(s) are being grabbed
        top = y < edge_size
        bottom = y > h - edge_size
        left = x < edge_size
        right = x > w - edge_size

        # Return the appropriate resize edge
        if top and left:
            return Qt.TopLeftCorner
        if top and right:
            return Qt.TopRightCorner
        if bottom and left:
            return Qt.BottomLeftCorner
        if bottom and right:
            return Qt.BottomRightCorner
        if top:
            return Qt.TopEdge
        if bottom:
            return Qt.BottomEdge
        if left:
            return Qt.LeftEdge
        if right:
            return Qt.RightEdge

        return None  # Not on any edge

    def update_cursor(self, pos):
        """Update cursor shape based on position"""
        edge = self.get_resize_edge(pos)

        if edge == Qt.TopLeftCorner or edge == Qt.BottomRightCorner:
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge == Qt.TopRightCorner or edge == Qt.BottomLeftCorner:
            self.setCursor(Qt.SizeBDiagCursor)
        elif edge == Qt.TopEdge or edge == Qt.BottomEdge:
            self.setCursor(Qt.SizeVerCursor)
        elif edge == Qt.LeftEdge or edge == Qt.RightEdge:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    # --- Window dragging and resizing functionality ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.title_bar.geometry().contains(event.pos()):
                self.offset = event.globalPos() - self.pos()
                event.accept()
            else:
                # Check if clicking on a resize edge
                edge = self.get_resize_edge(event.pos())
                if edge:
                    self.resizing = True
                    self.resize_edge = edge
                    self.resize_start_pos = event.globalPos()
                    self.resize_start_geometry = self.geometry()
                    event.accept()
                else:
                    self.offset = QPoint()
                    # Don't ignore to allow focus changes etc.

    def mouseMoveEvent(self, event):
        # Update cursor shape based on position
        self.update_cursor(event.pos())

        if event.buttons() & Qt.LeftButton:
            if self.resizing and self.resize_edge:
                # Handle resizing
                delta = event.globalPos() - self.resize_start_pos
                geo = self.resize_start_geometry

                # Apply changes based on which edge is being dragged
                new_geo = QRect(geo)

                if self.resize_edge in (Qt.TopLeftCorner, Qt.TopEdge, Qt.TopRightCorner):
                    new_geo.setTop(geo.top() + delta.y())

                if self.resize_edge in (Qt.TopLeftCorner, Qt.LeftEdge, Qt.BottomLeftCorner):
                    new_geo.setLeft(geo.left() + delta.x())

                if self.resize_edge in (Qt.TopRightCorner, Qt.RightEdge, Qt.BottomRightCorner):
                    new_geo.setRight(geo.right() + delta.x())

                if self.resize_edge in (Qt.BottomLeftCorner, Qt.BottomEdge, Qt.BottomRightCorner):
                    new_geo.setBottom(geo.bottom() + delta.y())

                # Apply new geometry (respecting minimum size)
                min_width = self.minimumWidth()
                min_height = self.minimumHeight()

                if new_geo.width() < min_width:
                    if self.resize_edge in (Qt.TopLeftCorner, Qt.LeftEdge, Qt.BottomLeftCorner):
                        new_geo.setLeft(new_geo.right() - min_width)
                    else:
                        new_geo.setRight(new_geo.left() + min_width)

                if new_geo.height() < min_height:
                    if self.resize_edge in (Qt.TopLeftCorner, Qt.TopEdge, Qt.TopRightCorner):
                        new_geo.setTop(new_geo.bottom() - min_height)
                    else:
                        new_geo.setBottom(new_geo.top() + min_height)

                self.setGeometry(new_geo)
                event.accept()

            elif not self.offset.isNull():
                # Handle dragging the window
                new_pos = event.globalPos() - self.offset

                # Add screen bounds check during drag
                screen_geometry = QDesktopWidget().availableGeometry()
                new_pos.setX(max(screen_geometry.left(), min(
                    new_pos.x(), screen_geometry.right() - self.width())))
                new_pos.setY(max(screen_geometry.top(), min(
                    new_pos.y(), screen_geometry.bottom() - self.height())))

                self.move(new_pos)
                event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = QPoint()
            self.resizing = False
            self.resize_edge = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            event.ignore()

    # Support for double-click to toggle window state
    def mouseDoubleClickEvent(self, event):
        if self.title_bar.geometry().contains(event.pos()):
            screen_geometry = QDesktopWidget().availableGeometry()

            if self.width() < screen_geometry.width() * 0.9 or self.height() < screen_geometry.height() * 0.9:
                # Save current geometry then maximize
                self.normal_geometry = self.geometry()
                self.setGeometry(screen_geometry)
            else:
                # Restore to previous size
                if self.normal_geometry:
                    self.setGeometry(self.normal_geometry)
                else:
                    # Fallback to initial size
                    self.resize(self._initial_size)
                    self.center_on_screen()

            event.accept()
        else:
            event.ignore()

    # Add support for mouse wheel to scroll chat
    def wheelEvent(self, event):
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().value() - event.angleDelta().y() // 2
        )
        event.accept()

    def closeEvent(self, event):
        # Stop the hotkey listener on close
        try:
            if hasattr(self, 'hotkey_listener'):
                self.hotkey_listener.stop()
                print("Hotkey 'Ctrl+Alt+C' unregistered.")
        except Exception as e:
            print(f"Error stopping hotkey listener: {e}")

        if self.floating_icon:
            self.floating_icon.close()
        super().closeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.normal_geometry is not None:
            self.normal_geometry = self.geometry()

    def showEvent(self, event):
        """Override showEvent to set focus on input field when window shows"""
        super().showEvent(event)
        QTimer.singleShot(100, self.input_field.setFocus)
