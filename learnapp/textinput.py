import pygame
import unicodedata
import pyperclip  # access to copied data


class textbox:

    def __init__(self, screen, x, y, minwidth, maxwidth, height, font, default_color, active_color, textcolor, border=2, initial="", cursor_blink_interval=400):
        self.width = 0
        self.screen = screen
        self.x = x
        self.y = y
        self.minwidth = minwidth  # start width of box
        self.maxwidth = maxwidth  # if text no longer fits inside the box it expands until it reaches this width
        self.height = height
        self.border = border
        self.font = font
        self.default_color = default_color
        self.active_color = active_color
        self.textcolor = textcolor

        self.active = False
        self.left = initial  # string on the left of the cursor
        self.right = ""  # string on the right of the cursor

        # vars required for the cursor
        self._clock = pygame.time.Clock()
        self._cursor_blink_interval = cursor_blink_interval
        self._cursor_visible = False
        self._last_blink_toggle = 0

    def draw(self):
        # prerender surface and adjust variables using the rendered surface
        rendered_surface = self.font.render(self.value + " ", True, self.textcolor)

        # create the box width
        self.width = max(self.minwidth, rendered_surface.get_width())
        if self.width > self.maxwidth:
            self.width = self.maxwidth

        # create the box surface, a surface is required, so that all the text that doesn't fit, dont get on the main screen
        box = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()

        if not self.active:
            pygame.draw.rect(box, self.default_color, (0, 0, self.width, self.height), self.border)
        else:
            pygame.draw.rect(box, self.active_color, (0, 0, self.width, self.height), self.border)

        # calculating an offset to let the text that doesnt fit on the surface disappear to the left
        if rendered_surface.get_width() > self.maxwidth:
            offset = rendered_surface.get_width() - self.maxwidth
        else:
            offset = 0

        box.blit(rendered_surface, (self.border - offset, (self.height - rendered_surface.get_height())/2))

        # rendering the cursor and calculating the blink intervall
        if self.active:
            self._clock.tick()
            self._last_blink_toggle += self._clock.get_time()
            if self._last_blink_toggle > self._cursor_blink_interval:
                self._last_blink_toggle %= self._cursor_blink_interval
                self._cursor_visible = not self._cursor_visible

            if self._cursor_visible:
                str_left_of_cursor = self.value[:self.cursor_pos]
                cursor_x = self.font.size(str_left_of_cursor)[0]
                pygame.draw.rect(box, self.textcolor, (cursor_x + self.border - offset, rendered_surface.get_height()/2, 3, rendered_surface.get_height()))

        self.screen.blit(box, (self.x, self.y))

    def update(self, mouse, click, events):
        # enable/disable all actions
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:  # if mouse is on box

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)  # change cursor to this text thingie i dunno man
            if click[0] and self.active == False:
                self.active = True
                pygame.key.set_repeat(200, 90)  # makes keyinput slower so that if you enter "a" it doesnt display "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

            # every time the box is clicked, find the position the user clicked, find the closest letter and set the cursor there
            elif click[0]:
                position_list = [0]
                for idx, letter in enumerate(self.value):
                    rendered_letters = self.font.render(self.value[:idx] + letter, True, (0, 0, 0))
                    position_list.append(rendered_letters.get_width())

                # calculating an offset to let the text that doesnt fit on the surface disappear to the left
                if len(self.value) > 0:
                    if rendered_letters.get_width() > self.maxwidth:
                        offset = rendered_letters.get_width() - self.maxwidth
                    else:
                        offset = 0
                else:
                    offset = 0

                # get letter that is closest to mouse[0]
                if position_list:
                    takeClosest = lambda num, collection: min(collection, key=lambda x: abs(x-offset-num))
                    self.cursor_pos = position_list.index(takeClosest(mouse[0] - self.x, position_list))

        else:

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # change cursor to default pointer thingie
            if click[0] and self.active == True:
                self.active = False
                pygame.key.set_repeat(0, 0)  # sets keyinput to default

        if self.active:
            for e in events:
                if e.type == pygame.KEYDOWN:

                    # search function with the name "_process_" + e.key and execute it
                    attrname = f"_process_{pygame.key.name(e.key)}"
                    if hasattr(self, attrname):
                        getattr(self, attrname)()

                    if e.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self._paste()

                    else:
                        if e.unicode != "" and unicodedata.category(e.unicode)[0] != "C":  # dont allow unicode controll chars in the value
                            self._process_other(e)

                    # Make cursor visible when something is pressed
                    self._last_blink_toggle = 0
                    self._cursor_visible = True
        self.draw()

    def _process_delete(self):
        self.right = self.right[1:]

    def _process_backspace(self):
        self.left = self.left[:-1]

    def _process_right(self):
        self.cursor_pos += 1

    def _process_left(self):
        self.cursor_pos -= 1

    def _process_end(self):
        self.cursor_pos = len(self.value)

    def _process_home(self):
        self.cursor_pos = 0

    def _process_other(self, e):
        self.left += e.unicode

    def _paste(self):
        for l in pyperclip.paste():
            self.left += l

    @property
    def value(self):
        return self.left + self.right
    
    @value.setter
    def value(self, value):
        cursor_pos = self.cursor_pos
        if len(value) > 0:
            self.left = value[:cursor_pos]
            self.right = value[cursor_pos:]
        else:
            self.left = ""
            self.right = ""

    @property
    def cursor_pos(self):
        # Get / set the position of the cursor. Will clamp to [0, length of input].
        return len(self.left)

    @cursor_pos.setter
    def cursor_pos(self, value):
        if value < 0:
            value = 0
        complete = self.value
        self.left = complete[:value]
        self.right = complete[value:]
        