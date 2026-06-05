from aiogram.fsm.state import State, StatesGroup


class AddMovie(StatesGroup):
    """Kino qo'shish states"""
    title = State()
    file = State()
    trailer = State()
    confirm = State()


class EditMovie(StatesGroup):
    """Kino tahrirlash states"""
    select = State()
    field = State()
    new_value = State()


class DeleteMovie(StatesGroup):
    """Kino o'chirish state"""
    select = State()


class Broadcast(StatesGroup):
    """Broadcast states"""
    message = State()
    confirm = State()


class ManageChannels(StatesGroup):
    """Kanallar boshqaruvi states"""
    action = State()
    channel_id = State()
