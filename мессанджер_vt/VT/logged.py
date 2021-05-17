import pygame
from class_ import *
import connected_user.user as user



def connection_user(connection: user.start, db: user.db):
    pygame.init()
    pygame.display.set_caption("Вход в VT")
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()
    err = None

    input_box1 = InputBox((100, 120, 0, 32), max_length=15, hidden_text="логин", copy=False)
    input_box2 = InputBox((100, 175, 0, 32), max_length=15, hidden_text="пароль", copy=False)

    text = Text((120, 50), 300, "Месанджер VT", FONT=pg.font.Font(None, 50), color_text=(100, 140, 100))

    button1 = Button((200, 230, 71, 34), "войти", "open_user")
    button2 = Button((120, 330, 251, 34), "создать пользователя", "go to func create_user")

    overflow = OverFlow((0, 0, 500, 500))
    overflow.add(button1, button2, text, input_box1, input_box2)

    _done = False

    while not _done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _done = True

            d = overflow.handle_event(event)
            try:
                err.handle_event(event)
            except:
                pass
            if not d is None:
                if d.type == "open_user":
                    answer = connection.spend({
                        "name": input_box1.text,
                        "password": input_box2.text,
                        "command": "open_user",
                        "path": "user"
                    })
                    try:
                        if answer["answer"] == "connected":
                            db.update({
                                "name": input_box1.text,
                                "password": input_box2.text
                            })
                            return True
                        else:
                            err = Text((120, 30), 300, answer["answer"], color_text=(230, 100, 100))
                    except:
                        err = Text((140, 30), 300, answer, color_text=(230, 100, 100))
                if d.type == "go to func create_user":
                    a = create_user(connection, db)
                    if not a is False:
                        return a
                    else:
                        input_box1.text = ""
                        input_box2.text = ""

        overflow.update()
        try:
            err.update()
        except:
            pass
        screen.fill((0, 0, 0))

        screen = overflow.draw(screen)
        try:
            screen = err.draw(screen)
        except:
            pass
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return None


def create_user(connection: user.start, db: user.db):
    pygame.init()
    pygame.display.set_caption("Вход в VT")
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()

    err = None

    input_box1 = InputBox((100, 120, 0, 32), max_length=15, hidden_text="логин", copy=False)
    input_box2 = InputBox((100, 205, 0, 32), max_length=15, hidden_text="пароль", copy=False)

    button1 = Button((180, 330, 120, 34), "вернуться", "go to func connection_user")
    button2 = Button((120, 280, 251, 34), "создать пользователя", "create_user")

    text = Text((120, 50), 300, "Месанджер VT", FONT=pg.font.Font(None, 50), color_text=(100, 140, 100))
    text1 = Text((140, 160), 220,
                 "У логин минимальная длина 3 знака. Максимальная длина 15 знаков.")
    text2 = Text((140, 245), 220,
                 "У пароля минимальная длина 3 знака. Максимальная длина 15 знаков.")

    overflow = OverFlow((0, 0, 500, 500))
    overflow.add(button1, button2, text, text1, text2, input_box1, input_box2)

    _done = False

    while not _done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _done = True
                return None
            d = overflow.handle_event(event)
            try:
                err.handle_event(event)
            except:
                pass
            if not d is None:
                if d.type == "create_user":
                    answer = connection.spend({
                        "name": input_box1.text,
                        "password": input_box2.text,
                        "command": "create_user",
                        "path": "user"
                    })
                    try:
                        print(answer["answer"])
                        if answer["answer"] == "user made":
                            db.update({
                                "name": input_box1.text,
                                "password": input_box2.text
                            })
                            return True
                        else:
                            err = Text((120, 30), 300, answer["answer"], color_text=(230, 100, 100))
                    except:
                        err = Text((120, 30), 300, answer, color_text=(230, 100, 100))
                elif d.type == "go to func connection_user":
                    return False
        overflow.update()
        try:
            err.update()
        except:
            pass
        screen.fill((0, 0, 0))

        screen = overflow.draw(screen)
        try:
            screen = err.draw(screen)
        except:
            pass
        pygame.display.flip()
        clock.tick(30)
