import asyncio
from chat.main import QApplication, ChatWindow
import sys
from qasync import QEventLoop


if __name__ == '__main__':

    app = QApplication(sys.argv)
    loop = QEventLoop(app)  # Integrate asyncio with PyQt
    asyncio.set_event_loop(loop)

    window = ChatWindow()
    window.show()

    with loop:  # Run the event loop
        sys.exit(loop.run_forever())