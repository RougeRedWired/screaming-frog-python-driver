"""
Contains all crawlers for the project

"""

import subprocess
import os
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler(
            "{0}/{1}.log".format(os.getcwd(), "screaming_frog")),
        logging.StreamHandler()
    ])


class ScreamingFrogSpider(object):
    """
    Make use of Screaming Frog (SF) (https://www.screamingfrog.co.uk/) via the subprocess module.
    It calls the Screaming Frog CLI, default url is based off of the default set up.
    param:seospiderconfig_absolute_pathname: str pathname to binary file containing all config set up using SF UI.
    mandatory parameter by design, so you remember to add the correct configuration every time
    param:output_folder:str where all output should be saved to.
    param:export_tabs:list of strings all exports under export, matching the UI. default extract Internal:All Name matches UI set up
    param:file_full_path:str path to list of urls to crawl if list mode.
    param:spider name:str
    param:override
    """

    def __init__(self,
                 seospiderconfig_absolute_pathname,
                 cli_exe,
                 file_full_path=None,
                 name="screaming_frog",
                 override=False,
                 output_folder=os.getcwd(),
                 ):
        self.name = name
        self.seospiderconfig_absolute_pathname = seospiderconfig_absolute_pathname
        self.output_folder = output_folder
        self.cli_exe = cli_exe
        self.file_full_path = file_full_path
        self.override = override
        self.logger = logging.getLogger()

    def _define_overwrite_mode(self, override_switch):
        if override_switch == True:
            return "--overwrite"
        else:
            return "--timestamped-output"

    def start_list_crawl(self, *args):
        """This function makes use of the subprocess module to call screaming frog for crawling
        lists of urls.
        See https://screamingfrog.co.uk/seo-spider/user-guide/general/#command-line
        """
        now = time.time()

        list_crawl_configuration = [self.cli_exe,
                                    "--crawl-list",
                                    self.file_full_path,
                                    "--headless",
                                    "--config",
                                    self.seospiderconfig_absolute_pathname,
                                    "--output-folder",
                                    self.output_folder,

                                    ]

        self.logger.info("crawl configuration: %s", repr(list_crawl_configuration))
        self.logger.info("parsing arguments")

        for arg in args:
            self.logger.info("parsed %s", arg)
            list_crawl_configuration.append(arg)

        list_crawl_configuration.append(self._define_overwrite_mode(self.override))

        file_list = os.listdir(self.output_folder)

        subprocess.run(list_crawl_configuration, shell=True)

        return None

    def start_spider_crawl(self, website, *args):
        """This function makes use of the subprocess module to call screaming frog for crawling
        websites
        See https://screamingfrog.co.uk/seo-spider/user-guide/general/#command-line
        """
        list_crawl_configuration = [self.cli_exe,
                                    "--crawl",
                                    website,
                                    "--headless",
                                    "--config",
                                    self.seospiderconfig_absolute_pathname,
                                    "--output-folder",
                                    self.output_folder,
                                    ]
        for arg in args:
            list_crawl_configuration.append(arg)

        list_crawl_configuration.append(
            self._define_overwrite_mode(self.override))

        logger.info("Crawling %s", list_crawl_configuration[2])
        subprocess.run(list_crawl_configuration, shell=True)

        return None

    def __str__(self):
        return f"""ScreamingFrogSpider(name:{self.name},
        spider_config:{self.seospiderconfig_absolute_pathname},
        cli:{self.cli_exe},
        list_of_urls:{self.file_full_path},
        override_mode:{self.override}
        """
