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
import pulp
from main_lab1 import getcandidates


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
        self.setGeometry(100, 100, 1000, 600)

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
        self.input_p.setText("age, sex, x1a, x2a, x3a, x4a, x5a, x6a, x7a, x8a, q1")
        self.p_label.setGeometry(100, 100, 200, 30)
        self.input_p.setGeometry(300, 100, 600, 30)

        # Add an input field
        self.s_label = QLabel("Змінні стану:", self)
        self.input_s = QLineEdit(self)
        self.input_s.setPlaceholderText("Введіть змінні стану")
        self.input_s.setText("x4b, x5b, x6b, x7b")
        self.s_label.setGeometry(100, 200, 200, 30)
        self.input_s.setGeometry(300, 200, 600, 30)

        # Add an input field
        self.u_label = QLabel("Змінні управління:", self)
        self.input_u = QLineEdit(self)
        self.input_u.setPlaceholderText("Введіть змінні управління")
        self.input_u.setText("u1, u2")
        self.u_label.setGeometry(100, 300, 200, 30)
        self.input_u.setGeometry(300, 300, 600, 30)

        # Add an input field
        self.q_label = QLabel("Критерій:", self)
        self.input_q = QLineEdit(self)
        self.input_q.setPlaceholderText("Введіть критерій")
        self.input_q.setText("q2")
        self.q_label.setGeometry(100, 400, 200, 30)
        self.input_q.setGeometry(300, 400, 600, 30)

        # Add a close button
        self.close_button = QPushButton("Створити модель", self)
        self.close_button.clicked.connect(self.next)
        self.close_button.setGeometry(100, 500, 200, 30)

        self.normal_screen()
        self.normal_all()
    
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def next(self):
        p = self.input_p.text().replace(" ", "").split(",")
        s = self.input_s.text().replace(" ", "").split(",")
        u = self.input_u.text().replace(" ", "").split(",")
        q = self.input_q.text().replace(" ", "")
        self.next_window = SettingStepwiseWindow(p, s, u, q)
        self.next_window.show()
        self.close()
    
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


class MyCandidatesWindow(QWidget):
    def __init__(self, parent, vars, candidates):
        super().__init__()
        self.parent = parent
        w0, w1, h0, m0 = 150, 30, 30, 2
        vars_n = len(vars)
        candidates_lens = []
        for cand in candidates:
            candidates_lens.append(len(cand))
        self.w = (w0 + w1 + 2 * m0) * vars_n + m0
        self.h = (max(candidates_lens) + 3) * h0 + (max(candidates_lens) + 3) * m0
        self.setFixedSize(self.w, self.h)
        label0 = QLabel("Кандидати на вхід до моделі", self)
        label0.setStyleSheet("color: black; font-size: 20px;")
        label0_w, label0_h = label0.sizeHint().width(), label0.sizeHint().height()
        label0_x, label0_y = 300 - int(label0_w / 2) + m0, h0 - int(label0_h / 2) + m0
        label0.setGeometry(label0_x, label0_y, label0_w, label0_h)
        for i, var in enumerate(vars):
            label = QLabel(var + " =", self)
            label.setStyleSheet("color: black; font-size: 14px;")
            label_w, label_h = label.sizeHint().width(), label.sizeHint().height()
            label_x = int((w1 + w0 + 2 * m0) * (i + 0.5)) - int(label_w / 2)
            label_y = int((h0 + m0) * 2.5) - int(label_h / 2)
            label.setGeometry(label_x, label_y, label_w, label_h)
            for j, val in enumerate(candidates[i]):
                label = QLabel(val, self)
                label.setStyleSheet("color: black; font-size: 14px;")
                label_w, label_h = label.sizeHint().width(), label.sizeHint().height()
                label_x = int((w1 + w0 + 2 * m0) * i) + int((w0 + m0) / 2) - int(label_w / 2)
                label_y = int((h0 + m0) * (3.5 + j)) - int(label_h / 2)
                label.setGeometry(label_x, label_y, label_w, label_h)
                button = QPushButton("-", self)
                button.setStyleSheet("background-color: white; color: black; font-size: 14px;")
                button.clicked.connect(lambda checked, var = var, val = val: parent.remove_candidate(var, val))
                button_x = int((w1 + w0 + 2 * m0) * (i + 1)) - h0
                button_y = int((h0 + m0) * (3.5 + j)) - int(label_h / 2)
                button.setGeometry(button_x, button_y, h0, h0)


class MyMandatoryMembersWindow(QWidget):
    def __init__(self, parent, vars, members):
        super().__init__()
        self.parent = parent
        w0, w1, h0, m0 = 150, 30, 30, 2
        vars_n = len(vars)
        candidates_lens = []
        for cand in members:
            candidates_lens.append(len(cand))
        self.w = (w0 + w1 + 2 * m0) * vars_n + m0
        self.h = (max(candidates_lens) + 3) * h0 + (max(candidates_lens) + 3) * m0
        self.setFixedSize(self.w, self.h)
        label0 = QLabel("Обов'язкові члени моделі", self)
        label0.setStyleSheet("color: black; font-size: 20px;")
        label0_w, label0_h = label0.sizeHint().width(), label0.sizeHint().height()
        label0_x, label0_y = 300 - int(label0_w / 2) + m0, h0 - int(label0_h / 2) + m0
        label0.setGeometry(label0_x, label0_y, label0_w, label0_h)
        for i, var in enumerate(vars):
            label = QLabel(var + " =", self)
            label.setStyleSheet("color: black; font-size: 14px;")
            label_w, label_h = label.sizeHint().width(), label.sizeHint().height()
            label_x = int((w1 + w0 + 2 * m0) * (i + 0.5)) - int(label_w / 2)
            label_y = int((h0 + m0) * 2.5) - int(label_h / 2)
            label.setGeometry(label_x, label_y, label_w, label_h)
            for j, val in enumerate(members[i]):
                label = QLabel(val, self)
                label.setStyleSheet("color: black; font-size: 14px;")
                label_w, label_h = label.sizeHint().width(), label.sizeHint().height()
                label_x = int((w1 + w0 + 2 * m0) * i) + int((w0 + m0) / 2) - int(label_w / 2)
                label_y = int((h0 + m0) * (3.5 + j)) - int(label_h / 2)
                label.setGeometry(label_x, label_y, label_w, label_h)
                button = QPushButton("-", self)
                button.setStyleSheet("background-color: white; color: black; font-size: 14px;")
                button.clicked.connect(lambda checked, var = var, val = val: parent.remove_member(var, val))
                button_x = int((w1 + w0 + 2 * m0) * (i + 1)) - h0
                button_y = int((h0 + m0) * (3.5 + j)) - int(label_h / 2)
                button.setGeometry(button_x, button_y, h0, h0)


class SettingStepwiseWindow(QMainWindow):
    def __init__(self, p, s, u, q):
        super().__init__()
        self.w, self.h = 1230, 820
        self.setFixedSize(self.w, self.h)
        self.vars = [q] + s

        self.candidates = []
        for var in self.vars:
            candidates = getcandidates(p, u, rank = 1)
            self.candidates.append(candidates)
        
        self.members = []
        for var in self.vars:
            members = [var]
            self.members.append(members)
        
        self.candidates_widget = MyCandidatesWindow(self, self.vars, self.candidates)
        self.scroll_candidates = QScrollArea(self)
        self.scroll_candidates.setGeometry(10, 10, 600, 400)
        self.scroll_candidates.setStyleSheet("background-color: #ddffff;")
        self.scroll_candidates.setWidget(self.candidates_widget)

        self.members_widget = MyMandatoryMembersWindow(self, self.vars, self.members)
        self.scroll_members = QScrollArea(self)
        self.scroll_members.setGeometry(620, 10, 600, 400)
        self.scroll_members.setStyleSheet("background-color: #ddffff;")
        self.scroll_members.setWidget(self.members_widget)
    
    def remove_candidate(self, var, val):
        ind = self.vars.index(var)
        self.candidates[ind].remove(val)
        self.candidates_widget = MyCandidatesWindow(self, self.vars, self.candidates)
        self.scroll_candidates.setWidget(self.candidates_widget)
    
    def remove_member(self, var, val):
        ind = self.vars.index(var)
        self.members[ind].remove(val)
        self.members_widget = MyMandatoryMembersWindow(self, self.vars, self.members)
        self.scroll_members.setWidget(self.members_widget)


class PatientData(QWidget):
    def __init__(self, vars, default_p = 0):
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
            if default_p != 0:
                input.setText(str(default_p[i]))
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
                return f"Не всі поля параметрів пацієнта введені, або деякі введені некоректно (поля мають містити лише числові дані)\n{self.vars[i]}='{input.text()}'"
            data.append(float(input.text()))
        return [self.vars, data]


class LimitationData(QWidget):
    def __init__(self, vars, default_lims = 0):
        super().__init__()
        self.vars = vars
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
            if default_lims != 0:
                input1.setText(str(default_lims[i][0]))
                input2.setText(str(default_lims[i][1]))
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
        for i, input in enumerate(self.inputs):
            try:
                float(input[0].text())
            except:
                return f"Проблеми з обмеженнями: min {self.vars[i]} = '{input[0].text()}'"
            try:
                float(input[1].text())
            except:
                return f"Проблеми з обмеженнями: max {self.vars[i]} = '{input[1].text()}'"
            data.append([float(input[0].text()), float(input[1].text())])
        return [self.vars, data]


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
                ind = results[0].index(vars[i])
                label2 = QLabel(str(round(results[1][ind], 4)), self)
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
    def __init__(self, p, s, u, q, full_models, default_p = 0, default_lims = 0):
        super().__init__()
        self.full_models = full_models
        title = "Курсова"
        self.setWindowTitle(title)
        w, h = 1240, 830
        self.p, self.s, self.u, self.q = p, s, u, q
        self.setFixedSize(w, h)
        #self.setGeometry(100, 100, 1000, 800)

        self.patient_widget = PatientData(p, default_p=default_p)
        self.scroll_patient = QScrollArea(self)
        self.scroll_patient.setGeometry(10, 10, 400, 400)
        self.scroll_patient.setStyleSheet("background-color: lightblue;")
        self.scroll_patient.setWidget(self.patient_widget)
        self.scroll_patient.setWidgetResizable(True)

        self.limitation_widget = LimitationData(s + u, default_lims=default_lims)
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
        self.calc_button.setStyleSheet("background-color: #ff0055; font-size: 14px;")
        self.calc_button.clicked.connect(self.calc)
        self.calc_button.setGeometry(625, 720, 300, 100)

        self.back_button = QPushButton("Назад до моделей", self)
        self.back_button.setStyleSheet("background-color: #ff0055; font-size: 14px;")
        self.back_button.clicked.connect(self.back)
        self.back_button.setGeometry(930, 720, 300, 100)
    
    def calc(self):
        values = self.patient_widget.get_data()
        if type(values) == str:
            self.show_message(values)
            return
        self.short_models = simple_data.replace_with_values(self.full_models, values)
        self.short_models_widget = ShowModels(self.short_models)
        self.scroll_short.setWidget(self.short_models_widget)

        limitations = self.limitation_widget.get_data()
        if type(limitations) == str:
            self.show_message(limitations)
            return
        us = []
        for u in self.u:
            u_ind = limitations[0].index(u)
            lim_min, lim_max = limitations[1][u_ind]
            exec(u + "=pulp.LpVariable('" + u + "'," + str(lim_min) + "," + str(lim_max) + ")")
            exec("us.append(" + u + ")")
        model = pulp.LpProblem("Minimization problem", pulp.LpMinimize)
        # print(self.short_models)
        for i, arr_model in enumerate(self.short_models):
            str_model = str(arr_model[1])
            if arr_model[0] == self.q:
                text_to_exec = "model+=" + str_model + ", 'Objective function'"
                exec(text_to_exec)
                continue
            s_lim_ind = limitations[0].index(arr_model[0])
            lim_min, lim_max = limitations[1][s_lim_ind]
            text_to_exec1 = "model+=" + str_model + "<=" + str(lim_min) + ", 'Constraint " + str(i*2+1) + "'"
            text_to_exec2 = "model+=" + str_model + ">=" + str(lim_min) + ", 'Constraint " + str(i*2+2) + "'"
            # print(text_to_exec1)
            # print(text_to_exec2)
            exec(text_to_exec1)
            exec(text_to_exec2)
        status = model.solve()
        #print("Status:", pulp.LpStatus[status])
        values = []
        pump_values = []
        for i, u in enumerate(us):
            # print(self.u[i], pulp.value(u))
            values.append(pulp.value(u))
            pump_values.append([self.u[i], pulp.value(u)])
        values = [self.u, values]
        result_models = simple_data.replace_with_values(self.short_models, values) + pump_values
        result_models_values = []
        result_models_vars = []
        for res in result_models:
            result_models_vars.append(res[0])
            result_models_values.append(res[1])
        result_models = [result_models_vars, result_models_values]
        # print(result_models)
        self.results_widget = ResultsData(self.s + self.u, results=result_models)
        self.scroll_results.setWidget(self.results_widget)
    
    def back(self):
        self.show_message("Повернутися до моделей можна у повній версії програми")
    
    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("В нас тут проблемка")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


def light_test():
    app = QApplication(sys.argv)
    test_p = ["age", "sex", "x1a", "x2a", "x3a", "x4a", "x5a", "x6a", "x7a", "x8a", "q1"]
    test_s = ["x4b", "x5b", "x6b", "x7b"]
    test_u = ["u1", "u2"]
    test_q = "q2"
    file_name = "data_renamed.xlsx"
    file = pd.read_excel(file_name)
    ava_p = []
    for p in test_p:
        if p == "sex":
            ava_p.append(1)
        else:
            ava_p.append(file[p].mean())
    # print(ava_p)
    def_lims = []
    for l in test_s + test_u:
        if p == "sex":
            def_lims.append([0, 1])
        else:
            def_lims.append([file[l].min(), file[l].max()])
    # print(def_lims)
    test_mosels = simple_data.models2
    window = Results(test_p, test_s, test_u, test_q, test_mosels, default_p=ava_p, default_lims=def_lims)
    window.show()
    sys.exit(app.exec_())


def main_test():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # light_test()
    main_test()
