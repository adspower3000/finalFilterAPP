import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QDateEdit, QFileDialog
from PyQt5.QtCore import Qt, QDate
import psycopg2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import qdarkstyle




class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        # Создаем элементы интерфейса
        self.date_from_label = QLabel('Дата от:')
        self.date_from_edit = QDateEdit(self)
        self.date_from_edit.setDate(
            QDate.currentDate().addDays(-7))  # установите начальную дату, например, за последнюю неделю

        self.date_to_label = QLabel('Дата до:')
        self.date_to_edit = QDateEdit(self)
        self.date_to_edit.setDate(QDate.currentDate())

        self.open_csv_button = QPushButton('Открыть CSV')
        self.open_csv_button.clicked.connect(self.open_csv_file)

        self.filter_button = QPushButton('Применить фильтр')
        self.filter_button.clicked.connect(self.filter_data)

        self.plot_button = QPushButton('Построить график')
        self.plot_button.clicked.connect(self.plot_data)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Дата', 'Мощность', 'Рабочие часы'])

        self.sum_label = QLabel('Сумма в промежутке дат: 0')

        # Размещаем элементы в макете
        layout = QVBoxLayout(self)

        layout.addWidget(self.open_csv_button)

        layout.addWidget(self.date_from_label)
        layout.addWidget(self.date_from_edit)
        layout.addWidget(self.date_to_label)
        layout.addWidget(self.date_to_edit)

        layout.addWidget(self.filter_button)

        layout.addWidget(self.table)

        layout.addWidget(self.sum_label)

        layout.addWidget(self.plot_button)

        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(dark_stylesheet)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Рассчетка')
        self.show()

    def open_csv_file(self):
        filename = QFileDialog.getOpenFileName(self)
        return filename


    def db_conn(self):
        date_from = self.date_from_edit.date().toString(Qt.ISODate)
        date_to = self.date_to_edit.date().toString(Qt.ISODate)

        # ... (ваш существующий код для подключения к базе данных и выполнения запроса)
        conn_params = {
            'dbname': 'suz_sutki',
            'user': 'postgres',
            'password': '123321',
            'host': '127.0.0.1',
            'port': '5432',
        }

        try:
            # Подключаемся к базе данных
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()

            # Выполняем запрос к базе данных с использованием параметров дат
            query = f"SELECT date_time, power, job_hours  FROM suz_sutki WHERE date_time BETWEEN '{date_from}' AND '{date_to}';"
            cursor.execute(query)
            data = cursor.fetchall()

            cursor.close()
            conn.close()

        except Exception as e:
              print(f"Error: {e}")

        return data

    def filter_data(self):
        # Получаем значения дат из элементов интерфейса
        data = self.db_conn()

        # Очищаем таблицу перед обновлением данных
        self.table.setRowCount(0)

        # Обновляем таблицу с полученными данными
        for row_num, (date, power, job_hours) in enumerate(data):
            self.table.insertRow(row_num)
            self.table.setItem(row_num, 0, QTableWidgetItem(str(date)))
            self.table.setItem(row_num, 1, QTableWidgetItem(str(power)))
            self.table.setItem(row_num, 2, QTableWidgetItem(str(job_hours)))

        # Подсчитываем сумму по столбцу N
        sum_n = sum(row[1] for row in data)
        self.sum_label.setText(f'Сумма в промежутке дат: {sum_n}')




    def plot_data(self):

        data = self.db_conn()

    # Получаем данные для построения графика
        dates = [row[0] for row in data]
        values = [row[1] for row in data]

        # Создаем график
        fig, ax = plt.subplots()
        ax.plot(dates, values, label='Столбец N')
        ax.set_title('График столбца N')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Значение')
        ax.legend()

        # Отображаем график
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    sys.exit(app.exec_())