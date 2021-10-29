from unittest import TestCase
import os
import platform
import glob


"""
Testcases in here are meant to check if all required modules are installed for all the different collectors.
The test case "TestMinimumDependencies" must be passed in order to run mosk on your system. The other test cases
are meant to test dependencies for all the different collectors. If you are not trying to run a collector on your system
you can savely ignore the dependency-test case for the collector, hence all collectors should be encapsuled and the
whole system, or the other collectors, should not, and are not dependent on one single collector.
"""


class TestMinimumDependencies(TestCase):
    def setUp(self) -> None:
        self._currentCWD = os.getcwd()
        os.chdir('..')

    def tearDown(self) -> None:
        logfiles = glob.glob('./dependency_test*.txt')
        for logfile in logfiles:
            os.remove(logfile)
        os.chdir(self._currentCWD)

    def test_run_minimum_instructions(self):
        """
        Should run without any exceptions, if all required modules are installed on the system.
        :return:
        """
        instructions_path = './tests/instructions/dependencies_test_minimal.xml'
        if platform.system() == "Windows":
            instructions_path =  ".\\tests\\instructions\\dependencies_test_minimal.xml"

        logfile:str = "dependency_test_log.txt"
        self._run_instrcutions(instructions_path, logfile)

        self.assertTrue(os.path.exists(logfile))

    def test_run_minimum_instructions_for_collectors(self):
        """
        Looks inside "tests/testfiles/instructions/collector_instructions" and runs every instrcutions file
        in there. Normally, there should be no exception, or anything else.
        :return:
        """
        dependency_test_instructions = glob.glob('./tests/instructions/collector_instructions/dependency_test_*.xml')

        for instructions_file in dependency_test_instructions:
            artefact:str = instructions_file.split('/')[-1].replace('dependency_test_', '').replace('.xml', '')\
                .replace('_', '.')
            print(f"Dependency Test for module: '{artefact}'")
            logfile:str = f"dependency_test_log_{artefact}.txt"
            self._run_instrcutions(instructions_file, logfile)
            self.assertTrue(os.path.exists(logfile))
            self.assertTrue(os.stat(logfile).st_size > 0)

    @staticmethod
    def _run_instrcutions(instructions_path, logfile_path):
        os.system(f"python ./mosk.py -g 'global_placeholders.json' -i "
                  f"'{instructions_path}' -e tst -l Debug "
                  f"-p {logfile_path}")