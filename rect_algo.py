
import copy
from time import sleep
import pygame as pg

pg.init()


class DrawRects:
    color_yellow = (255, 255, 0)

    def __init__(self):
        self.SCREEN_HEIGHT = int(input("Height of you screen please: "))
        self.SCREEN_WIDTH = int(input("Width of your screen please: "))
        self.SCREEN_HEIGHT_HALF = self.SCREEN_HEIGHT / 2
        self.SCREEN_WIDTH_HALF = self.SCREEN_WIDTH / 2
        self.all_allowed_rects = int(input("How many rects do you want?: "))
        self.screen = pg.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

    def check_if_odd(self, number):
        if number % 2 != 0:
            return True
        else:
            return False

    def remain(self, locale_all_allowed_rects, sumik):
        zbytek = sumik - locale_all_allowed_rects
        return zbytek

    def logic(self):
        """
        How this program works: Basically I am creating two lists of numbers from 1 to x, where x is always increased
        by one. In the same time I am creating a middle number, which is always the biggest number in the list (so
        len of the list). When len sum of this two lists exceeds the rect limit (given to me by the user),
        the adding stops, and I'll check by how much it exceeded the rect limit, and I'll edit the list,
        so the sum is exactly equal to the rect limit. When editing the list, I am removing or adding to both sides or middle number
        equally, so the result is as symmetric as possible.

        """
        rect_size = 120
        rect_x_pos = self.SCREEN_WIDTH_HALF
        rect_y_pos = self.SCREEN_HEIGHT - rect_size
        gaps = 20
        sum_of_lists = 0
        number = 1
        ls1 = []
        ls2 = []
        middle_number = None

        while sum_of_lists < self.all_allowed_rects:
            ls1.append(number)
            ls2.append(number)
            number += 1
            middle_number = len(ls1)
            sum_of_lists = self.get_sum(ls1, ls2)

        sumik2 = self.get_sum(ls1, ls2)
        ls1.remove(middle_number)
        ls2.remove(middle_number)
        ls2 = sorted(ls2, reverse=True)
        ls1.extend(ls2)
        ls2.clear()
        ls1.insert(len(ls1) - int(len(ls1) / 2), middle_number)
        middle_number_backup = middle_number
        ls1_backup = copy.deepcopy(ls1)
        ls1_backup.insert(len(ls1) - int(len(ls1) / 2), middle_number)
        middle_number = 0
        sum_of_lists = self.get_sum(ls1, ls2, middle_number)

        if sumik2 == self.all_allowed_rects:
            ls_ulti = ls1_backup

        elif sum_of_lists + 1 == self.all_allowed_rects:
            ls1.remove(middle_number_backup)
            middle_number_backup += 1
            ls1.insert(len(ls1) - int(len(ls1) / 2), middle_number_backup)
            ls_ulti = self.equalizer(middle_number, ls1, ls2, self.all_allowed_rects)
        else:
            ls_ulti = self.equalizer(middle_number, ls1, ls2, self.all_allowed_rects)

        self.drawing_logic(rect_x_pos, rect_y_pos, rect_size, ls_ulti, gaps, self.all_allowed_rects)

    def drawing_logic(self, rect_x_pos, rect_y_pos, rect_size, ls_ulti, gaps, allowed_rects):
        index = 0
        index_of_list_of_increase = 0
        aktivni_krizky = 0
        index2 = -1
        rects_in_row = 0
        list_of_increase = []
        decrease = False
        for x in range(0, 2):
            if ls_ulti[index] != 0:
                allowed_in_row = ls_ulti[index]
            else:
                index += 1
        pocitadlo = 0
        while aktivni_krizky < allowed_rects:
            try:
                last_rect = pg.draw.rect(self.screen, self.color_yellow,
                                         (rect_x_pos, rect_y_pos, rect_size, rect_size - 18), 3)
                aktivni_krizky += 1
                if not decrease:
                    rect_x_pos += rect_size + gaps
                else:
                    rect_x_pos -= rect_size + gaps
                rects_in_row += 1
                if ls_ulti[index] < ls_ulti[index + 1]:
                    list_of_increase.append(last_rect)
                if rects_in_row == allowed_in_row:
                    pocitadlo += 1
                    index += 1
                    if ls_ulti[index - 1] > ls_ulti[index]:
                        rect_x_pos = self.SCREEN_WIDTH_HALF - (allowed_in_row * rect_size) / 2 - rect_size / 2 - gaps
                        index2 = pocitadlo
                        list_of_increase = sorted(list_of_increase, reverse=True)
                        decrease = True
                    if decrease:
                        rect_x_pos = list_of_increase[index_of_list_of_increase][0]
                        index_of_list_of_increase += 1
                        index2 -= 1
                    elif ls_ulti[index - 1] + 1 == ls_ulti[index]:
                        rect_x_pos -= (ls_ulti[index] * rect_size)
                        rect_x_pos += rect_size / 2
                        rect_x_pos -= gaps * (ls_ulti[index] - 0.5)

                    elif ls_ulti[index - 1] + 3 == ls_ulti[index]:
                        rect_x_pos = self.SCREEN_WIDTH_HALF - (pocitadlo * rect_size) / 2 - rect_size - gaps * 2

                    elif ls_ulti[index - 1] + 2 == ls_ulti[index]:
                        if last_rect[0] != self.SCREEN_WIDTH_HALF:
                            rect_x_pos = (last_rect[0] - rects_in_row * rect_size) - gaps * ls_ulti[index - 1]
                        else:
                            rect_x_pos = (last_rect[0] - rects_in_row * rect_size) - gaps
                    elif ls_ulti[index - 1] + 3 < ls_ulti[index]:
                        rect_x_pos -= (ls_ulti[index] * rect_size) - ls_ulti[index] * gaps

                    elif ls_ulti[index - 1] == ls_ulti[index]:
                        if 2 < ls_ulti[index - 1] < 3:
                            rect_x_pos = last_rect[0] - (pocitadlo - 1) * rect_size - gaps * 2 - gaps
                        if ls_ulti[index] == 3:
                            rect_x_pos = last_rect[0] - (pocitadlo - 1) * rect_size - gaps * 2
                        else:
                            rect_x_pos = last_rect[0] - (pocitadlo - 1) * rect_size - gaps

                    allowed_in_row = ls_ulti[index]
                    rect_y_pos -= rect_size + gaps - 18
                    rects_in_row = 0
                pg.display.update()
                sleep(0.5)
                if aktivni_krizky + 1 == allowed_rects:
                    rect_x_pos = self.SCREEN_WIDTH_HALF
            except IndexError:
                rect_x_pos = self.SCREEN_WIDTH_HALF
                pg.draw.rect(self.screen, self.color_yellow,
                             (rect_x_pos, rect_y_pos, rect_size, rect_size - 18), 3)
                pg.display.update()
        if input("Exit? (y): ") == "y":
            exit(0)

    def equalizer(self, middle_number, ls1, ls2, all_allowed_rects):
        index = 0
        sum_of_numbers = self.get_sum(ls1, ls2, middle_number)
        remainder = self.remain(all_allowed_rects, sum_of_numbers)
        if self.check_if_odd(remainder):
            while self.check_if_odd(remainder):
                middle_number += 1
                ls1[(len(ls1) - int(len(ls1) / 2 + 1))] += middle_number
                sum_of_numbers = self.get_sum(ls1, ls2)
                remainder = self.remain(all_allowed_rects, sum_of_numbers)
        if not self.check_if_odd(remainder):
            if remainder > 0:
                remainder = self.remove_overload(ls1, ls2, sum_of_numbers, all_allowed_rects, middle_number, True)
            if remainder < 0:
                remainder = self.remove_overload(ls1, ls2, sum_of_numbers, all_allowed_rects, middle_number, False)

        if remainder == 0:
            return ls1

    def get_sum(self, ls1, ls2, *args):
        try:
            sum_of_lists = sum(ls1) + sum(ls2) + args[0]
        except IndexError:
            sum_of_lists = sum(ls1) + sum(ls2)
        return sum_of_lists

    def remove_overload(self, ls1, ls2, sum_of_lists, all_allowed_rects, middle_number, switch_mode):
        index = 0
        if switch_mode:
            while sum_of_lists != all_allowed_rects:
                ls1[index] -= 1
                ls1[len(ls1) - 1 - index] -= 1
                sum_of_lists = self.get_sum(ls1, ls2)
                index += 1
            remainder = 0
            return remainder
        if not switch_mode:
            while sum_of_lists != all_allowed_rects:
                if sum_of_lists + 2 < all_allowed_rects:
                    ls1[index] += 1
                    ls1[len(ls1) - 1 - index] += 1
                    index += 1
                if sum_of_lists + 2 == all_allowed_rects:
                    ls1[len(ls1) - int(len(ls1) / 2 + 1)] += 2
                    break
                sum_of_lists = self.get_sum(ls1, ls2, middle_number)
            remainder = 0
            return remainder
