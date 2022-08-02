# pip install discontrol
# pip install pyqt5
# pip install discord

try:
    from os import name
    from os.path import expanduser
    from re import findall

    CurrentUserFolder = expanduser('~')

    if name != 'nt':
        input('WINDOWS ONLY')
        exit(1)

    import discontrol, threading, random, time
    from PyQt5 import QtCore, QtWidgets, QtGui
    from sys import argv
    from ctypes import windll
    import random
    from os import _exit
    from os.path import split, sep
    from discord import Webhook, RequestsWebhookAdapter

    class HoverButton(QtWidgets.QPushButton):
        hover = QtCore.pyqtSignal(str)

        def __init__(self, parent=None):
            super(HoverButton, self).__init__(parent)

        def enterEvent(self, event):
            self.hover.emit('enterEvent')

        def leaveEvent(self, event):
            self.hover.emit('leaveEvent')

    folder = split(__file__)[0]

    WhatIsToken = '''ТОКЕН УЧЁТНОЙ ЗАПИСИ
Это код, состоящий из набора символов, дающий полный доступ к учётной записи Discord.

Получить токен можно следующий образом:
1. Откройте браузерную версию приложения
2. Войдите в свой аккаунт (или тот который будет рейдить)
3. Откройте инструменты разработчика (Ctrl+Shift+I)
4. Перейдите в раздел Сеть
5. Отправьте какое нибудь сообщение, или выполните другое действие
6. Нажмите на запрос
7. Найдите в заголовках Authorization
8. Скопируйте значение'''

    WhatIsChannelID = '''ID канала Discord

ID канала - это уникальная цифра
У каждого объекта в Disord (будь то роль или сервер) есть свой ID

Как получить ID объекта?
1. Откройте настройки Discord
2. Перейдите во вкладку Расширенные
3. Включите режим разработчика

Теперь вы можете копировать ID любого объекта, кликнув по нему ПКМ и выбрав пункт Копировать ID'''

    WhatIsMessageInput = '''ДОСТУПНЫЕ МОДИФИКАТОРЫ
?digit - случайное однозначное число
?letter - случайная анлийская буква
?pref - случайный знак препинания
?char <начало:Число>,<конец:Число> - рандомный символ со случайным индексом между началом и концом

Модификаторы созданы, чтобы избежать анти-спама.'''

    class Attackker:
        is_working = False
        is_checking = False

    def SmartSplit(text, sep):
        if sep not in text:
            return [text]
        else:
            return text.split(sep)

    def Parse(message):

        if not ('?digit' in message or '?letter' in message
                or '?prep' in message or '?char' in message):
            return message

        for x in range(message.count('?digit')):
            message = message.replace('?digit', str(random.randint(0, 9)), 1)

        for x in range(message.count('?letter')):
            message = message.replace(
                '?letter', random.choice('QWERTYUIOPASDFGHJKLZXCVBNM'), 1)

        for x in range(message.count('?prep')):
            message = message.replace('?prep', random.choice('.!?'), 1)

        if '?char' in message:
            searches_randchar = findall('\?char \d+,\s*\d+', message)

            for s in searches_randchar:
                vals = s.replace('?char ', '').split(',')
                start = int(vals[0])
                end = int(vals[1])
                if start >= end:
                    raise TypeError(
                        'Минимальное число не может быть больше максимального')
                if start < 0 or end < 0:
                    raise TypeError(
                        '?char <start> или ?char <end> не может быть меньше 0')
                message = message.replace(s, chr(random.randint(start, end)))

        return message

    def cont_rand():
        return ''.join(
            random.choice('QWERTYUIOPASDFGHJKLZXCVBNM') for x in range(2))

    class Data:
        LogsWindowIsOpened = False

    logs = ''

    def UpdateLogs(text):

        global logs
        logs = text + '\n' + logs

        if len(logs.split('\n')) > 50:
            logs = '\n'.join(logs.split('\n')[:35])

    class ApplicationLogsWindow(QtWidgets.QMainWindow):
        update_signal = QtCore.pyqtSignal(str)

        def LogsUpdateSignalHandler(self):
            global logs
            self.Logs.setPlainText(logs)

        def InitializeWindow(self, MainWindow):
            Data.LogsWindowIsOpened = True
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(380, 230)
            MainWindow.setMinimumSize(QtCore.QSize(380, 230))
            MainWindow.setMaximumSize(QtCore.QSize(380, 230))
            self.move(420, 100)
            self.setWindowIcon(QtGui.QIcon(folder + sep + 'log.png'))
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.Background = QtWidgets.QLabel(self.centralwidget)
            self.Background.setGeometry(QtCore.QRect(0, 0, 381, 230))
            self.Background.setStyleSheet("background-color: rgb(54,57,63)")
            self.Background.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.Background.setObjectName("Background")
            self.Logs = QtWidgets.QPlainTextEdit(self.centralwidget)
            self.Logs.setGeometry(QtCore.QRect(10, 10, 360, 180))
            self.Logs.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.Logs.setReadOnly(True)
            self.Logs.setPlaceholderText("В логах пусто")
            self.Logs.setPlainText(logs)
            self.Logs.setStyleSheet("font: 87 8pt \"Segoe UI Black\";\n"
                                    "background-color: rgb(64,68,75);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-radius: 5;\n"
                                    "padding-left: 3;\n"
                                    "padding-top: 3;\n"
                                    "padding-right: 3;\n"
                                    "padding-bottom: 3;\n")
            self.ClearLogs = HoverButton(self.centralwidget)
            self.ClearLogs.setGeometry(QtCore.QRect(10, 200, 360, 20))
            self.ClearLogs.setFocusPolicy(QtCore.Qt.NoFocus)
            self.ClearLogs.setStyleSheet("font: 87 8pt \"Segoe UI Black\";\n"
                                         "border-style: solid;\n"
                                         "border-color: white;\n"
                                         "border-radius: 5;\n"
                                         "background-color: rgb(88,101,242);\n"
                                         "color: white;")
            self.ClearLogs.setObjectName("ClearLogs")
            MainWindow.setCentralWidget(self.centralwidget)
            MainWindow.setWindowTitle("HeckerAttack - Logs")
            self.ClearLogs.setText("ОЧИСТИТЬ ЛОГИ")

            QtCore.QMetaObject.connectSlotsByName(MainWindow)

            self.ClearLogs.clicked.connect(self.InvokeClearLogs)

            upt = threading.Thread(target=self.Ticker)

            self.update_signal.connect(self.LogsUpdateSignalHandler)

            upt.start()

            self.ClearLogs.hover.connect(self.ClButtonHover)

        def InvokeClearLogs(self):
            global logs
            self.Logs.setPlainText('')
            logs = ''

        def Ticker(self):
            while True:
                text = "Update"
                self.update_signal.emit(text)
                time.sleep(.2)

        def ClButtonHover(self, event):
            if event == 'enterEvent':
                self.ClearLogs.setStyleSheet(
                    "font: 87 8pt \"Segoe UI Black\";\n"
                    "border-style: solid;\n"
                    "border-color: white;\n"
                    "border-radius: 5;\n"
                    "background-color: rgb(72,84,200);\n"
                    "color: white;")
            else:
                self.ClearLogs.setStyleSheet(
                    "font: 87 8pt \"Segoe UI Black\";\n"
                    "border-style: solid;\n"
                    "border-color: white;\n"
                    "border-radius: 5;\n"
                    "background-color: rgb(88,101,242);\n"
                    "color: white;\n")

    class LogsWindowClass(ApplicationLogsWindow):

        def __init__(self):
            super().__init__()
            self.InitializeWindow(self)

        def closeEvent(self, *args):
            Data.LogsWindowIsOpened = False
            global logs
            logs = self.Logs.toPlainText()
            self.close()

    class Invokers:

        def InvokeWindowStep1():
            windll.user32.MessageBoxW(0, WhatIsToken,
                                      'Что такое токен и как получить', 0)

        def InvokeWindowStep2():
            windll.user32.MessageBoxW(0, WhatIsChannelID,
                                      'Что такое Discord ID и как получить', 0)

        def InvokeWindowStep3():
            windll.user32.MessageBoxW(0, WhatIsMessageInput, 'Ввод сообщения',
                                      0)

    class ApplicationMainWindow(QtWidgets.QMainWindow):

        AttackButtonChangeStyleSignal = QtCore.pyqtSignal(str)

        is_attack = False

        def hecker_attack(self, token, attack_channels, spam_text, thr_id):

            print(f'Starting hecker attack on token {token}')

            UpdateLogs(f'[INFO] Started attack thread {thr_id} - USER')

            client = discontrol.Client(token)

            while Attackker.is_working:
                for attack in attack_channels:
                    try:
                        if not Attackker.is_working:
                            return
                        client.send_message(attack, Parse(spam_text), False)
                        UpdateLogs(
                            f'[INFO] [200 - OK] Sended flood in {attack} as USER'
                        )
                    except Exception as e:
                        try:
                            retry_after = e.args[0]['retry_after']
                            UpdateLogs(
                                f'[INFO] [429 - Ratelimited] Wait {round(retry_after, 3)} s. - {attack}'
                            )
                            time.sleep(retry_after)
                        except:
                            try:
                                message = e.args[0]['message']
                                UpdateLogs(f'[Error] {message}')
                                time.sleep(1)
                            except:
                                UpdateLogs(f'[Error] Unknown -> {e}')
                                time.sleep(1)

        def webhook_hecker_attack(self, url, spam_text, thr_id):

            UpdateLogs(f'[INFO] Started attack thread {thr_id} - WEBHOOK')

            try:
                webhook = Webhook.from_url(url,
                                           adapter=RequestsWebhookAdapter())
            except:
                UpdateLogs(f'[ERROR] Webhook error: {url}')
                return

            while Attackker.is_working:
                try:
                    webhook.send(Parse(spam_text))
                    UpdateLogs(f'[INFO] [200 - OK] Sended flood as WEBHOOK')
                except:
                    UpdateLogs(f'[ERROR] Failed to send flood as webhook')
                    time.sleep(1)

        def attack(self, clients, channels, spam_text):
            for c in clients:
                threading.Thread(target=lambda: self.hecker_attack(
                    c, channels, spam_text)).start()

        def start_attack(self):
            if not Attackker.is_checking:
                threading.Thread(target=self.start_attack_thread).start()

        def start_attack_thread(self):
            if self.TokensInput.toPlainText() == '':
                windll.user32.MessageBoxW(
                    0, f'Поле ввода токенов не может быть пустым.', 'ОШИБКА!',
                    0)
                return

            try:
                Parse(self.SpamEdit.toPlainText())
            except Exception as e:
                windll.user32.MessageBoxW(0, str(e), 'Ошибка парсера', 0x10)
                return

            if self.is_attack:
                Attackker.is_working = False
                self.is_attack = False
                self.AttackButtonChangeStyleSignal.emit('Default')
                UpdateLogs('[INFO] Stopping attack')
                return

            UpdateLogs('[INFO] Starting attack')

            clients = SmartSplit(self.TokensInput.toPlainText(), '\n')

            index = 0

            for token in clients:
                if 'http://' not in token and 'https://' not in token:
                    try:
                        index += 1
                        self.AttackButtonChangeStyleSignal.emit(
                            f'CheckingClient {index},{len(clients)}')
                        UpdateLogs(f'[INFO] Сканирование токена {token}')
                        discontrol.Client(str(token))
                    except Exception as e:
                        UpdateLogs(f'[WARNING] Неверный токен - {token}')
                        print(f'Error {e}')
                        windll.user32.MessageBoxW(
                            0, f'Токен "{token}" №{index} неверен.', 'ОШИБКА!',
                            0)
                        self.AttackButtonChangeStyleSignal.emit('Default')
                        return
                else:
                    try:
                        index += 1
                        self.AttackButtonChangeStyleSignal.emit(
                            f'CheckingClient {index},{len(clients)}')
                        UpdateLogs(f'[INFO] Сканирование вебхука {token}')
                        Webhook.from_url(token,
                                         adapter=RequestsWebhookAdapter())
                    except:
                        UpdateLogs(f'[WARNING] Неверный вебхук - {token}')
                        print(f'Error {e}')
                        windll.user32.MessageBoxW(
                            0, f'Вебхук "{token}" №{index} неверен.',
                            'ОШИБКА!', 0)
                        self.AttackButtonChangeStyleSignal.emit('Default')
                        return

            channels = []

            for channelid in SmartSplit(self.IdsInput.toPlainText(), '\n'):
                try:
                    channelid = int(channelid)
                    channels.append(channelid)
                    continue
                except:
                    windll.user32.MessageBoxW(
                        0, f'Канал "{channelid}" не является числом.',
                        'ОШИБКА!', 0)
                    self.AttackButtonChangeStyleSignal.emit('Default')

            self.is_attack = True

            clients = SmartSplit(self.TokensInput.toPlainText(), '\n')

            UpdateLogs('[INFO] Starting attack clients')

            index = 1

            Attackker.is_working = True

            for token in clients:
                if 'http://' not in token and 'https://' not in token:
                    threading.Thread(target=lambda: self.hecker_attack(
                        str(token), channels, self.SpamEdit.toPlainText(),
                        index)).start()
                else:
                    threading.Thread(target=lambda: self.webhook_hecker_attack(
                        str(token), self.SpamEdit.toPlainText(), index)).start(
                        )
                index += 1
                time.sleep(.2)

            global CurrentUserFolder

            tokens = open(
                CurrentUserFolder + '\\' + 'hecker_attack_ok_tokens.txt', 'w')

            tokens.write(self.TokensInput.toPlainText())

            UpdateLogs('[INFO] Токены записаны в hecker_attack_ok_tokens.txt')

            tokens.close()

            self.AttackButtonChangeStyleSignal.emit('Attacking')

        def InitializeWindow(self, MainWindow):
            global CurrentUserFolder
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(310, 440)
            MainWindow.setMinimumSize(QtCore.QSize(310, 440))
            MainWindow.setMaximumSize(QtCore.QSize(310, 440))
            self.move(100, 100)
            self.setWindowIcon(QtGui.QIcon(folder + sep + 'icon.png'))
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.ApplicationMainLabel = QtWidgets.QLabel(self.centralwidget)
            self.ApplicationMainLabel.setGeometry(QtCore.QRect(5, 5, 301, 31))
            self.ApplicationMainLabel.setStyleSheet(
                "font: 87 14pt \"Segoe UI Black\";\n"
                "color: rgb(255, 255, 255);")
            self.ApplicationMainLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.ApplicationMainLabel.setObjectName("ApplicationMainLabel")
            self.TokensInput = QtWidgets.QPlainTextEdit(self.centralwidget)
            self.TokensInput.setGeometry(QtCore.QRect(10, 70, 291, 66))
            self.TokensInput.setStyleSheet("font: 87 8pt \"Segoe UI Black\";\n"
                                           "background-color: rgb(64,68,75);\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border-radius: 5;\n"
                                           "padding-left: 3;\n"
                                           "padding-top: 3;\n"
                                           "padding-right: 3;\n"
                                           "padding-bottom: 3;\n")
            self.TokensInput.setObjectName("TokensInput")
            try:
                tokens = open(
                    CurrentUserFolder + '\\' + 'hecker_attack_ok_tokens.txt',
                    'r')
                available_tokens = tokens.read()
                tokens.close()
                UpdateLogs(
                    f'[INFO] Чтение токенов из hecker_attack_ok_tokens.txt')
            except:
                available_tokens = ''
                file = open(
                    CurrentUserFolder + '\\' + 'hecker_attack_ok_tokens.txt',
                    'w')
                file.close()
                UpdateLogs(
                    '[INFO] В папке пользователя создан hecker_attack_ok_tokens.txt, потому что предыдущий был удалён/не создан.'
                )

            if available_tokens != '':
                self.TokensInput.setPlainText(available_tokens)

            self.LabelStep1 = QtWidgets.QLabel(self.centralwidget)
            self.LabelStep1.setGeometry(QtCore.QRect(10, 40, 291, 21))
            self.LabelStep1.setStyleSheet("font: 10pt \"Segoe UI Black\";\n"
                                          "color: rgb(184,187,194);")
            self.LabelStep1.setAlignment(QtCore.Qt.AlignCenter)
            self.LabelStep1.setObjectName("LabelStep1")
            self.IdsInput = QtWidgets.QPlainTextEdit(self.centralwidget)
            self.IdsInput.setGeometry(QtCore.QRect(10, 180, 291, 66))
            self.IdsInput.setStyleSheet("font: 87 8pt \"Segoe UI Black\";\n"
                                        "background-color: rgb(64,68,75);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-radius: 5;\n"
                                        "padding-left: 3;\n"
                                        "padding-top: 3;\n"
                                        "padding-right: 3;\n"
                                        "padding-bottom: 3;\n")
            self.IdsInput.setObjectName("IdsInput")
            self.LabelStep2 = QtWidgets.QLabel(self.centralwidget)
            self.LabelStep2.setGeometry(QtCore.QRect(10, 150, 291, 21))
            self.LabelStep2.setStyleSheet("font: 10pt \"Segoe UI Black\";\n"
                                          "color: rgb(184,187,194);")
            self.LabelStep2.setAlignment(QtCore.Qt.AlignCenter)
            self.LabelStep2.setObjectName("LabelStep2")
            self.SpamEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
            self.SpamEdit.setGeometry(QtCore.QRect(10, 290, 291, 66))
            self.SpamEdit.setStyleSheet("font: 87 8pt \"Segoe UI Black\";\n"
                                        "background-color: rgb(64,68,75);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-radius: 5;\n"
                                        "padding-left: 3;\n"
                                        "padding-top: 3;\n"
                                        "padding-right: 3;\n"
                                        "padding-bottom: 3;\n")
            self.SpamEdit.setObjectName("SpamEdit")
            self.LabelStep3 = QtWidgets.QLabel(self.centralwidget)
            self.LabelStep3.setGeometry(QtCore.QRect(10, 260, 291, 21))
            self.LabelStep3.setStyleSheet("font: 10pt \"Segoe UI Black\";\n"
                                          "color: rgb(184,187,194);")
            self.LabelStep3.setAlignment(QtCore.Qt.AlignCenter)
            self.LabelStep3.setObjectName("LabelStep3")
            self.AttackButton = HoverButton(self.centralwidget)
            self.AttackButton.setGeometry(QtCore.QRect(20, 380, 186, 36))
            self.AttackButton.setStyleSheet(
                "font: 87 8pt \"Segoe UI Black\";\n"
                "border-style: solid;\n"
                "border-color: white;\n"
                "border-radius: 5;\n"
                "background-color: rgb(88,101,242);\n"
                "color: white;\n")
            self.AttackButton.setObjectName("AttackButton")
            self.Background = QtWidgets.QLabel(self.centralwidget)
            self.Background.setGeometry(QtCore.QRect(0, 0, 316, 441))
            self.Background.setStyleSheet("background-color: rgb(54,57,63);")
            self.Background.setText("")
            self.Background.setObjectName("Background")
            self.AboutStep1 = QtWidgets.QPushButton(self.centralwidget)
            self.AboutStep1.setGeometry(QtCore.QRect(275, 110, 21, 21))
            self.AboutStep1.setStyleSheet(
                "font: 87 8pt \"Segoe UI Black\";\n"
                "border-radius: 10;\n"
                "background-color: rgb(185,187,190);\n"
                "color: rbg(64,68,75);")
            self.AboutStep1.setObjectName("AboutStep1")
            self.AboutStep2 = QtWidgets.QPushButton(self.centralwidget)
            self.AboutStep2.setGeometry(QtCore.QRect(275, 220, 21, 21))
            self.AboutStep2.setStyleSheet(
                "font: 87 8pt \"Segoe UI Black\";\n"
                "border-radius: 10;\n"
                "background-color: rgb(185,187,190);\n"
                "color: rbg(64,68,75);")
            self.AboutStep2.setObjectName("AboutStep2")
            self.AboutStep3 = QtWidgets.QPushButton(self.centralwidget)
            self.AboutStep3.setGeometry(QtCore.QRect(275, 330, 21, 21))
            self.AboutStep3.setStyleSheet(
                "font: 87 8pt \"Segoe UI Black\";\n"
                "border-radius: 10;\n"
                "background-color: rgb(185,187,190);\n"
                "color: rbg(64,68,75);")
            self.AboutStep3.setObjectName("AboutStep3")
            self.ShowLogs = HoverButton(self.centralwidget)
            self.ShowLogs.setGeometry(QtCore.QRect(215, 380, 76, 36))
            self.ShowLogs.setStyleSheet("font: 87 8pt \"Segoe UI Black\";\n"
                                        "border-style: solid;\n"
                                        "border-color: white;\n"
                                        "border-radius: 5;\n"
                                        "background-color: rgb(59,165,93);\n"
                                        "color: white;")
            self.ShowLogs.setObjectName("ShowLogs")
            self.Background.raise_()
            self.ApplicationMainLabel.raise_()
            self.TokensInput.raise_()
            self.LabelStep1.raise_()
            self.IdsInput.raise_()
            self.LabelStep2.raise_()
            self.SpamEdit.raise_()
            self.LabelStep3.raise_()
            self.AttackButton.raise_()
            self.AboutStep1.raise_()
            self.AboutStep2.raise_()
            self.AboutStep3.raise_()
            self.ShowLogs.raise_()
            MainWindow.setCentralWidget(self.centralwidget)

            MainWindow.setWindowTitle("HeckerAttack")
            self.ApplicationMainLabel.setText("HeckerAttack by Its-MatriX")
            self.TokensInput.setPlaceholderText(
                "Введите токен(ы) аккаунта(ов) или URL вебхука(ов) по одному на строку"
            )
            self.LabelStep1.setText("1. Аккаунты")
            self.IdsInput.setPlaceholderText(
                "Введите ID каналов по одному на строку")
            self.LabelStep2.setText("2. Каналы")
            self.SpamEdit.setPlaceholderText("Введите текст")
            self.LabelStep3.setText("3. Текст")
            self.AttackButton.setText("АТАКОВАТЬ")
            self.AboutStep1.setText("?")
            self.AboutStep2.setText("?")
            self.AboutStep3.setText("?")
            self.ShowLogs.setText("ЛОГИ")

            QtCore.QMetaObject.connectSlotsByName(MainWindow)

            self.AboutStep1.clicked.connect(Invokers.InvokeWindowStep1)
            self.AboutStep2.clicked.connect(Invokers.InvokeWindowStep2)
            self.AboutStep3.clicked.connect(Invokers.InvokeWindowStep3)
            self.AttackButton.clicked.connect(self.start_attack)
            self.ShowLogs.clicked.connect(self.OpenLogsWindow)
            self.AttackButton.hover.connect(self.AttackButtonHover)
            self.ShowLogs.hover.connect(self.LogsButtonHover)
            self.AttackButtonChangeStyleSignal.connect(
                self.ChangeAttackButtonStyle)

        def ChangeAttackButtonStyle(self, signal):
            print(f'Event -> ChangeAttackButtonStyle: {signal}')
            if signal == 'Attacking':
                Attackker.is_checking = False
                self.AttackButton.setStyleSheet(
                    "font: 87 8pt \"Segoe UI Black\";\n"
                    "border-style: solid;\n"
                    "border-color: white;\n"
                    "border-radius: 5;\n"
                    "background-color: rgb(237,66,69);\n"
                    "color: rgb(255, 255, 255);")
                self.AttackButton.setText('АТАКА')
            elif signal == 'Default':
                Attackker.is_checking = False
                self.AttackButton.setStyleSheet(
                    "font: 87 8pt \"Segoe UI Black\";\n"
                    "border-style: solid;\n"
                    "border-color: white;\n"
                    "border-radius: 5;\n"
                    "background-color: rgb(88,101,242);\n"
                    "color: white;")
                self.AttackButton.setText('АТАКОВАТЬ')
            elif signal == 'Starting':
                Attackker.is_checking = False
                self.AttackButton.setStyleSheet(
                    "font: 87 8pt \"Segoe UI Black\";\n"
                    "border-style: solid;\n"
                    "border-color: white;\n"
                    "border-radius: 5;\n"
                    "background-color: rgb(88,101,242);\n"
                    "color: white;")
                self.AttackButton.setText('ЗАПУСК')
            else:
                Attackker.is_checking = True
                if signal.startswith('CheckingClient'):
                    self.AttackButton.setStyleSheet(
                        "font: 87 8pt \"Segoe UI Black\";\n"
                        "border-style: solid;\n"
                        "border-color: white;\n"
                        "border-radius: 5;\n"
                        "background-color: rgb(237,66,212);\n"
                        "color: white;")
                    signal = signal.replace('CheckingClient ', '')
                    signal = signal.split(',')
                    now = int(signal[0])
                    total = int(signal[1])
                    self.AttackButton.setText(f'ПРОВЕРКА {now}/{total}')

        def OpenLogsWindow(self):
            if not Data.LogsWindowIsOpened:
                global LogsWindowClassdublicate
                LogsWindowClassdublicate = LogsWindowClass()
                LogsWindowClassdublicate.show()

        def AttackButtonHover(self, event):
            if not self.is_attack:
                if event == 'enterEvent':
                    self.AttackButton.setStyleSheet(
                        "font: 87 8pt \"Segoe UI Black\";\n"
                        "border-style: solid;\n"
                        "border-color: white;\n"
                        "border-radius: 5;\n"
                        "background-color: rgb(72,84,200);\n"
                        "color: white;")
                else:
                    self.AttackButton.setStyleSheet(
                        "font: 87 8pt \"Segoe UI Black\";\n"
                        "border-style: solid;\n"
                        "border-color: white;\n"
                        "border-radius: 5;\n"
                        "background-color: rgb(88,101,242);\n"
                        "color: white;\n")
            else:
                if event == 'enterEvent':
                    self.AttackButton.setStyleSheet(
                        "font: 87 8pt \"Segoe UI Black\";\n"
                        "border-style: solid;\n"
                        "border-color: white;\n"
                        "border-radius: 5;\n"
                        "background-color: rgb(200, 0, 0);\n"
                        "color: rgb(255, 255, 255);")
                else:
                    self.AttackButton.setStyleSheet(
                        "font: 87 8pt \"Segoe UI Black\";\n"
                        "border-style: solid;\n"
                        "border-color: white;\n"
                        "border-radius: 5;\n"
                        "background-color: rgb(255, 0, 0);\n"
                        "color: rgb(255, 255, 255);")

        def LogsButtonHover(self, event):
            if event == 'enterEvent':
                self.ShowLogs.setStyleSheet(
                    "font: 87 8pt \"Segoe UI Black\";\n"
                    "border-style: solid;\n"
                    "border-color: white;\n"
                    "border-radius: 5;\n"
                    "background-color: rgb(55,134,80);\n"
                    "color: white;\n")
            else:
                self.ShowLogs.setStyleSheet(
                    "font: 87 8pt \"Segoe UI Black\";\n"
                    "border-style: solid;\n"
                    "border-color: white;\n"
                    "border-radius: 5;\n"
                    "background-color: rgb(59,165,93);\n"
                    "color: white;")

    class ApplicationWindow(ApplicationMainWindow):

        def __init__(self):
            super().__init__()
            self.InitializeWindow(self)

        def closeEvent(self, *args):
            _exit(0)

    if __name__ == "__main__":
        Application = QtWidgets.QApplication(argv)
        Window = ApplicationWindow()
        Window.show()
        _exit(Application.exec_())
    else:
        print('Error: Name is not __main__, close.')
        exit(1)
except Exception as e:
    import os

    if os.name != 'nt':
        print('WINDOWS ONLY')
        os._exit(1)

    from ctypes import windll

    MessageInfo = f'''Кажется, программа вылетела или вообще не смогла запуститься.
    
Тип ошибки: {type(e)}
Комментарий ошибки: {e}

Если вы запустили программу EXE, не в виде скрипта, и не модифицировали, свяжитесь с создателем программы - Its-MatriX#6770

Если вы скачали исходный код, и что-то модифицировали, либо скачайте исходный код заного, либо исправьте ошибку.

Если вы модифицировали EXE файл (сжимали, редактировали resource hacker'ом) и проводили другие манипуляции, скачайте программу заново.

Обратите внимание, что версии windows 7 и ниже - не поддерживаются. Если это не так, напишите об этом создателю программы.'''

    windll.user32.MessageBoxW(0, MessageInfo, 'Произошла ошибка', 0x10)
