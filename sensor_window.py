import tkinter as tk
from sensor import Sensor


class SensorWindow(tk.Canvas):
    def __init__(self, root, sensor, custom_name, interval, width, height):
        super().__init__(root, bg="white", width=width, height=height)

        self._root = root
        self._sensor = sensor
        self._custom_name = custom_name
        self._width = width
        self._height = height
        self._animation_interval = interval  # Milisekundy
        self._points_to_display = self._sensor.NUM_OF_MEASUREMENTS
        self._history_displayed = []

        self.after(self._animation_interval, self.draw_plot)

    def draw_plot(self):
        point_fill = "black"
        line_fill = "red"
        point_radius = 4
        line_width = 3
        title_height = 30
        legend_width = 50
        margin = 50

        self._sensor.update_history()

        self.delete("all")

        # Tytuł
        self.create_text(self._width // 2, 10, anchor=tk.N, text=self._custom_name, font=("Times New Roman", 12, "bold"))

        # Typ Sensora
        self.create_text(10, 10, anchor=tk.NW, text=self._sensor.name(), font=("Times New Roman", 12, "bold"))

        # Jednostka
        self.create_text(self._width - 10, 10, anchor=tk.NE, text=f"{self._sensor.unit()}", font=("Times New Roman", 10, "bold"))

        # High limit i Low limit
        self.create_text(self._width - 10, margin, anchor=tk.NE, text=f"{self._sensor.high_limit}", font=("Times New Roman", 10, "bold"))
        self.create_text(self._width - 10, self._height - margin - 15, anchor=tk.NE, text=f"{self._sensor.low_limit}", font=("Times New Roman", 10, "bold"))

        history = self._sensor.history

        # Jak długa ma być tablica history
        start_index = max(0, len(history) - self._points_to_display)
        self._history_displayed = history[start_index:]

        x_increment = (self._width - margin - legend_width) / self._points_to_display

        # Ustala gdzie konczy się wykres (Potrzebne do przerywanych linii tworzących granice)

        lower_limit_y = self._height - margin - ((self._sensor.low_limit - self._sensor.low_limit) / (self._sensor.high_limit - self._sensor.low_limit) * (self._height - 2 * margin))
        upper_limit_y = self._height - margin - ((self._sensor.high_limit - self._sensor.low_limit) / (self._sensor.high_limit - self._sensor.low_limit) * (self._height - 2 * margin))

        # Przerywane linie
        self.create_line(10, upper_limit_y, self._width - 10, upper_limit_y, fill="black", width=2, dash=(5, 5))
        self.create_line(10, lower_limit_y, self._width - 10, lower_limit_y, fill="black", width=2, dash=(5, 5))

        # Wykres
        for i in range(len(self._history_displayed) - 1):
            x1 = 10 + i * x_increment
            y1 = self._height - margin - ((self._history_displayed[i] - self._sensor.low_limit) / (self._sensor.high_limit - self._sensor.low_limit) * (self._height - 2 * margin))  # scaling for visualization
            x2 = 10 + (i + 1) * x_increment
            y2 = self._height - margin - ((self._history_displayed[i + 1] - self._sensor.low_limit) / (self._sensor.high_limit - self._sensor.low_limit) * (self._height - 2 * margin))

            # Linie
            self.create_line(x1, y1, x2, y2, fill=line_fill, width=line_width)

            # Punkty
            self.create_oval(x1 - point_radius, y1 - point_radius, x1 + point_radius, y1 + point_radius, fill=point_fill)
            self.create_oval(x2 - point_radius, y2 - point_radius, x2 + point_radius, y2 + point_radius, fill=point_fill)

        # Metoda after aby rysowac wykres w nieskończoność
        self.after(self._animation_interval, self.draw_plot)


if __name__ == '__main__':

    from main import main
    main()
