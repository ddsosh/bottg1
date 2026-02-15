from aiogram.fsm.state import StatesGroup, State


class AppState(StatesGroup):
    login = State()
    pas = State()

    main = State()

    movies_menu = State()
    notes_menu = State()

    add_movie_title = State()
    add_movie_type = State()
    add_movie_comment = State()
    delete_movie_number = State()

    add_note_title = State()
    add_note_date = State()
    delete_note_number = State()

