import os
import sys
import rsa
import time
import shelve
import socket
#from PyQt5 import QtCore, QtWidgets
from des import *

# АССИМЕТРИЧНОЕ 'rsa' ШИФРОВАНИЕ

# Мониторинг входящих сообщений
class message_monitor(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, server_socket, private_key, parent=None):
        QtCore.QThread.__init__(self, parent)
        # инициализируем сокет
        self.server_socket = server_socket
        # инициализируем приват ключ
        self.private_key = private_key
        # создаем сообщение
        self.message = None

    def run(self):
        # после запуска заходим в цикл
        while True:
            # Данные от собеседника (зашифрованные) (от сервера)
            try:
                self.message = self.server_socket.recv(1024)
                # если зашифрованное сообщение то расшифровываем при помощи 'rsa' и 'private_key'
                decrypt_message = rsa.decrypt(self.message, self.private_key)
                # отправляем сигнал в 'mysignal' и отправляем в расшифрованном формате (UTF-8)
                self.mysignal.emit(decrypt_message.decode('utf-8'))
            except: # Данные от сервера (не зашифрованные)
                # если данные не расшифрованы, то все равно передаем в норм формате
                self.mysignal.emit(self.message.decode('utf-8'))



class Client(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ip = None
        self.port = None
        self.friend_public_key = None
        
        # Ключи шифрования текущего клиента
        self.mypublickey = None
        self.myprivatekey = None
 
        # Проверка на наличие идентификатора собеседника
        # Есть ли в папке файл идентификатор собеседника
        if len(os.listdir('friend_id')) == 0:
            self.ui.lineEdit.setEnabled(False)  # блок кнопки
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
            message = 'Поместите идентификатор собеседника в "friend_id"'
            self.ui.plainTextEdit.appendPlainText(message)

        # Проверка создан ли личный идентификатор
        # Если в папке нет файла 'private'
        if not os.path.exists('private'):
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
            message = 'Также необходимо сгенерировать свой идентификатор'
            self.ui.plainTextEdit.appendPlainText(message)

        else:  # ТО:
            # Подгрузка данных текущего клиента
            # При помощи 'shelve' открываем файл и извлекаем 'private' ключ
            # Все данные храним в ОЗУ
            with shelve.open('private') as file:
                self.mypublickey = file['pubkey']
                self.myprivatekey = file['privkey']
                self.ip = file['ip']
                self.port = file['port']

            # Подгрузка данных собеседника
            # Открываем публичный ключ
            with shelve.open(os.path.join('friend_id', os.listdir('friend_id')[0])) as file:
                self.friend_public_key = file['pubkey']

            message = 'Подключитесь к серверу'
            self.ui.plainTextEdit.appendPlainText(message)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
            self.ui.pushButton_2.setEnabled(True)


        # Обработчики всех кнопок которые есть в интерфейсе
        self.ui.pushButton_2.clicked.connect(self.connect_server)
        self.ui.pushButton.clicked.connect(self.send_message)
        self.ui.pushButton_5.clicked.connect(self.generate_encrypt)
        self.ui.pushButton_4.clicked.connect(self.clear_panel)

    # ****Подключаемся к серверу****
    def connect_server(self):
        try:
            # создаем сокет запрос IPV4, TCP
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # производим коннект по инициализированному IP/PORT
            self.tcp_client.connect((self.ip, self.port)); time.sleep(2)

            # Запускаем мониторинг входящих сообщений
            self.message_monitor = message_monitor(self.tcp_client, self.myprivatekey)
            self.message_monitor.mysignal.connect(self.update_chat)  # обработчик 'emit'
            self.message_monitor.start()  # запуск бесконечных обновлений сообщений
            # если сообщение есть, то выводим его в 'ui.plainTextEdit'

            # Производим действия с объектами (Разблокировываем)
            self.ui.lineEdit_4.setEnabled(False)
            self.ui.lineEdit_5.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            # Заблокируем те что нам не надо
            self.ui.pushButton.setEnabled(True)
            self.ui.lineEdit.setEnabled(True)
            self.ui.pushButton_4.setEnabled(True)
            self.ui.pushButton_5.setEnabled(False)
        # В случае если сервер отключен
        except:
            self.ui.plainTextEdit.clear()
            self.ui.plainTextEdit.appendPlainText('Ошибка подключения к серверу!')
            self.ui.plainTextEdit.appendPlainText('Измените идентификаторы и повторите попытку!')


    # ****Отправить сообщение****
    # Функция привязана к Кнопке Отправить
    def send_message(self):
        # Перед тем как отправить, проверяем
        try:
            # Содержит ли поле для ввода символы > 0
            if len(self.ui.lineEdit.text()) > 0:
                # Присваиваем его в переменную 'message'
                message = self.ui.lineEdit.text()
                # Шифруем его используя Публичный ключ другого клиента
                crypto_message = rsa.encrypt(message.encode('utf-8'), self.friend_public_key)

                # Выводим наше сообщение в панель в открытом виде, чтобы удобно работать с текстом
                self.ui.plainTextEdit.appendPlainText(f'[Вы]: {message}')
                # Используя TCP клиент отправляем шифров сообщение (tcp_client это наш сокет)
                self.tcp_client.send(crypto_message)
                # Очищаем наш lineEdit
                self.ui.lineEdit.clear()
        except:
            sys.exit()


    # Сгенерировать ключи шифрования
    def generate_encrypt(self):
        if len(self.ui.lineEdit_4.text()) > 0:  # Указан ли IP
            if len(self.ui.lineEdit_5.text()) > 0:  # Указан ли Port
                # Если оба заполнены, то генерируем Pub и Priv ключи используя 'rsa.newkeys'
                (pubkey, privkey) = rsa.newkeys(512)

                # Проверяем создана ли папка 'test'
                test_dir = 'test'
                # Если нет, то создаем
                if not os.path.exists(test_dir):
                    os.makedirs(test_dir)
                # После того как сгенерировали Ключ открываем 'shelve' и указываем ИМЯ ФАЙЛА
                with shelve.open('test/your_id') as file:
                    # В качестве СЛОВАРЯ указываем наш КЛЮЧ и Передаём значения
                    file['pubkey'] = pubkey
                    file['ip'] = str(self.ui.lineEdit_4.text())
                    file['port'] = int(self.ui.lineEdit_5.text())
                    # В файл 'your_id' записываем КЛЮЧИ 'pubkey' 'ip' 'port'
                
                with shelve.open('test/private') as file:
                    file['pubkey'] = pubkey
                    file['privkey'] = privkey
                    file['ip'] = str(self.ui.lineEdit_4.text())
                    file['port'] = int(self.ui.lineEdit_5.text())

                with shelve.open(os.path.join('friend_id', os.listdir('friend_id')[0])) as file:
                    self.friend_public_key = file['pubkey']

                self.ui.plainTextEdit_2.appendPlainText('Создан "your_id" идентификатор')
                self.ui.plainTextEdit_2.appendPlainText('Передайте его собеседнику и начните диалог')
        # ЕСЛИ НЕ УКАЗАЛ ДАННЫЕ ТО ВЫВОДИМ СООБЩЕНИЯ ОБ ОШИБКЕ
            else:
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText('Проверьте правильность вводимых данных!')     
        else:
            self.ui.plainTextEdit_2.clear()
            self.ui.plainTextEdit_2.appendPlainText('Проверьте правильность вводимых данных!')



    # Закрытия соединения
    def closeEvent(self, event):
        try:
            # Отправляем СЕРВЕРУ сообщение 'exit'
            self.tcp_client.send(b'exit')
            self.tcp_client.close()
        except:
            pass


    # Обновляем окно чата
    def update_chat(self, value):
        self.ui.plainTextEdit.appendHtml(value)  # передаем значение из 'emit'


    # Очищаем окно с чатом
    def clear_panel(self):
        self.ui.plainTextEdit.clear()
            


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Client()
    myapp.show()
    sys.exit(app.exec_())
