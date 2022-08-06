from dataclasses import dataclass
from typing import ClassVar, Dict, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    info_message: ClassVar[str] = ('Тип тренировки: {0}; '
                                   'Длительность: {1:.3f} ч.; '
                                   'Дистанция: {2:.3f} км; '
                                   'Ср. скорость: {3:.3f} км/ч; '
                                   'Потрачено ккал: {4:.3f}.')
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить строку сообщения."""
        return self.info_message.format(self.training_type,
                                        self.duration,
                                        self.distance,
                                        self.speed,
                                        self.calories)


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_speed_1: int = 18
        coeff_speed_2: int = 20
        in_minutes = self.duration * 60
        return ((coeff_speed_1 * self.get_mean_speed() - coeff_speed_2)
                * self.weight / self.M_IN_KM * in_minutes)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_weight_1: float = 0.035
        coeff_weight_2: float = 0.029
        coeff_speed: int = 2
        in_minutes = self.duration * 60
        return ((coeff_weight_1 * self.weight
                + (self.get_mean_speed()**coeff_speed // self.height)
                * coeff_weight_2 * self.weight) * in_minutes)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_speed: float = 1.1
        coeff_weight: int = 2
        return ((self.get_mean_speed() + coeff_speed)
                * coeff_weight * self.weight)


def read_package(workout_type: str, data: list) -> Union[Training, None]:
    """Прочитать данные полученные от датчиков."""
    training_data: Dict[str, type] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking}
    if workout_type in training_data:
        training = training_data[workout_type]
        return training(*data)
    else:
        return None


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training is None:
            print('Тренировка не распознана')
        else:
            main(training)
