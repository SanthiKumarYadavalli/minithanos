from RealtimeSTT import AudioToTextRecorder
import asyncio
from agents.god import do
from live import audio_mode
from chat.main import QApplication, QFont, ChatWindow
import sys


def text_mode():
    while True:
        prompt = input(">>> ")
        if prompt == "exit":
            break
        if prompt:
            response = do(prompt)
            print("\n" + response + "\n")


# if __name__ == "__main__":
#     recorder = AudioToTextRecorder(language="en", spinner=True, ensure_sentence_ends_with_period=True)
#     while True:
#         try:
#             # asyncio.run(audio_mode(recorder))
#             text_mode()
#         except Exception as e:
#             print(type(e), e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application-wide font
    app_font = QFont("Segoe UI", 10)
    app.setFont(app_font)

    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())