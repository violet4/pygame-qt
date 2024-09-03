import signal
from typing import Final, Tuple

import pygame

from pygame_qt import QHBoxLayout, QWidget, QSize, QVBoxLayout, QGridLayout, QPushButton, QApplication, QWindow


initial_window_size: Final[Tuple[int, int]] = (800, 600)
_max_fps: Final[int] = 60


class ButtonWindow(QWindow):
    def __init__(self, column_count: int, row_count: int,
                 button_width:int=50, button_height:int=50):
        super().__init__()
        padding = 15

        self.setWindowTitle("Custom GUI Window")
        self.setFixedSize(QSize(
            (button_width + padding * 2) + column_count,
            (button_height + padding * 2),
        ))

        self.buttonGrid = QHBoxLayout(self)
        button_size = QSize(button_width, button_height)

        if isinstance(self.buttonGrid, QHBoxLayout):
            for i in range(row_count):
                button = QPushButton(self)
                # x x y y x x y y ...
                if i % 4 < 2:
                    button.padX = padding
                else:
                    button.padY = padding
                button.setFixedSize(button_size)
                self.buttonGrid.addWidget(button)
        elif isinstance(self.buttonGrid, QGridLayout):
            for row in range(row_count):
                for col in range(column_count):
                    button = QPushButton(self)
                    button.setFixedSize(button_size)
                    self.buttonGrid.addWidget(button, row, col)

        self.setLayout(self.buttonGrid)
        self.resetSize()


def main() -> None:
    global _max_fps

    pygame.init()
    screen = pygame.display.set_mode(
        initial_window_size,
        flags=pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE,#|pygame.SCALED,
        vsync=1,  # maybe only works with pygame.SCALED?
    )
    clock = pygame.time.Clock()
    button_window = ButtonWindow(5, 10)
    button_window.show()
    app = QApplication([button_window])

    running = True
    while running:
        delta = clock.tick(_max_fps) / 1000.0
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            app.handle_input(event)
            if event.type == pygame.QUIT:
                print("Received QUIT signal.")
                running = False
            elif event.type == pygame.KEYDOWN:
                #TODO:send signal, which is subscribed to by player input handler
                pass
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if button_window.visible:
            #         button_window.hide()
            #     else:
            #         button_window.show()

        app.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
