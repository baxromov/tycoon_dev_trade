import logging
import time
from typing import Optional, List, Callable, Union

from iqoptionapi.stable_api import IQ_Option

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
CALL = "call"
PUT = "put"
ACTIONS = {CALL: "call", PUT: "put"}


class BinaryTrader(IQ_Option):
    """
    ACTIVES: EURUSD
    interval: 1m
    data amount: 4
    """

    def __init__(self, email, password,
                 amount_list: Optional[list] = None,
                 data_amount: Optional[int] = None,
                 active: Optional[str] = None,
                 interval: Optional[int] = None,
                 expiration: Optional[int] = None):
        self.email = email
        self.password = password
        self.api = super().__init__(self.email, self.password)
        self.interval = interval  # 60  # 1m
        self.expiration = expiration  # 1  # 1m
        self.active = active  # 'EURUSD'
        self.data_amount = data_amount + 1  # 4  кандалов
        self.amount_list = amount_list  # [1, 2.2, 4.84, 10.65]

    def connect(self, sms_code=None):
        """
            Подключение
        """
        logging.info('Подключение')
        return super().connect()

    def change_balance(self, mode: Optional[str]) -> Optional[None]:
        """
        PRACTICE: Практический режим
        REAL: Реальный режим
        :param mode:
        :type mode:
        :return:
        :rtype:
        """
        logging.info('Изменение режима')
        return super(BinaryTrader, self).change_balance(mode)

    def get_candles(self, ACTIVES=None, interval=None, count=None, endtime=None) -> Optional[List]:
        """
            Получение кандалов
        """
        logging.info('Получение кандалов')
        return super().get_candles(ACTIVES=self.active, interval=self.interval, count=self.data_amount,
                                   endtime=time.time())

    def get_color(self, data: Optional[list]) -> Optional[List[int]]:
        """
        Получение цвета по данным
        """
        logging.info('Получение цвета по данным')
        temp = []
        color = []
        for value in data:
            temp.append((value.get('open'), value.get('close')))
        for iten in temp:
            if iten[0] > iten[1]:
                color.append(0)
            elif iten[0] < iten[1]:
                color.append(1)
        return color

    def is_all_candles_red_or_green(self, data: Optional[list]) -> Optional[bool]:
        """
        Проверка на все кандалы красные или зеленые
        """
        logging.info('Проверка на все кандалы красные или зеленые')
        green = data[:-1].count(1)
        red = data[:-1].count(0)
        if green == len(data[:-1]):
            logging.info('Все кандалы зеленые')
            return True
        elif red == len(data[:-1]):
            logging.info('Все кандалы красные')
            return False
        else:
            logging.info('Не все кандалы красные или зеленые')
            return None

    def buy(self, price: Optional[float], ACTIVES: Optional[str] = None, ACTION: Optional[str] = None,
            expirations: Optional[int] = 0) -> Optional[int]:
        """
            Покупка
        """
        logging.info('Покупка')
        ACTION = ACTIONS[CALL]
        ACTIVES = self.active
        expirations = self.expiration
        check, id = super().buy(price, ACTIVES, ACTION, expirations)
        return id

    def sell(self, price: Optional[float]) -> Optional[int]:
        """
            Продажа
        """
        logging.info('Продажа')
        check, id = super().buy(price, ACTIVES=self.active, ACTION=ACTIONS[PUT], expirations=self.expiration)
        return id

    def check_win(self, id_order: Optional[int]) -> Optional[float]:
        """
            Проверка на выигрыш
        """
        logging.info('Проверка на выигрыш')
        k, win = super(BinaryTrader, self).check_win_v4(id_order)
        return win

    def is_out_of_range(self, data: Optional[list], index: Optional[int]) -> Union[tuple]:
        """
            Проверка на выход за пределы диапазона
        """
        logging.info('Проверка на выход за пределы диапазона')
        try:
            a = data[index]
            return False, a
        except IndexError:
            return True, None

    def martingale_strategy(self, win: Optional[float], active: Optional[Callable], timeout: Optional[int]) -> Optional[
        List[float]]:
        """
            Мартингейл
            timeout - время ожидания после покупки (s)
        """
        logging.info('Мартингейл')
        profit = [0]
        if win > 0:
            logging.info('Выигрыш(Мартингейл)')
            profit.append(win)
            time.sleep(timeout * 60)
            return profit
        else:
            logging.info('Проигрыш(Мартингейл)')
            count = 0
            _amount_list = self.amount_list[1:]
            while True:
                if win <= 0:
                    flag, price = self.is_out_of_range(_amount_list, count)
                    print(flag, price)
                    if flag:
                        profit.append(win)
                        time.sleep(timeout * 60)
                        return profit
                    order_id = active(price)
                    win = self.check_win(order_id)
                    count += 1
                    print(win)
                    profit.append(win)
                    if win > 0:
                        time.sleep(timeout * 60)
                        logging.info('Выигрыш(Мартингейл)')
                        return profit

    @property
    def stop_minus_loss(self) -> Optional[float]:
        """
            Стоп лосс
        """
        logging.info('Стоп лосс')
        data = self.amount_list
        return sum(data) * -1

    @property
    def stop_plus_loss(self) -> Optional[float]:
        """
            Стоп лосс
        """
        logging.info('Стоп лосс')
        data = self.amount_list
        return sum(data) / 3
