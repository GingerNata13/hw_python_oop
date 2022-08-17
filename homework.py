class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.'
                        )

        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        k1: int = 18
        k2: int = 20
        m_in_h: int = 60
        calories_part1 = (k1 * self.get_mean_speed() - k2)
        calories_part2 = self.weight / self.M_IN_KM * (self.duration * m_in_h)
        calories: float = calories_part1 * calories_part2
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # K1: float = 0.035
    # K2: float = 0.029
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        k1: float = 0.035
        k2: float = 0.029
        k3: int = 2
        m_in_h: int = 60
        """Получить количество затраченных калорий."""
        calories_part0 = self.get_mean_speed() ** k3 // self.height
        calories_part1 = k1 * self.weight + calories_part0 * k2 * self.weight
        calories_part2 = self.duration * m_in_h
        calories: float = calories_part1 * calories_part2
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_part1 = self.length_pool * self.count_pool
        speed_part2 = self.M_IN_KM
        speed_part3 = self.duration
        speed: float = speed_part1 / speed_part2 / speed_part3
        return speed

    def get_spent_calories(self) -> float:
        k1: float = 1.1
        k2: int = 2
        """Получить количество затраченных калорий."""
        calories: float = (self.get_mean_speed() + k1) * k2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict = dict(RUN=Running, WLK=SportsWalking, SWM=Swimming)
    class_type = workout_dict[workout_type]
    return class_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    # info = InfoMessage.get_message(training.show_training_info())
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
