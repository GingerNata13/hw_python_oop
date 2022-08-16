

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {round(self.duration,3)}; '
                f'Дистанция: {round(self.distance,3)}; '
                f'Ср. скорость: {round(self.speed, 3)} км/ч; '
                f'Потрачено ккал: {round(self.calories, 3)}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    def __init__(self,
                 action: int = 5300,
                 duration: float = 1,
                 weight: float = 90
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        #print(self.action * Training.LEN_STEP / Training.M_IN_KM)
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        #print(self.get_distance() / self.duration)
        return self.get_distance() / self.duration

# x = Training().get_mean_speed()
# print(x)

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

# x2 = Training().show_training_info()
# print(x2)

class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        k1: int = 18
        k2: int = 20
        return (k1 * self.get_mean_speed() - k2) * self.weight / Training.M_IN_KM * (self.duration * 60)

# x3 = Running().get_spent_calories()
# print(x3)

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int = 5300,
                 duration: float = 1,
                 weight: float = 90,
                 height: float = 175
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        k3 = 0.035
        k4 = 0.029
        """Получить количество затраченных калорий."""
        return (k3 * self.weight + (self.get_mean_speed() ** 2 // self.height) * k4 * self.weight) * (self.duration * 60)

    #округление результата?

# x4 = SportsWalking().get_spent_calories()
# print(x4)

class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    def __init__(self,
                 action: int = 5300,
                 duration: float = 1,
                 weight: float = 90,
                 length_pool: float = 25,
                 count_pool: int = 20
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / Training().M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        k5 = 1.1
        k6 = 2
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + k5) * k6 * self.weight


# x5 = Swimming().get_mean_speed()
# print(x5)
# x6 = Swimming().get_spent_calories()
# print(x6)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict = dict(RUN=Running, WLK=SportsWalking, SWM=Swimming)
    class_type = workout_dict[workout_type]
    return class_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = InfoMessage.get_message(training.show_training_info())
    print (info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)



