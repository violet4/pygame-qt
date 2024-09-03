from dataclasses import dataclass
from re import X
from typing import Any, Generic, Optional, Sequence, Tuple, TypeVar, List, Union
import enum
import random

from pygame import Event, Rect, Surface
import pygame

T = TypeVar('T')


def create_2d_array(num_rows: int, num_cols: int) -> List[List[None]]:
    """
    Creates a 2D array (list of lists) with the specified number of rows and columns,
    initializing all elements to the specified initial value.

    Parameters:
    num_rows (int): Number of rows in the 2D array.
    num_cols (int): Number of columns in each row of the 2D array.
    initial_value (any, optional): Initial value for each element of the 2D array. Defaults to None.

    Returns:
    list: A 2D list with the specified dimensions and initial values.
    """
    return [[None for _ in range(num_cols + 1)] for _ in range(num_rows + 1)]


class Array(Generic[T]):
    _elements: List[List[T|None]]
    _w: int
    _h: int

    def __init__(self, w:int, h:int) -> None:
        self._w = w
        self._h = h
        self._elements = create_2d_array(w, h)  # type: ignore

    def __getitem__(self, s:Tuple[int,int]) -> T|None:
        if s[0] > self._w - 1 or s[1] > self._h - 1:
            return None
        ele: T|None = self._elements[s[0]][s[1]]
        return ele

    def __setitem__(self, s:Tuple[int,int], value:T|None) -> None:
        w, h = s
        if w > self._w or h > self._h:
            self._w = max(w, self._w)
            self._h = max(h, self._h)
            new_elements: List[List[T|None]] = create_2d_array(self._w, self._h)  # type: ignore
            for i in range(len(self._elements)):
                for j in range(len(self._elements[0])):
                    new_elements[i][j] = self._elements[i][j]
            self._elements = new_elements

        self._elements[s[0]][s[1]] = value


def generate_random_hex() -> str:
    random_number = random.randint(0, 0xFFFFFF)
    return f"#{random_number:06x}"


class AlignmentFlag(enum.IntFlag):

    AlignLeading             = 0x1
    AlignLeft                = 0x1
    AlignRight               = 0x2
    AlignTrailing            = 0x2
    AlignHCenter             = 0x4
    AlignJustify             = 0x8
    AlignAbsolute            = 0x10
    AlignHorizontal_Mask     = 0x1f
    AlignTop                 = 0x20
    AlignBottom              = 0x40
    AlignVCenter             = 0x80
    AlignCenter              = 0x84
    AlignBaseline            = 0x100
    AlignVertical_Mask       = 0x1e0


class QPainter:
    pass


class QPaintDevice(object):

    class PaintDeviceMetric(enum.Enum):

        PdmWidth                  = 0x1
        PdmHeight                 = 0x2
        PdmWidthMM                = 0x3
        PdmHeightMM               = 0x4
        PdmNumColors              = 0x5
        PdmDepth                  = 0x6
        PdmDpiX                   = 0x7
        PdmDpiY                   = 0x8
        PdmPhysicalDpiX           = 0x9
        PdmPhysicalDpiY           = 0xa
        PdmDevicePixelRatio       = 0xb
        PdmDevicePixelRatioScaled = 0xc

    def __init__(self) -> None:
        pass


class QGuiApplication:
    pass


class QApplication(QGuiApplication):
    _widgets: Sequence['QWidget']

    def __init__(self, widgets: Sequence['QWidget']) -> None:
        self._widgets = widgets

    def draw(self, screen:Surface) -> None:
        for widget in self._widgets:
            widget.draw(screen)

    def handle_input(self, event:Event) -> None:
        pass


class QSize:
    _w: int
    _h: int

    def __init__(self, w: int, h: int) -> None:
        self._w = w
        self._h = h


class QObject:
    pass


class QLayoutItem:
    _alignment: AlignmentFlag
    _rect: Rect

    def __init__(self, alignment: AlignmentFlag = AlignmentFlag.AlignCenter):
        self._alignment = alignment

    @property
    def geometry(self) -> Rect:
        return self._rect

    @geometry.setter
    def geometry(self, val: Rect) -> None:
        self._rect = val

    def sizeHint(self) -> QSize:
        return QSize(*self._rect.size)


class QLayout(QObject, QLayoutItem):
    _parent: 'Optional[QWidget|QLayout]'
    _widgets: List['QWidget']
    _layout: 'Optional[QLayout]'
    _width: int
    _height: int

    def __init__(self, parent:'Optional[QWidget|QLayout]'=None, *args:Any, **kwargs:Any):
        super().__init__(*args, **kwargs)
        self._parent = parent
        self._widgets = []
        self._layout = None
        self._width = 0
        self._height = 0

    def addLayout(self, layout:'QLayout') -> None:
        assert self._layout is not None, "Can't add layout; layout already exists"
        self._layout = layout

    def addWidget(self, w:'QWidget') -> None:
        self._widgets.append(w)

    def draw(self, screen:Surface, x:int=0, y:int=0) -> None:
        pass

    def _max_widget_dimensions(self) -> Tuple[int, int]:
        max_x = 0
        max_y = 0
        for child in self._widgets:
            max_x = min(max_x, child._rect.size[0])
            max_y = min(max_y, child._rect.size[1])
        return max_x, max_y

    def resetSize(self) -> None:
        pass

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height


class QBoxLayout(QLayout):

    def __init__(self, *args:Any, width:int=0, height:int=0, **kwargs:Any):
        super().__init__(*args, **kwargs)
        self._width = width
        self._height = height


class QHBoxLayout(QBoxLayout):

    def resetSize(self) -> None:
        width = 0
        height = 0
        for child in self._widgets:
            width = max(width, child.width + sum(child.padX))
            height += child.height + sum(child.padY)
        self._width = width
        self._height = height

    def draw(self, screen:Surface, x:int=0, y:int=0) -> None:
        for child in self._widgets:
            new_y = child.sizeHint._h
            y += child._padTop
            child.draw(screen, x + child._padLeft, y)
            y += new_y + child._padBottom


class QVBoxLayout(QBoxLayout):

    def resetSize(self) -> None:
        width = 0
        height = 0
        for child in self._widgets:
            width += child.width + sum(child.padX)
            height = max(height, child.height + sum(child.padY))
        self._width = width
        self._height = height

    def draw(self, screen:Surface, x:int=0, y:int=0) -> None:
        for child in self._widgets:
            new_x = child.sizeHint._w
            x += child._padLeft
            child.draw(screen, x, y + child._padTop)
            x += new_x + child._padRight


class QSizePolicy:
    pass


class QWidget(QObject, QPaintDevice):
    _parent: 'Optional[QWidget]'
    _title: str
    _layout: Optional[QLayout]
    _visible: bool
    _rect: Rect
    _color: str
    _size: QSize
    _disabled: bool
    _padLeft: int
    _padRight: int
    _padTop: int
    _padBottom: int

    def __init__(self, parent:Optional['QWidget']=None):
        self._parent = parent
        self._title = ''
        self._visible = True
        self._size = QSize(50, 50)
        self._rect = Rect(0, 0, self._size._h, self._size._w)
        self._color = generate_random_hex()
        self._disabled = False
        self._layout = None
        self._padLeft = 0
        self._padRight = 0
        self._padTop = 0
        self._padBottom = 0

    def update(self) -> None:
        if self._disabled:
            return

    @property
    def padding(self) -> Tuple[int, int, int, int]:
        return (
            self._padLeft,
            self._padRight,
            self._padTop,
            self._padBottom,
        )

    @padding.setter
    def padding(self, v1:Union[int, Tuple[int, int, int, int]]) -> None:
        if isinstance(v1, tuple):
            self._padLeft = v1[0]
            self._padRight = v1[1]
            self._padTop = v1[2]
            self._padBottom = v1[3]
        else:
            self._padLeft = v1
            self._padRight = v1
            self._padTop = v1
            self._padBottom = v1

    @property
    def padX(self) -> Tuple[int, int]:
        return (self._padLeft, self._padRight)

    @padX.setter
    def padX(self, x:Union[int, Tuple[int, int]]) -> None:
        if isinstance(x, int):
            self._padLeft = x
            self._padRight = x
        else:
            self._padLeft, self._padRight = x

    @property
    def padY(self) -> Tuple[int, int]:
        return (self._padLeft, self._padRight)

    @padY.setter
    def padY(self, y:Union[int, Tuple[int, int]]) -> None:
        if isinstance(y, int):
            self._padTop = y
            self._padBottom = y
        else:
            self._padTop, self._padBottom = y

    @property
    def width(self) -> int:
        return self._rect.width

    @property
    def height(self) -> int:
        return self._rect.height

    def layout(self) -> Optional[QLayout]:
        return self._layout

    @property
    def visible(self) -> bool:
        return self._visible

    def hide(self) -> None:
        self._visible = False

    def show(self) -> None:
        self._visible = True

    def setDisabled(self, disabled: bool) -> None:
        self._disabled = disabled

    @property
    def enabled(self) -> bool:
        return not self._disabled

    def setEnabled(self, enabled: bool) -> None:
        self._disabled = not enabled

    @property
    def sizeHint(self) -> QSize:
        return self._size

    def setWindowTitle(self, title: str) -> None:
        self._title = title

    def setFixedSize(self, size: QSize) -> None:
        self._rect.size = (size._w, size._h)
        self._size = size

    def setLayout(self, layout: QLayout) -> None:
        self._layout = layout

    def resetSize(self) -> None:
        if self._layout is not None:
            self._layout.resetSize()
            if self._layout.width > 0 and self._layout.height > 0:
                self._rect.size = (self._layout.width, self._layout.height)

    def _draw(self, screen:Surface, x:int, y:int) -> None:
        if not self._visible:
            return
        self._rect.topleft = (x, y)
        pygame.draw.rect(screen, self._color, self._rect)

    def draw(self, screen:Surface, x:int=0, y:int=0) -> None:
        if not self._visible:
            return
        self._draw(screen, x, y)
        if self._layout is not None:
            self._layout.draw(screen, x, y)


@dataclass
class QGridLayoutSizeTriple:
    minS: QSize
    hint: QSize
    maxS: QSize


# maybe someday. this is needed for widgets that span multiple grid slots.
class QGridBox:
    _item: QLayoutItem
    row: int
    col: int
    torow: int
    tocol: int

    def __init__(self, layout_item: QLayoutItem):
        self._item = layout_item

    def sizeHint(self) -> QSize:
        return self._item.sizeHint()


class QGridLayout(QLayout):
    _width: int
    _height: int
    _grid_widgets: Array['QWidget']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._width = 0
        self._height = 0
        self._grid_widgets = Array['QWidget'](0, 0)

    def addWidget(self, w: QWidget, row:Optional[int]=None, column:Optional[int]=None,
                  alignment: AlignmentFlag = AlignmentFlag.AlignCenter) -> None:
        """
        Adds a widget to the grid layout at the specified row and column.

        :param w: QWidget to add.
        :param row: The grid row index (0-based).
        :param column: The grid column index (0-based).
        :param alignment: Optional alignment flag.
        :raises TypeError: If `row` or `column` are None.
        """
        assert row is not None and column is not None, "row and column must be non-null"
        self._grid_widgets[row, column] = w


class QAbstractButton(QWidget):
    pass


class QPushButton(QAbstractButton):
    pass


class QWindow(QWidget):
    # https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow
    # The QWindow class represents a window in the underlying windowing system
    _x: int
    _y: int
    _active: bool
    _height: int
    _max_height: int
    _min_height: int
    _width: int
    _min_width: int
    _max_width: int
    _opacity: float

    def __init__(self) -> None:
        super().__init__()
        self._x = 0
        self._y = 0
        self._active = False

        self._height = 0
        self._min_height = 0
        self._max_height = 0

        self._width = 0
        self._min_width = 0
        self._max_width = 0

        self._opacity = 0.0
        self._visible = False
