import sys
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QComboBox, QHBoxLayout, QFileDialog, QToolBar, QAction
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image

class VideoConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DM Multimedia Converter")

        self.init_ui()

    def init_ui(self):
        # Создание тулбара для переключения между вкладками
        self.toolbar = self.addToolBar('Switch Tabs')

        # Добавление действий для тулбара
        video_action = QAction("Видео", self)
        video_action.triggered.connect(self.showVideoTab)
        self.toolbar.addAction(video_action)

        image_action = QAction("Изображения", self)
        image_action.triggered.connect(self.showImageTab)
        self.toolbar.addAction(image_action)

        # Вкладка для конвертации видео
        self.video_tab = QWidget()
        self.init_video_tab()

        # Вкладка для конвертации изображений
        self.image_tab = QWidget()
        self.init_image_tab()

        # Первоначально показываем вкладку с видео
        self.showVideoTab()

        # Добавление виджетов вкладок в центральную область
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.video_tab)
        central_layout.addWidget(self.image_tab)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        # Применение стилей
        self.apply_styles()

        # Установка фиксированного размера окна
        self.setFixedSize(600, 200)

        # Иконка для приложения
        script_directory = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_directory, 'img', 'icon.png')
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

    def apply_styles(self):
        style_sheet = """
            QWidget {
                background-color: #f0f0f0;
                color: #333;
                font-size: 14px;
            }

            QPushButton {
                background-color: #009B77;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #00664E;
            }

            QLineEdit, QComboBox {
                padding: 8px;
                font-size: 14px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }

            QLabel {
                padding: 8px;
                font-size: 14px;
            }

            QToolBar {
                background-color: #009B77;
                color: white;
                border: none;
                font-size: 14px;
            }

            QToolButton {
                background-color: #00664E;
                color: white;
                border: none;
                padding: 8px;
                font-size: 14px;
            }

            QToolButton:hover {
                background-color: #004733;
            }
        """

        self.setStyleSheet(style_sheet)

    def init_video_tab(self):
        # Создание фрейма для ввода файла и выбора формата
        file_format_frame = QFrame(self.video_tab)
        self.video_tab.layout = QVBoxLayout(self.video_tab)
        self.video_tab.layout.addWidget(file_format_frame)

        # Создание горизонтального макета для ввода файла и выбора формата
        file_format_layout = QHBoxLayout(file_format_frame)

        # Создание текстового поля для ввода файла
        self.video_entry = QLineEdit(self.video_tab)
        file_format_layout.addWidget(self.video_entry)

        # Кнопка для выбора файла
        select_video_button = QPushButton("Выбрать видео", self.video_tab)
        select_video_button.clicked.connect(self.selectVideoFile)
        file_format_layout.addWidget(select_video_button)

        # Выпадающий список для выбора формата видео
        self.video_format_combo = QComboBox(self.video_tab)
        self.video_format_combo.addItem("Выберите формат")
        self.video_format_combo.addItems(['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm'])
        file_format_layout.addWidget(self.video_format_combo)

        # Кнопка для конвертации видео
        convert_video_button = QPushButton("Конвертировать видео", self.video_tab)
        convert_video_button.clicked.connect(self.convertVideo)
        file_format_layout.addWidget(convert_video_button)

        # Метка для вывода статуса
        self.video_status_label = QLabel(self.video_tab)
        self.video_tab.layout.addWidget(self.video_status_label)

        self.video_tab.setLayout(self.video_tab.layout)

    def init_image_tab(self):
        # Создание фрейма для ввода файла и выбора формата
        file_format_frame = QFrame(self.image_tab)
        self.image_tab.layout = QVBoxLayout(self.image_tab)
        self.image_tab.layout.addWidget(file_format_frame)

        # Создание горизонтального макета для ввода файла и выбора формата
        file_format_layout = QHBoxLayout(file_format_frame)

        # Создание текстового поля для ввода файла
        self.image_entry = QLineEdit(self.image_tab)
        file_format_layout.addWidget(self.image_entry)

        # Кнопка для выбора файла
        select_image_button = QPushButton("Выбрать фото", self.image_tab)
        select_image_button.clicked.connect(self.selectImageFile)
        file_format_layout.addWidget(select_image_button)

        # Выпадающий список для выбора формата изображения
        self.image_format_combo = QComboBox(self.image_tab)
        self.image_format_combo.addItem("Выберите формат")
        self.image_format_combo.addItems(['png', 'jpg', 'bmp', 'gif', 'jpeg', 'tiff', 'ico'])
        file_format_layout.addWidget(self.image_format_combo)

        # Кнопка для конвертации изображения
        convert_image_button = QPushButton("Конвертировать фото", self.image_tab)
        convert_image_button.clicked.connect(self.convertImage)
        file_format_layout.addWidget(convert_image_button)

        # Метка для вывода статуса
        self.image_status_label = QLabel(self.image_tab)
        self.image_tab.layout.addWidget(self.image_status_label)

        self.image_tab.setLayout(self.image_tab.layout)

    def selectVideoFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        video_file, _ = QFileDialog.getOpenFileName(self, "Выбрать видео файл", "", "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm);;All Files (*)", options=options)
        self.video_entry.setText(video_file)

    def selectImageFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_file, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Image Files (*.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        self.image_entry.setText(image_file)

    def convertVideo(self):
        video_file = self.video_entry.text()
        output_format = self.video_format_combo.currentText()

        if video_file and output_format != "Выберите формат":
            output_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            output_file = os.path.join(output_dir, f'converted_video.{output_format}')

            video_clip = VideoFileClip(video_file)
            video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
            video_clip.close()

            self.video_status_label.setText(f'Видео успешно сконвертировано в {output_file}')
        else:
            self.video_status_label.setText("Пожалуйста, выберите файл и формат для конвертации.")

    def convertImage(self):
        input_file = self.image_entry.text()
        output_format = self.image_format_combo.currentText()

        if input_file and output_format != "Выберите формат":
            output_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            output_file = os.path.join(output_dir, f'converted_image.{output_format}')

            image = Image.open(input_file)
            image.save(output_file, format=output_format)

            self.image_status_label.setText(f'Изображение успешно сконвертировано в {output_file}')
        else:
            self.image_status_label.setText("Пожалуйста, выберите файл и формат для конвертации.")

    def showVideoTab(self):
        self.video_tab.show()
        self.image_tab.hide()

    def showImageTab(self):
        self.image_tab.show()
        self.video_tab.hide()


if __name__ == "__main__":
    app = QApplication([])
    window = VideoConverterApp()
    window.show()
    sys.exit(app.exec_())
