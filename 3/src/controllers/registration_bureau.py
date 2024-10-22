import uuid
from colorama import Fore, Style
from models import User
from .voter import VoterController

class RegistrationBureauController:

    def __init__(self) -> None:
        self._registered_users = dict()

    def get_voters(self) -> list[int]:
        return list(self._registered_users.values())

    def register(self, user: User) -> VoterController:
        if user is None:
            raise ValueError("user cannot be None")

        print(f"{Fore.YELLOW}REGISTRATION{Style.RESET_ALL} #{user.get_id()} | ", end = '')

        print(f"{Fore.YELLOW}STATUS{Style.RESET_ALL}: ", end = '')

        if not user.get_is_able_to_vote():
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} (User is not able to vote)")
            return None

        if user in self._registered_users.keys():
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} (User has been already registered)")
            return None

        registration_id = uuid.uuid4().int
        self._registered_users[user] = registration_id
        voter_controller = VoterController(registration_id)

        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL} ({registration_id})")

        return voter_controller