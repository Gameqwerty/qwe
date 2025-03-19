import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# Настройка GPIO
GPIO.setmode(GPIO.BCM)

# Определение пинов
DAC_PINS = [10, 9, 11, 5, 6, 13, 19, 26]
LED_PINS = [14, 15, 18, 23, 24, 25, 8, 7]
COMP_PIN = 4
TROIKA_PIN = 17

# Настройка пинов
GPIO.setup(DAC_PINS, GPIO.OUT)
GPIO.setup(LED_PINS, GPIO.OUT)
GPIO.setup(COMP_PIN, GPIO.IN)
GPIO.setup(TROIKA_PIN, GPIO.OUT)

# Функция для вывода двоичного представления числа на светодиоды
def display_binary(value)
    for i in range(8)
        GPIO.output(LED_PINS[i], (value  i) & 1)

# Функция для измерения напряжения на выходе тройка-модуля
def measure_voltage()
    return GPIO.input(COMP_PIN)

# Основной блок скрипта
try
    measurements = []
    start_time = time.time()

    # Зарядка конденсатора
    GPIO.output(TROIKA_PIN, GPIO.HIGH)
    while True
        voltage = measure_voltage()
        measurements.append(voltage)
        display_binary(voltage)
        if voltage = 0.97  3.3
            break
        time.sleep(0.01)

    # Разрядка конденсатора
    GPIO.output(TROIKA_PIN, GPIO.LOW)
    while True
        voltage = measure_voltage()
        measurements.append(voltage)
        display_binary(voltage)
        if voltage = 0.02  3.3
            break
        time.sleep(0.01)

    end_time = time.time()
    duration = end_time - start_time

    # Построение графика
    plt.plot(measurements)
    plt.xlabel('Measurement Number')
    plt.ylabel('Voltage (V)')
    plt.title('RC Circuit ChargingDischarging')
    plt.show()

    # Сохранение данных в файл
    with open('data.txt', 'w') as f
        for value in measurements
            f.write(f{value}n)

    # Сохранение настроек в файл
    sampling_rate = len(measurements)  duration
    adc_step = 3.3  255  # Предполагаем 8-битный АЦП
    with open('settings.txt', 'w') as f
        f.write(fSampling Rate {sampling_rate} Hzn)
        f.write(fADC Step {adc_step} Vn)

    # Вывод информации в терминал
    print(fTotal Duration {duration} s)
    print(fMeasurement Period {duration  len(measurements)} s)
    print(fAverage Sampling Rate {sampling_rate} Hz)
    print(fADC Step {adc_step} V)

finally
    # Сброс GPIO
    GPIO.output(DAC_PINS, GPIO.LOW)
    GPIO.output(LED_PINS, GPIO.LOW)
    GPIO.output(TROIKA_PIN, GPIO.LOW)
    GPIO.cleanup()