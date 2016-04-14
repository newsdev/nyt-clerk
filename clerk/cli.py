import bson
from functools import wraps
import pkg_resources

from clerk import scdb
from clerk import scores

from clint.textui import puts, colored
from cement.core.foundation import CementApp
from cement.ext.ext_logging import LoggingLogHandler
from cement.core.controller import CementBaseController, expose

VERSION = pkg_resources.get_distribution('nyt-clerk').version
LOG_FORMAT = '%(asctime)s (%(levelname)s) %(namespace)s (v{0}) : \
%(message)s'.format(VERSION)
BANNER = "NYT Clerk version {0}".format(VERSION)


class ClerkBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Get and process Supreme Court data from previous terms."
        arguments = [
            (['--format-json'], dict(
                action='store_true',
                help='Pretty print JSON when using `-o json`.'
            )),
            (['-v', '--version'], dict(
                action='version',
                version=BANNER
            )),
        ]

    @expose(hide=True)
    def default(self):
        """
        Print help
        """
        self.app.args.print_help()

    @expose(help="Get SCDB votes")
    def votes(self):
        """
        Initialize SCDB votes
        """
        self.app.log.info('Getting SCDB votes (one per Justice per case) for\
 terms 1791-2014')

        l = scdb.Load()
        l.download()
        l.unzip()
        l.load('votes')
        data = l.votes
        self.app.render(data)

    @expose(help="Get SCDB cases")
    def cases(self):
        """
        Initialize SCDB cases
        """
        self.app.log.info('Getting SCDB cases for terms 1791-2014')

        l = scdb.Load()
        l.download()
        l.unzip()
        l.load('cases')
        data = l.cases
        self.app.render(data)

    @expose(help="Get Martin-Quinn justice scores")
    def terms(self):
        """
        Initialize Martin-Quinn justice scores
        """
        self.app.log.info('Getting Martin-Quinn justice scores for each Justice\
 by term.')

        l = scores.Load()
        l.download()
        l.load('justice_terms')
        data = l.justice_terms
        self.app.render(data)

    @expose(help="Get Segal-Cover justice scores")
    def justices(self):
        """
        Initialize Segal-Cover justice scores
        """
        self.app.log.info('Getting Justice information, including pre-confirmation\
 Segal-Cover ideology and qualification scores.')

        l = scores.Load()
        l.download()
        l.load('justices')
        data = l.justices
        self.app.render(data)

    @expose(help="Get Martin-Quinn court scores")
    def courts(self):
        """
        Initialize Martin-Quinn court scores
        """
        self.app.log.info('Get Martin-Quinn court scores for the whole Court\
 by term.')

        l = scores.Load()
        l.download()
        l.load('courts')
        data = l.courts
        self.app.render(data)

class ClerkApp(CementApp):
    class Meta:
        label = 'clerk'
        base_controller = ClerkBaseController
        hooks = []
        extensions = [
            'clerk.ext_csv',
            'clerk.ext_json'
        ]
        output_handler = 'csv'
        handler_override_options = dict(
            output=(['-o'], dict(help='output format (default: csv)')),
        )
        log_handler = LoggingLogHandler(
            console_format=LOG_FORMAT,
            file_format=LOG_FORMAT
        )


def main():
    with ClerkApp() as app:
        app.run()