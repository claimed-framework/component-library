#
# Copyright 2018-2021 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import nbformat
import re

from traitlets.config import LoggingConfigurable

from typing import TypeVar, List, Dict

# Setup forward reference for type hint on return from class factory method.  See
# https://stackoverflow.com/questions/39205527/can-you-annotate-return-type-when-value-is-instance-of-cls/39205612#39205612
F = TypeVar('F', bound='FileReader')


class FileReader(LoggingConfigurable):
    """
    Base class for parsing a file for resources according to operation type. Subclasses set
    their own parser member variable according to their implementation language.
    """

    def __init__(self, filepath: str):
        self._filepath = filepath

    @property
    def filepath(self):
        return self._filepath

    @property
    def language(self) -> str:
        file_extension = os.path.splitext(self._filepath)[-1]
        if file_extension == '.py':
            return 'python'
        elif file_extension == '.r':
            return 'r'
        else:
            return None

    def read_next_code_chunk(self) -> List[str]:
        """
        Implements a generator for lines of code in the specified filepath. Subclasses
        may override if explicit line-by-line parsing is not feasible, e.g. with Notebooks.
        """
        with open(self._filepath) as f:
            for line in f:
                yield [line.strip()]


class NotebookReader(FileReader):
    def __init__(self, filepath: str):
        super().__init__(filepath)

        with open(self._filepath) as f:
            self._notebook = nbformat.read(f, as_version=4)
            self._language = None

            try:
                self._language = self._notebook['metadata']['kernelspec']['language'].lower()

            except KeyError:
                self.log.warning(f'No language metadata found in {self._filepath}')
                pass

    @property
    def language(self) -> str:
        return self._language

    def read_next_code_chunk(self) -> List[str]:
        for cell in self._notebook.cells:
            if cell.source and cell.cell_type == "code":
                yield cell.source.split('\n')


class ScriptParser():
    """
    Base class for parsing individual lines of code. Subclasses implement a search_expressions()
    function that returns language-specific regexes to match against code lines.
    """

    _comment_char = "#"

    def _get_line_without_comments(self, line):
        if self._comment_char in line:
            index = line.find(self._comment_char)
            line = line[:index]
        return line.strip()

    def parse_environment_variables(self, line):
        # Parse a line fed from file and match each regex in regex dictionary
        line = self._get_line_without_comments(line)
        if not line:
            return []

        matches = []
        for key, value in self.search_expressions().items():
            for pattern in value:
                regex = re.compile(pattern)
                for match in regex.finditer(line):
                    matches.append((key, match))
        return matches


class PythonScriptParser(ScriptParser):
    def search_expressions(self) -> Dict[str, List]:
        # TODO: add more key:list-of-regex pairs to parse for additional resources
        regex_dict = dict()

        # First regex matches envvar assignments of form os.environ["name"] = value w or w/o value provided
        # Second regex matches envvar assignments that use os.getenv("name", "value") with ow w/o default provided
        # Third regex matches envvar assignments that use os.environ.get("name", "value") with or w/o default provided
        # Both name and value are captured if possible
        envs = [r"os\.environ\[[\"']([a-zA-Z_]+[A-Za-z0-9_]*)[\"']\](?:\s*=(?:\s*[\"'](.[^\"']*)?[\"'])?)*",
                r"os\.getenv\([\"']([a-zA-Z_]+[A-Za-z0-9_]*)[\"'](?:\s*\,\s*[\"'](.[^\"']*)?[\"'])?",
                r"os\.environ\.get\([\"']([a-zA-Z_]+[A-Za-z0-9_]*)[\"'](?:\s*\,(?:\s*[\"'](.[^\"']*)?[\"'])?)*"]
        regex_dict["env_vars"] = envs
        return regex_dict


class RScriptParser(ScriptParser):
    def search_expressions(self) -> Dict[str, List]:
        # TODO: add more key:list-of-regex pairs to parse for additional resources
        regex_dict = dict()

        # Tests for matches of the form Sys.setenv("key" = "value")
        envs = [r"Sys\.setenv\([\"']*([a-zA-Z_]+[A-Za-z0-9_]*)[\"']*\s*=\s*[\"']*(.[^\"']*)?[\"']*\)",
                r"Sys\.getenv\([\"']*([a-zA-Z_]+[A-Za-z0-9_]*)[\"']*\)(.)*"]
        regex_dict["env_vars"] = envs
        return regex_dict


class ContentParser(LoggingConfigurable):
    parsers = {
        'python': PythonScriptParser(),
        'r': RScriptParser()
    }

    def parse(self, filepath: str) -> dict:
        """Returns a model dictionary of all the regex matches for each key in the regex dictionary"""

        properties = {"env_vars": {}, "inputs": [], "outputs": []}
        reader = self._get_reader(filepath)
        parser = self._get_parser(reader.language)

        if not parser:
            return properties

        for chunk in reader.read_next_code_chunk():
            if chunk:
                for line in chunk:
                    matches = parser.parse_environment_variables(line)
                    for key, match in matches:
                        if key == "env_vars":
                            properties[key][match.group(1)] = match.group(2)
                        else:
                            properties[key].append(match.group(1))

        return properties

    def _validate_file(self, filepath: str):
        """
        Validate file exists and is file (e.g. not a directory)
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'No such file or directory: {filepath}')
        if not os.path.isfile(filepath):
            raise IsADirectoryError(f'Is a directory: {filepath}')

    def _get_reader(self, filepath: str):
        """
        Find the proper reader based on the file extension
        """
        file_extension = os.path.splitext(filepath)[-1]

        self._validate_file(filepath)

        if file_extension == '.ipynb':
            return NotebookReader(filepath)
        elif file_extension in ['.py', '.r']:
            return FileReader(filepath)
        else:
            raise ValueError(f'File type {file_extension} is not supported.')

    def _get_parser(self, language: str):
        """
        Find the proper parser based on content language
        """
        parser = None
        if language:
            parser = self.parsers.get(language)

            if not parser:
                self.log.warning(f'Content parser for {language} is not available.')
                pass

        return parser
