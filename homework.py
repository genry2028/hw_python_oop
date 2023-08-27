class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.training_type = training_type

    def get_message(self) -> str:
        """Вывод сообщения"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM * self.duration
                          * self.MIN_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CONSTANT_WLK_ONE = 0.035
    CONSTANT_WLK_TWO = 0.029
    KMH_IN_MSEC = 0.278
    SM_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed_ms: float = self.get_mean_speed() * self.KMH_IN_MSEC
        spent_calories = ((self.CONSTANT_WLK_ONE * self.weight
                          + (mean_speed_ms ** 2 / (self.height / self.SM_IN_M))
                          * self.CONSTANT_WLK_TWO * self.weight)
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    CONSTANT_SWM_ONE = 1.1
    CONSTANT_SWM_TWO = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.CONSTANT_SWM_ONE)
                          * self.CONSTANT_SWM_TWO * self.weight
                          * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_class = {'RUN': Running,
                   'WLK': SportsWalking,
                   'SWM': Swimming
                   }
    training: Training = train_class[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    info_message: str = info.get_message()
    print(info_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
