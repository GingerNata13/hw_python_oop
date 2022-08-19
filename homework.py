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
        """Но имеет ли смысл message объявлять тут? - Данная переменная
        действительно лишняя и изначально её не было, но при отпрвке кода
        Вам на проверку выскакивала ошибка: get_message() должна возвращать тип str,
        хотя def get_message(self) -> str: было прописано, решилась данная проблема
        только добавлением переменной message. Посмотрим пропустит ли проверка в этот
        раз ))."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

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
    """Константы вывела, так тоже было изначально (о чём свидетельствали
    мои забытые в комментах части кода)), но потом мне показалось, что это 
    сильно "утежеляет" код, особенно при дальнейшем описании формул ввиду 
    ограничения строк <79 символов, я из-за этого ограничения и так несколько 
    раз ошибалась в них, а после вывода констант строки становятся ещё длиннее."""
    K_1: int = 18
    K_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        """Здесь и далее попыталась дать вспомогательным переменым более
        осмысленные названия, но у меня не везде получилось"""
        cal_f_part1 = (self.K_1 * self.get_mean_speed() - self.K_2) * self.weight
        duration_in_min = self.duration * self.M_IN_H
        calories: float = cal_f_part1 / self.M_IN_KM * duration_in_min
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1: float = 0.035
    K_2: float = 0.029
    K_3: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cal_f_part1 = self.get_mean_speed() ** self.K_3 // self.height
        cal_f_part2 = self.K_1 * self.weight + cal_f_part1 * self.K_2 * self.weight
        duration_in_min = self.duration * self.M_IN_H
        calories: float = cal_f_part2 * duration_in_min
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    K_1: float = 1.1
    K_2: int = 2

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
        pool_distance = self.length_pool * self.count_pool
        speed: float = pool_distance / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (self.get_mean_speed() + self.K_1) * self.K_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict = dict(RUN=Running, WLK=SportsWalking, SWM=Swimming)
    class_type = workout_dict[workout_type]
    return class_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    """Сделала проверку на KeyError, Вы предлагали это сделать в read_package(), 
    но там я не справилась с дальнейшей передачей данных в переменную training,
    в случае KeyError, поэтому решила сразу её проверять."""

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except KeyError:
            print('Указан неверный тип тренировки.')

    """Отдельное спасибо за комплименты в адрес пары решений в моём коде!
    Он мне дался совсем не просто во второй половине, а в Слак заглядывалать
    не хотелось, чтоб случайно чужое не списать."""

    """P.S. Напишите мне, пожалуйста, на будущее, если оставлять такие комментарии 
    непосредственно в коде нельзя."""
