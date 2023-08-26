import sys
from random import randint
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QLabel, QFrame, QPushButton, QCheckBox, 
                               QLineEdit, QFormLayout, QVBoxLayout)

class PasswordWidget(QWidget):
    
    # Symbol Pools for Password Generation
    LETTERS = 'qwertyuiopasdfghjklzxcvbnm'
    NUMBERS = '1234567890'
    SPEC_CHARS = "`~!@#$%^&*()_-+={}[]\\|:;'<>,.?/"
    
    def __init__(self) -> None:
        super().__init__()
        
        # Output TextField
        self.password_field = QLabel(text="Нажмите \"Сгенерировать\"")
        self.password_field.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard or Qt.TextInteractionFlag.TextSelectableByMouse)
        self.password_field.setFrameStyle(QFrame.Shape.Box)
        self.password_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Generate Button
        self.generate_btn = QPushButton(text="Сгенерировать")
        
        # Checkboxes
        self.numbers_checkbox = QCheckBox("Должен содержать цифры")
        self.upper_checkbox = QCheckBox("Должен содержать заглавные буквы")
        self.spec_chars_checkbox = QCheckBox("Должен содержать специальные символы")
        
        # Text Labels
        self.min_length_label = QLabel(text="Минимальный размер пароля: ")
        self.max_length_label = QLabel(text="Максимальный размер пароля: ")
        self.warining_label = QLabel()
        self.warining_label.setWordWrap(True)
        self.warining_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Text Fields
        self.min_length_textfield = QLineEdit(text="6")
        self.max_length_textfield = QLineEdit(text="20")
        
        # Layouts - Password Generation Field and Button Layout
        self.generate_field_layout = QVBoxLayout()
        self.generate_field_layout.addWidget(self.warining_label)
        self.generate_field_layout.addWidget(self.password_field)
        self.generate_field_layout.addWidget(self.generate_btn)
        
        # Layouts
        self.main_layout = QVBoxLayout(self)
        
        # Layouts - Max and Min Pass Length
        self.pass_length_form = QFormLayout()
        self.pass_length_form.addRow(self.min_length_label, self.min_length_textfield)
        self.pass_length_form.addRow(self.max_length_label, self.max_length_textfield)
        
        self.main_layout.addLayout(self.pass_length_form)
        self.main_layout.addLayout(self.generate_field_layout)
        self.main_layout.addWidget(self.numbers_checkbox)
        self.main_layout.addWidget(self.upper_checkbox)
        self.main_layout.addWidget(self.spec_chars_checkbox)
        
        # Slots and Connections
        self.generate_btn.clicked.connect(self.generatePassword)
        
        
    @Slot()
    def generatePassword(self):
        self.warining_label.setText("")
        
        # Passwords Length Validation
        try:
            max_length = int(self.max_length_textfield.text())
            min_length = int(self.min_length_textfield.text())
            if not (4 <= min_length <= max_length and min_length <= max_length <= 20):
                self.warining_label.setText("Некорректная длина пароля\nПароль может быть от 4 до 20 символов")
                return
        except ValueError:
            self.warining_label.setText("В полях настроек должны быть только цифры")
            return
        
        # Password Generation
        password_length = randint(min_length, max_length)
        password = ""
        
        contains_upper = self.upper_checkbox.isChecked()
        contains_numbers = self.numbers_checkbox.isChecked()
        contains_spec_chars = self.spec_chars_checkbox.isChecked()
        
        if (any([contains_upper, contains_numbers, contains_spec_chars])):
            selected_options_count = (contains_numbers + contains_spec_chars + contains_upper)
            max_char_count = password_length - 1 // (selected_options_count + 1)
            
            if max_char_count > selected_options_count:
                max_char_count //= selected_options_count
            
            if contains_upper:
                upper_chars_count = randint(1, max_char_count)
                for i in range(0, upper_chars_count):
                    password += self.LETTERS.upper()[randint(0, len(self.LETTERS)-1)]
                password_length -= upper_chars_count
            
            if contains_spec_chars:
                spec_chars_count = randint(1, max_char_count)
                for i in range(0, spec_chars_count):
                    password += self.SPEC_CHARS[randint(0, len(self.SPEC_CHARS) - 1)]
                password_length -= spec_chars_count
            
            if contains_numbers:
                num_count = randint(1, max_char_count)
                for i in range(0, num_count):
                    password += self.NUMBERS[randint(0, len(self.NUMBERS) - 1)]
                password_length -= num_count
            
            for i in range(0, password_length):
                password += self.LETTERS[randint(0,len(self.LETTERS)-1)]
            
            password = list(password)
            
            for i in range(0, len(password)):
                perm_index = randint(0, len(password) - 1)
                password[i], password[perm_index] = password[perm_index], password[i]
            
            password = "".join(password)
        else:
            for i in range(0, password_length):
                password += self.LETTERS[randint(0,len(self.LETTERS)-1)]
        
        self.password_field.setText(password)
        
        
        


class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Генератор паролей")
        self.setFixedSize(400,270)
        
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu("Файл")
        
        self.exit_action = self.filemenu.addAction("Выйти", self.close)
        
        self.setCentralWidget(PasswordWidget())




if __name__ == "__main__":
    app = QApplication()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())