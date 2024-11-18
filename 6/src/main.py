from models import VoterEntry
from services import DatabaseService

if __name__ == '__main__':
    database = DatabaseService[str, VoterEntry]()