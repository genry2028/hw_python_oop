from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    INFO_MESSAGE: str = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.training_type = training_type

    def get_message(self) -> str:
        """Вывод сообщения"""
        return self.INFO_MESSAGE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories,
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CONSTANT_WLK_ONE: float = 0.035
    CONSTANT_WLK_TWO: float = 0.029
    KMH_IN_MSEC: float = 0.278
    SM_IN_M: int = 100

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.CONSTANT_WLK_ONE * self.weight
                + (
                    (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.SM_IN_M)
                )
                * self.CONSTANT_WLK_TWO
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    CONSTANT_SWM_ONE: float = 1.1
    CONSTANT_SWM_TWO: int = 2
    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CONSTANT_SWM_ONE)
            * self.CONSTANT_SWM_TWO
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list[int, float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_class: Dict[str, Type[Training]] = {
        "RUN": Running,
        "WLK": SportsWalking,
        "SWM": Swimming,
    }
    if not isinstance(workout_type, str):
        raise ValueError("А здесь понятный текст, что пошло нет так")
    return train_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    info_message: str = info.get_message()
    print(info_message)


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
