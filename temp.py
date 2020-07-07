#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QApplication,
                             QMessageBox, QSystemTrayIcon,
                             QMenu, QAction, QStyle)
from PyQt5.QtCore import pyqtSlot, QTimer, QPoint
from PyQt5.QtGui import QCursor

__doc__ = '''PyQt5 Timer example'''


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        # Подключим слоты для реакции на
        # Нажатие кнопки по значку в панеле управления
        self.activated.connect(self.icon_activated_slot)
        # Нажатие по сообщению
        self.messageClicked.connect(self.message_clicked_slot)
        # Покажем одну из стандартных иконок
        self.setIcon(QApplication.style().standardIcon(QStyle.SP_DriveDVDIcon))

        self._counter = 0
        # Создаём таймер и присваиваем в локальную переменную класса
        self._timer = QTimer()
        # Задаём интервал в милисекундах
        self._timer.setInterval(1000)
        # Подсоединяем слот, куда таймер будет слать сообщения
        self._timer.timeout.connect(self.recurring_timer)
        self._timer.start()
        self.create_menu()

    def create_menu(self):
        """Создадим меню
        Внимание:
        QSystemTrayIcon не владеет ContextMenu,
        а потому не может быть в роли parent!"""
        # Может оно и лишнее в локальную переменную сохранять
        _menu = QMenu()

        startA = QAction("Start Timer", _menu)
        startA.triggered.connect(self._timer.start)
        _menu.addAction(startA)

        stopA = QAction("Stop timer", _menu)
        stopA.triggered.connect(self._timer.stop)
        _menu.addAction(stopA)
        

        quiteA = QAction("Exit", _menu)
        quiteA.triggered.connect(self.exit_slot)
        _menu.addAction(quiteA)
        self._menu = _menu
        self.setContextMenu(self._menu)

    @pyqtSlot()
    def exit_slot(self):
        print('exit_slot')
        # Зададим пользователю вопрос
        reply = QMessageBox.question(None, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Пользователь сказал "да, хочу выйти"
            self._timer.stop()
            self._menu.deleteLater()
            # Одобряем выход
            # Скрываем себя, а то ОС часто долго не обновляет панель
            self.hide()
            QApplication.instance().exit(0)

    @pyqtSlot()
    def recurring_timer(self):
        print('recurring_timer')
        self._counter = self._counter + 1
        msg = "Counter: {}".format(self._counter)
        # Укажем сообщение, которое показывать при наведении мышкой
        # на иконку
        self.setToolTip(msg)
        # почему-то следующее не работает(
        if self.supportsMessages():
            self.showMessage("MyTimer", msg, QSystemTrayIcon.Information, 1000)

    #@pyqtSlot(int)
    def icon_activated_slot(self, reason):
        """Кликнули по иконке в панеле управления"""
        print('icon_activated_slot')
        if reason == QSystemTrayIcon.Unknown:
            #неизвестно
            print('QSystemTrayIcon.Unknown')
            pass
        elif reason == QSystemTrayIcon.Context:
            #запрос контекстного меню
            print('QSystemTrayIcon.Context')
            pass
        elif reason == QSystemTrayIcon.DoubleClick:
            print('QSystemTrayIcon.DoubleClick')
            #двойной клие
            pass
        elif reason == QSystemTrayIcon.Trigger:
            print('QSystemTrayIcon.Trigger')
            # Клик по системному терю
            pass
        elif reason == QSystemTrayIcon.MiddleClick:
            # Нажата средняя кнопка мыши
            print('QSystemTrayIcon.MiddleClick')
            # Получим актуальную позицию мышки
            # Сдвинем на 50 пикселей по Х и У осям экрана вверх
            current_mouse_cursor = QCursor.pos() - QPoint(50, 50)
            # Запросим актуальное меню
            # Хотя могли бы и self._menu использовать
            menu = self.contextMenu()
            menu.popup(current_mouse_cursor)

    @pyqtSlot()
    def message_clicked_slot(self):
        """Кликнули по сообщению"""
        print("Кликнули по сообщению")

    def closeEvent(self, event):
        """Для иконки в трее не вызывается!"""
        # Зададим пользователю вопрос
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Пользователь сказал "да, хочу выйти"
            self._timer.stop()
            # уберём из локальных переменных класса,
            # чтобы кольцевые ссылки случайно не получились
            self._menu.deleteLater()
            # Одобряем выход
            # Скрываем себя, а то ОС часто долго не обновляет панель
            self.hide()
            event.accept()
        else:
            # отменяем запрос на выход
            event.ignore()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    my_tray = TrayIcon()
    my_tray.show()
    sys.exit(app.exec())