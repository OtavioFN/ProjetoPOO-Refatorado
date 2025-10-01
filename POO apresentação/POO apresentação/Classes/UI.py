import time
import os

class UI:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause_and_clear(seconds=2):
        time.sleep(seconds)
        UI.clear_screen()

    @staticmethod
    def wait_for_enter():
        input("\n\tPress ENTER to continue...")

    @staticmethod
    def generate_stars(rating):
        rounded_rating = round(rating)
        return '★' * rounded_rating + '☆' * (5 - rounded_rating)