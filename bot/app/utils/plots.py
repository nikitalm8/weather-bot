import time
import random

from app.database.models import User

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio.session import AsyncSession

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.axes import Axes


class BasePlotCreator(object):

    DAY = 60 * 60 * 24
    DAYS = 20
    WIDTH = 10

    LABEL_Y = 'Данные'

    TITLE_TEMPLATE = 'Статистика c %s по %s'

    PATH = 'plot.png'


    @staticmethod
    def splitting(value: int) -> str:

        if value == 0:

            return ''

        return '%.1fk' % (value / 1000)


    @classmethod
    async def create_plot(cls, session: AsyncSession, unix_time: float=None) -> str:

        unix_time = unix_time or time.time()

        data = (await cls.get_data(session, unix_time))[::-1]
        figure, _ = cls.configure_axes(data, unix_time)

        figure.tight_layout()
        figure.savefig(cls.PATH)

        return cls.PATH


    @staticmethod
    async def get_day(session: AsyncSession, unix_time: float) -> int:
        """
        Method to be remapped in child classes.
        """

        return random.randint(500, 1000)


    @classmethod
    def get_offsets(cls, unix_time: float) -> list:

        for days in range(cls.DAYS):

            yield unix_time - (cls.DAY * days)


    @classmethod
    async def get_data(cls, session: AsyncSession, unix_time: float) -> list:

        return [
            await cls.get_day(session, offset)
            for offset in cls.get_offsets(unix_time)
        ]


    @classmethod
    def _create_row(cls, axes: Axes, data: list, color: str, max_value: int, label: str, offset: float=0, width: float=0.4, bottom: bool=False, splitting: bool=False):

        positions = [
            position + offset
            for position in
            range(len(data))
        ]

        axes.bar(
            positions, 
            data, 
            color=color, 
            width=width, 
            alpha=1,
        )

        for index, value in enumerate(data):

            axes.text(
                index + offset, 
                (
                    value + (max_value * 0.02)
                    if not bottom else
                    -(max_value * 0.035)
                ), 
                (
                    cls.splitting(value) 
                    if splitting else
                    value if value else ''
                ), 
                horizontalalignment='center',
                color=color, 
                fontsize=(
                    10 if not bottom else 9
                ),
            )


    @classmethod
    def create_bars(cls, axes: Axes, data: list, max_value: int):
        """
        Method to be remapped in child classes.
        """

        cls._create_row(
            axes, data, '#645fd5', max_value, 'Число',  bottom=True,
        )

        axes.legend(
            handles=(
                mpatches.Patch(
                    color='#645fd5', 
                    label='Число',
                ),
            )
        )


    @classmethod
    def configure_axes(cls, data: list, unix_time: float):

        date_labels = [
            time.strftime('%d.%m', time.localtime(offset))
            for offset in cls.get_offsets(unix_time)
        ][::-1]

        max_value = max(data)

        if isinstance(max_value, tuple):

            max_value = max(max_value)

        figure, axes = plt.subplots(
            figsize=(cls.WIDTH, 6), 
            facecolor='white', 
            dpi=100,
        )

        axes.set_xticks(
            range(len(data)),
            date_labels,
            fontsize=10,
            rotation=60, 
            horizontalalignment='center', 
        )
        axes.set_title(
            cls.TITLE_TEMPLATE % (
                date_labels[-1],
                date_labels[0],
            ),
            fontsize=18,
        )
        axes.set(
            ylabel=cls.LABEL_Y,
        )
        axes.set_ylim(-max_value * 0.05, max_value * 1.1)

        cls.create_bars(axes, data, max_value)

        return figure, axes


class UsersPlot(BasePlotCreator):

    LABEL_Y = 'Количество'
    PATH = 'app/src/users_plot.png'


    @classmethod
    async def get_day(cls, session: AsyncSession, unix_time: float) -> tuple:

        return (
            await session.scalar(
                select(func.count(1))
                .where(
                    User.join_date.between(
                        unix_time - cls.DAY,
                        unix_time,
                    ),
                    User.block_date == 0,
                )
            ),
            await session.scalar(
                select(func.count(1))
                .where(
                    User.block_date.between(
                        unix_time - cls.DAY,
                        unix_time,
                    ),
                )
            ),
        )


    @classmethod
    def create_bars(cls, axes: Axes, data: list, max_value: int):

        active = [
            item[0] for item in data
        ]
        block = [
            item[1] for item in data
        ]

        cls._create_row(
            axes, active, '#645fd5', max_value, 'Пользователи', offset=0.3, splitting=True,
        )
        cls._create_row(
            axes, block, '#ae1311', max_value, 'Заблокированные', offset=-0.1, width=0.2, bottom=True, splitting=True,
        )

        axes.legend(
            handles=(
                mpatches.Patch(
                    color='#645fd5', 
                    label='Пользователи',
                ),
                mpatches.Patch(
                    color='#ae1311', 
                    label='Заблокированные',
                ),
            )
        )
