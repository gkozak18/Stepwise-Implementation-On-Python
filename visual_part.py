import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton, 
    QVBoxLayout,
    QGridLayout,
    QWidget, 
    QFileDialog, 
    QLabel, 
    QDesktopWidget, 
    QLineEdit,
    QScrollArea,
    QMessageBox)
from PyQt5.QtCore import Qt
import pandas as pd
import simple_data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Завантаження файлу")

        layout = QVBoxLayout()

        self.button = QPushButton("Виберіть файл", self)
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(100, 100, 1000, 800)  # (x, y, width, height)
        #self.showFullScreen()
        self.center()
    
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.load_file(file_name)

    def load_file(self, file_name):
        # Open a new window to display the file content
        self.file_window = FileWindow(file_name)
        self.file_window.show()
        self.close()


class FileWindow(QMainWindow):
    def __init__(self, file_name):
        super().__init__()
        title = file_name.split("/")[-1]
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1000, 800)

        data = pd.read_excel(file_name)
        variables = data.columns
        vars_str = "Список доступних змінних: "
        for i in variables:
            vars_str += i + ", "
        vars_str = vars_str[:-2]

        self.vars_label = QLabel(vars_str, self)
        self.vars_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.vars_label.setGeometry(100, 50, 800, 30)

        self.p_label = QLabel("Параметри:", self)
        self.input_p = QLineEdit(self)
        self.input_p.setPlaceholderText("Введіть параметри по котрим має будуватися модель")
        self.p_label.setGeometry(100, 100, 200, 30)
        self.input_p.setGeometry(300, 100, 600, 30)

        # Add an input field
        self.s_label = QLabel("Змінні стану:", self)
        self.input_s = QLineEdit(self)
        self.input_s.setPlaceholderText("Введіть змінні стану")
        self.s_label.setGeometry(100, 200, 200, 30)
        self.input_s.setGeometry(300, 200, 600, 30)

        # Add an input field
        self.u_label = QLabel("Змінні управління:", self)
        self.input_u = QLineEdit(self)
        self.input_u.setPlaceholderText("Введіть змінні управління")
        self.u_label.setGeometry(100, 300, 200, 30)
        self.input_u.setGeometry(300, 300, 600, 30)

        # Add an input field
        self.q_label = QLabel("Критерій:", self)
        self.input_q = QLineEdit(self)
        self.input_q.setPlaceholderText("Введіть критерій")
        self.q_label.setGeometry(100, 400, 200, 30)
        self.input_q.setGeometry(300, 400, 600, 30)

        # Add a close button
        self.close_button = QPushButton("Створити модель", self)
        self.close_button.clicked.connect(self.close)
        self.close_button.setGeometry(100, 500, 200, 30)

        self.normal_screen()
        self.normal_all()
    
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def normal_screen(self):
        w, h = 0.9, 0.9
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, int(screen.width() * w), int(screen.height() * h))
    
    def move_to(self, widget, x, y, xx, yy):
        window = self.geometry()
        w, h = window.width(), window.height()
        a, b, = int(w / xx), int(h / yy)
        widget.move(x * a, y * b)
    
    def resizeEvent(self, event):
        self.normal_all()
    
    def normal_all(self):
        self.move_to(self.vars_label, 1, 1, 10, 7)

        self.move_to(self.p_label, 1, 2, 10, 7)
        self.move_to(self.input_p, 2, 2, 10, 7)

        self.move_to(self.s_label, 1, 3, 10, 7)
        self.move_to(self.input_s, 2, 3, 10, 7)

        self.move_to(self.u_label, 1, 4, 10, 7)
        self.move_to(self.input_u, 2, 4, 10, 7)

        self.move_to(self.q_label, 1, 5, 10, 7)
        self.move_to(self.input_q, 2, 5, 10, 7)

        self.move_to(self.close_button, 1, 6, 10, 7)


class PatientData(QWidget):
    def __init__(self, vars):
        super().__init__()
        x0, y0 = 375, 50
        x1, x3 = int(x0 / 4), 3 * int(x0 / 4)
        y2 = int(y0 / 2)
        self.labels = []
        self.inputs = []
        self.vars = vars
        n = len(vars)
        self.setFixedSize(x0, (n + 2) * y0)
        
        label0 = QLabel("Дані пацієнта", self)
        label0.setStyleSheet("color: black; font-size: 20px;")
        label0_w, label0_h = label0.sizeHint().width(), label0.sizeHint().height() 
        label0.setGeometry(int(x0 / 2) - int(label0_w / 2), int(y0 / 2) - int(label0_h / 2), label0_w, label0_h)
        label1 = QLabel("Показники:", self)
        label1.setStyleSheet("font-size: 14px;")
        label1_w, label1_h = label1.sizeHint().width(), label1.sizeHint().height()
        label1.setGeometry(x1 - int(label1_w / 2), y0 + y2 - int(label1_h / 2), label1_w, label1_h)
        label2 = QLabel("Значення:", self)
        label2.setStyleSheet("font-size: 14px;")
        label2_w, label2_h = label2.sizeHint().width(), label2.sizeHint().height()
        label2.setGeometry(x3 - int(label2_w / 2), y0 + y2 - int(label2_h / 2), label2_w, label2_h)
        for i in range(n):
            label = QLabel(vars[i], self)
            label.setStyleSheet("font-size: 14px;")
            input = QLineEdit(self)
            label_w, label_h = label.sizeHint().width(), label.sizeHint().height()
            label_x, label_y = x1 - int(label_w / 2), (i + 3) * y0 - y2 - int(label_h / 2)
            input_w, input_h = 140, 30
            input_x, input_y = x3 - int(input_w / 2), (i + 3) * y0 - y2 - int(input_h / 2)
            label.setGeometry(label_x, label_y, label_w, label_h)
            input.setGeometry(input_x, input_y, input_w, input_h)
            input.setStyleSheet("background-color: white;")
            self.labels.append(label)
            self.inputs.append(input)
    
    def get_data(self):
        data = []
        for i, input in enumerate(self.inputs):
            try:
                float(input.text())
            except:
                return "Не всі поля параметрів пацієнта введені, або деякі введені некоректно (поля мають містити лише числові дані)"
            data.append(float(input.text()))
        return [self.vars, data]


class LimitationData(QWidget):
    def __init__(self, vars):
        super().__init__()
        x0, y0 = 375, 50
        x1, x3, x5 = int(x0 / 6), 3 * int(x0 / 6), 5 * int(x0 / 6)
        y2 = int(y0 / 2)
        self.labels = []
        self.inputs = []
        n = len(vars)
        self.setFixedSize(x0, (n + 2) * y0)
        
        label0 = QLabel("Обмеження", self)
        label0.setStyleSheet("color: black; font-size: 20px;")
        label0_w, label0_h = label0.sizeHint().width(), label0.sizeHint().height() 
        label0.setGeometry(int(x0 / 2) - int(label0_w / 2), int(y0 / 2) - int(label0_h / 2), label0_w, label0_h)
        label1 = QLabel("Максимум:", self)
        label1.setStyleSheet("font-size: 14px;")
        label1_w, label1_h = label1.sizeHint().width(), label1.sizeHint().height()
        label1.setGeometry(x1 - int(label1_w / 2), y0 + y2 - int(label1_h / 2), label1_w, label1_h)
        label2 = QLabel("Мінімум:", self)
        label2.setStyleSheet("font-size: 14px;")
        label2_w, label2_h = label2.sizeHint().width(), label2.sizeHint().height()
        label2.setGeometry(x5 - int(label2_w / 2), y0 + y2 - int(label2_h / 2), label2_w, label2_h)
        for i in range(n):
            label = QLabel(vars[i], self)
            label.setStyleSheet("font-size: 14px;")
            input1 = QLineEdit(self)
            input2 = QLineEdit(self)
            label_w, label_h = label.sizeHint().width(), label.sizeHint().height()
            label_x, label_y = x3 - int(label_w / 2), (i + 3) * y0 - y2 - int(label_h / 2)
            input_w, input_h = 100, 30
            input1_x, input1_y = x1 - int(input_w / 2), (i + 3) * y0 - y2 - int(input_h / 2)
            input2_x, input2_y = x5 - int(input_w / 2), (i + 3) * y0 - y2 - int(input_h / 2)
            label.setGeometry(label_x, label_y, label_w, label_h)
            input1.setGeometry(input1_x, input1_y, input_w, input_h)
            input1.setStyleSheet("background-color: white;")
            input2.setGeometry(input2_x, input2_y, input_w, input_h)
            input2.setStyleSheet("background-color: white;")
            self.labels.append(label)
            self.inputs.append((input1, input2))
    
    def get_data(self):
        data = []
        for i in self.inputs:
            data.append(float(i[0].text()), float(i[1].text()))
        return data


class ResultsData(QWidget):
    def __init__(self, vars, results = 0):
        super().__init__()
        x0, y0 = 375, 50
        x1, x3 = int(x0 / 4), 3 * int(x0 / 4)
        y2 = int(y0 / 2)
        n = len(vars)
        self.setFixedSize(x0, (n + 1) * y0)
        
        label0 = QLabel("Результати", self)
        label0.setStyleSheet("color: black; font-size: 20px;")
        label0_w, label0_h = label0.sizeHint().width(), label0.sizeHint().height() 
        label0.setGeometry(int(x0 / 2) - int(label0_w / 2), int(y0 / 2) - int(label0_h / 2), label0_w, label0_h)
        for i in range(n):
            label1 = QLabel(vars[i], self)
            label1.setStyleSheet("font-size: 14px;")
            if results == 0:
                label2 = QLabel("0", self)
            else:
                label2 = QLabel(str(results[i]), self)
            label2.setStyleSheet("font-size: 14px;")
            label1_w, label1_h = label1.sizeHint().width(), label1.sizeHint().height()
            label1_x, label1_y = x1 - int(label1_w / 2), (i + 2) * y0 - y2 - int(label1_h / 2)
            label2_w, label2_h = label2.sizeHint().width(), label2.sizeHint().height()
            label2_x, label2_y = x3 - int(label2_w / 2), (i + 2) * y0 - y2 - int(label2_h / 2)
            label1.setGeometry(label1_x, label1_y, label1_w, label1_h)
            label2.setGeometry(label2_x, label2_y, label2_w, label2_h)


class ShowModels(QWidget):
    def __init__(self, models):
        super().__init__()
        y0 = 50
        y2 = int(y0 / 2)
        n = len(models)
        label_widths = []
        label0 = QLabel("Моделі:", self)
        label0.setStyleSheet("font-size: 20px;")
        label0_w, label0_h = label0.sizeHint().width(), label0.sizeHint().height()
        label0_x, label0_y = 10, y0 - y2
        label0.setGeometry(label0_x, label0_y, label0_w, label0_h)
        for i, model in enumerate(models):
            text = model[0] + " = "
            if len(model) == 3:
                for j in range(len(model[1])):
                    text += str(round(model[2][j], 4)) + "*" + model[1][j] + " + "
                text += str(round(model[2][-1], 4))
            else:
                text += str(model[1])
            label = QLabel(text, self)
            label.setStyleSheet("font-size: 14px;")
            label_w, label_h = label.sizeHint().width(), label.sizeHint().height()
            label_x, label_y = 10, (i + 2) * y0 - y2
            label.setGeometry(label_x, label_y, label_w, label_h)
            label_widths.append(label.sizeHint().width())
        max_width = max(label_widths)
        self.setFixedSize(max_width + 20, (n + 1) * y0)


class Results(QMainWindow):
    def __init__(self, p, s, u, full_models):
        super().__init__()
        self.full_models = full_models
        title = "Курсова"
        self.setWindowTitle(title)
        w, h = 1240, 830
        self.setFixedSize(w, h)
        #self.setGeometry(100, 100, 1000, 800)

        self.patient_widget = PatientData(p)
        self.scroll_patient = QScrollArea(self)
        self.scroll_patient.setGeometry(10, 10, 400, 400)
        self.scroll_patient.setStyleSheet("background-color: lightblue;")
        self.scroll_patient.setWidget(self.patient_widget)
        self.scroll_patient.setWidgetResizable(True)

        self.limitation_widget = LimitationData(s + u)
        self.scroll_limitation = QScrollArea(self)
        self.scroll_limitation.setGeometry(420, 10, 400, 400)
        self.scroll_limitation.setStyleSheet("background-color: lightblue;")
        self.scroll_limitation.setWidget(self.limitation_widget)
        self.scroll_limitation.setWidgetResizable(True)

        self.results_widget = ResultsData(s + u)
        self.scroll_results = QScrollArea(self)
        self.scroll_results.setGeometry(830, 10, 400, 400)
        self.scroll_results.setStyleSheet("background-color: #ff77ff;")
        self.scroll_results.setWidget(self.results_widget)
        self.scroll_results.setWidgetResizable(True)

        full_models_widget = ShowModels(full_models)
        self.scroll_full = QScrollArea(self)
        self.scroll_full.setGeometry(10, 420, 605, 400)
        self.scroll_full.setStyleSheet("background-color: #aaaaff;")
        self.scroll_full.setWidget(full_models_widget)

        self.short_models_widget = ShowModels(full_models)
        self.scroll_short = QScrollArea(self)
        self.scroll_short.setGeometry(625, 420, 605, 290)
        self.scroll_short.setStyleSheet("background-color: #aaaaff;")
        self.scroll_short.setWidget(self.short_models_widget)

        self.calc_button = QPushButton("Порахувати", self)
        self.calc_button.setStyleSheet("background-color: #ff0000;")
        self.calc_button.clicked.connect(self.calc)
        self.calc_button.setGeometry(625, 720, 300, 100)
    
    def calc(self):
        values = self.patient_widget.get_data()
        if type(values) == str:
            self.show_message(values)
            return
        self.short_models = simple_data.replace_with_values(self.full_models, values)
        self.short_models_widget = ShowModels(self.short_models)
        self.scroll_short.setWidget(self.short_models_widget)
    
    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("В нас тут проблемка")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


def light_test():
    app = QApplication(sys.argv)
    test_p = ["age", "sex", "x1a", "x2a", "x3a", "x4a", "x5a", "x6a", "x7a", "x8a", "q1"]
    test_s = ["x1b", "x2b", "x3b", "x4b", "x5b", "x6b", "x7b", "x8b"]
    test_u = ["u1", "u2"]
    test_mosels = simple_data.models
    window = Results(test_p, test_s, test_u, test_mosels)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    light_test()
