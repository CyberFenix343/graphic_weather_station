import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from popup_window import AddSensorWindow
import json
from sensor import TemperatureSensor, HumiditySensor, PressureSensor, WindSensor, InsolationSensor, Sensor
from sensor_window import SensorWindow
WIN_WIDTH = 1000
WIN_HEIGHT = 800

TITLE = "Graphic Weather Station"

list_of_dicts = [
    {"name": "T1", "type": "Temperature", "interval": 700, "low_limit": -40, "high_limit": 60},
    {"name": "H1", "type": "Humidity", "interval": 900, "low_limit": 0, "high_limit": 100}]


class GraphicWeatherStation():
    zmiana = 0
    zmiana2 = 0
    sensor_windows = []
    sensor_windows.append(list_of_dicts)

    def __init__(self, root):

        self.root = root

        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+100+100")
        self.root.resizable(False, False)

        self.root.title(TITLE)

        self.__menubar = tk.Menu(self.root)
        self.__file_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__file_menu2 = tk.Menu(self.__menubar, tearoff=0)

        self.__menubar.add_cascade(label="File", menu=self.__file_menu)
        self.__menubar.add_cascade(label="Sensor", menu=self.__file_menu2)
        self.root.config(menu=self.__menubar)
        self.__file_menu.add_command(label="Save as", command=self.save_file)
        self.__file_menu.add_command(label='Open', command=self.open_file)
        self.__file_menu2.add_command(label='Add', command=self.add_sensor)
        self.__file_menu2.add_command(label='Remove', command=self.remove_sensor)

        self.tryb()
        self.tryb2()
        self.create_sensor_windows()

    def add_sensor(self):
        child = AddSensorWindow(self.root, self.add_sensor_callback, list_of_dicts)
        child.grab_set()
        self.tryb2()

    def remove_sensor(self):
        self.tryb2()
        for i in range(0, len(self.sensor_windows)-1):
            # Usuwa sensor z listy
            removed_sensor = self.sensor_windows.pop()
            removed_sensor.destroy()  # Usuwa sensor z widoku

    def save_file(self):
        try:
            filetypes = (

                ('conf files', '*.cfg'),
                ('conf files', '*.cfg')

                )
            filet = fd.asksaveasfilename(
                title='Save as...',
                initialdir='',
                filetypes=filetypes)

            if filet:
                if not filet.endswith(".cfg"):
                    raise ValueError

            with open(filet, 'w')as file:
                json.dump(list_of_dicts, file, indent=4)
                self.tryb()
        except ValueError as v:
            print(f"Błąd podczas zapisywania {filet}{v}")
        except Exception as f:
            # W przypadku błędu wyświetlamy komunikat o błędzie.
            print(f"Error during save: {f}")

        finally:

            pass

    def open_file(self):
        try:
            filetypes = (
                ('conf files', '*.cfg'),
                ('conf files', '*.cfg')
                )
            filet = fd.askopenfilename(
                title='Open a file',
                initialdir='',
                filetypes=filetypes)

            if not filet.endswith(".cfg"):
                raise ValueError

            if filet is not None:
                with open(filet, 'r')as file:
                    content = json.load(file)
                    print("File content:")
                    print(json.dumps(content, indent=4))
                    self.tryb()
            else:
                with open(filet, 'r')as file:
                    content = "Nie wczytano pliku lub plik jest pusty"
                    print("File content:")
                    print(json.dumps(content, indent=4))

        except ValueError as v:
            print(f"Błąd podczas otwierania {filet}{v}")
        except Exception as f:
            # W przypadku błędu wyświetlamy komunikat o błędzie.
            print(f"Error during opening a file: {f}")

        finally:
            pass

    def tryb(self):
        if self.zmiana == 0:
            self.__file_menu.entryconfig("Open", state=tk.DISABLED)
            self.__file_menu.entryconfig("Save as", state=tk.NORMAL)
            self.zmiana = 1
        else:
            self.__file_menu.entryconfig("Open", state=tk.NORMAL)
            self.__file_menu.entryconfig("Save as", state=tk.DISABLED)
            self.zmiana = 0

    def tryb2(self):
        if self.zmiana2 == 0:
            self.__file_menu2.entryconfig("Add", state=tk.NORMAL)
            self.__file_menu2.entryconfig("Remove", state=tk.DISABLED)
            self.zmiana2 = 1
        else:
            self.__file_menu2.entryconfig("Add", state=tk.DISABLED)
            self.__file_menu2.entryconfig("Remove", state=tk.NORMAL)
            self.zmiana2 = 0
            
    # Funkcja tworząca wykres nowo powstalego sensora

    def add_sensor_callback(self, sensor_params):
        print('Callback with sensor parameters:', sensor_params)

        # Tworzymy obiket sensor na podstawie podanych parametrow
        sensor_name = sensor_params['name']
        sensor_type = sensor_params['type']
        interval = sensor_params['interval']
        low_limit = sensor_params['low_limit']
        high_limit = sensor_params['high_limit']

        # Wybieramy klase sensora na podstawie jego typu
        sensor_class = Sensor.to_sensor(sensor_type)

        # Tworzy instancje klasy sensora
        new_sensor = sensor_class(low_limit, high_limit)

        list_of_dicts.append({"name": sensor_name, "type": sensor_type, "interval": interval, "low_limit": low_limit, "high_limit": high_limit})

        # Tworzymy obiekt SensorWindow i dodajemy go do listy sensorów
        sensor_window = SensorWindow(self.root, new_sensor, sensor_name, interval, 600, 200)
        sensor_window.pack()
        self.sensor_windows.append(sensor_window)

    # Funkcja dodajaca pierwsze 2 wykresy 
    def create_sensor_windows(self):
        for sensor_params in list_of_dicts:
            sensor_name = sensor_params['name']
            sensor_type = sensor_params['type']
            interval = sensor_params['interval']
            low_limit = sensor_params['low_limit']
            high_limit = sensor_params['high_limit']
        
            sensor_class = Sensor.to_sensor(sensor_type)
            new_sensor = sensor_class(low_limit, high_limit)
            sensor_window = SensorWindow(self.root, new_sensor, sensor_name, interval, 600, 200)

            sensor_window.pack()

            self.sensor_windows.append(sensor_window)


if __name__ == '__main__':

    from main import main
    main()
