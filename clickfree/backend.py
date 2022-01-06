from clickupython import client
import datetime
import itertools as it
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

class Backend(object):
    def __init__(self, key, name):
        self.API_KEY = key
        self.username = name
        self.teams = self._teams()
        self.spaces = self._spaces()
        self.folders = self._folders()
        self.lists = self._lists()
        self.tasks = self._tasks()
        self.my_tasks = self.find_your_tasks()

    def client(self):
        return client.ClickUpClient(self.API_KEY)

    def _teams(self):
        logger.info("Getting teams!")
        return self.client().get_teams().teams

    def _spaces(self):
        logger.info("Getting workspaces!")
        cli = self.client()
        out = []
        for t in self.teams:
            try:
                out.append(cli.get_spaces(t.id).spaces)
            except:
                pass
        return list(it.chain(*out))

    def _folders(self):
        logger.info("Getting folders!")
        cli = self.client()
        return list(it.chain(*[cli.get_folders(s.id).folders for s in self.spaces]))

    def _lists(self):
        logger.info("Getting lists!")
        cli = self.client()
        return list(it.chain(*[cli.get_lists(f.id).lists for f in self.folders]))

    def _tasks(self, **kwargs):
        logger.info("Getting tasks!")
        cli = self.client()
        return list(it.chain(*[cli.get_tasks(l.id, **kwargs).tasks for l in self.lists]))

    def find_your_tasks(self):
        out = []
        for t in self.tasks:
            if len(t.assignees) == 0:
                continue
            ids = [a.username for a in t.assignees]
            if self.username in ids:
                out.append(t)
        return out


def humanize_time(timestamp):
    try:
        return datetime.datetime.fromtimestamp(int(timestamp)/1000)
    except:
        return datetime.datetime.utcnow()
