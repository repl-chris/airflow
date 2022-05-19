#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from airflow import settings
from airflow.utils.file import find_path_from_directory


class TestIgnorePluginFile(unittest.TestCase):
    """
    Test that the .airflowignore work and whether the file is properly ignored.
    """

    def setUp(self):
        """
        Make tmp folder and files that should be ignored. And set base path.
        """
        # Temp dir name includes an ignored token "not", but it shouldn't matter since it's in the base path.
        self.test_dir = tempfile.mkdtemp(prefix="onotole")
        self.test_file = os.path.join(self.test_dir, 'test_file.txt')
        self.plugin_folder_path = os.path.join(self.test_dir, 'test_ignore')
        os.mkdir(self.plugin_folder_path)
        os.mkdir(os.path.join(self.plugin_folder_path, "subdir1"))
        os.mkdir(os.path.join(self.plugin_folder_path, "subdir2"))
        os.mkdir(os.path.join(self.plugin_folder_path, "subdir3"))
        files_content = [
            ["test_load.py", "#Should not be ignored file"],
            ["test_notload.py", 'raise Exception("This file should have been ignored!")'],
            [".airflowignore", "#ignore test\nnot\nsubdir2"],
            [".airflowignore_glob", "#ignore test\n**/*not*\nsubdir2/"],
            ["subdir1/.airflowignore", "#ignore test\nnone\n_glob"],
            ["subdir1/.airflowignore_glob", "#ignore test\n*none*"],
            ["subdir1/test_load_sub1.py", "#Should not be ignored file"],
            ["test_notload_sub.py", 'raise Exception("This file should have been ignored!")'],
            ["subdir1/test_noneload_sub1.py", 'raise Exception("This file should have been ignored!")'],
            ["subdir2/test_shouldignore.py", 'raise Exception("This file should have been ignored!")'],
            ["subdir3/test_notload_sub3.py", 'raise Exception("This file should have been ignored!")'],
            ["test_notload_linktarget.py", '#Should not be loaded directly, but should be loaded via symlink'],
        ]
        symlinks = [
            ["test_notload_linktarget.py", "test_load_symlink.py"],
            ["test_load.py", "test_notload_symlink.py"],
        ]
        for file_path, content in files_content:
            with open(os.path.join(self.plugin_folder_path, file_path), "w") as f:
                f.write(content)
        for target, link in symlinks:
            os.symlink(os.path.join(self.plugin_folder_path, target), os.path.join(self.plugin_folder_path, link))
        self.mock_plugins_folder = patch.object(
            settings, 'PLUGINS_FOLDER', return_value=self.plugin_folder_path
        )

    def tearDown(self):
        """
        Delete tmp folder
        """
        shutil.rmtree(self.test_dir)

    def test_find_not_should_ignore_path_regexp(self):
        """
        Test that the .airflowignore regexp works and whether the files are properly ignored.
        """

        detected_files = set()
        should_ignore_files = {
            'test_notload.py',
            'test_notload_sub.py',
            'test_noneload_sub1.py',
            'test_shouldignore.py',
            '.airflowignore_glob',
            'test_notload_symlink.py',
            'test_notload_linktarget.py',
        }
        should_not_ignore_files = {
            'test_load.py',
            'test_load_sub1.py',
            'test_load_symlink.py',
        }
        ignore_list_file = ".airflowignore"
        for file_path in find_path_from_directory(self.plugin_folder_path, ignore_list_file):
            if not os.path.isfile(file_path):
                continue
            _, file_ext = os.path.splitext(os.path.split(file_path)[-1])
            if file_ext != '.py':
                continue
            detected_files.add(os.path.basename(file_path))
        assert detected_files == should_not_ignore_files
        assert detected_files & should_ignore_files == set()

    def test_find_not_should_ignore_path_glob(self):
        """
        Test that the .airflowignore glob syntax works and whether the files are properly ignored.
        """

        detected_files = set()
        should_ignore_files = {
            'test_notload.py',
            'test_notload_sub.py',
            'test_noneload_sub1.py',
            'test_shouldignore.py',
            'test_notload_symlink.py',
            'test_notload_linktarget.py',
        }
        should_not_ignore_files = {
            'test_load.py',
            'test_load_sub1.py',
            'test_load_symlink.py',
        }
        ignore_list_file = ".airflowignore_glob"
        for file_path in find_path_from_directory(self.plugin_folder_path, ignore_list_file, "glob"):
            if not os.path.isfile(file_path):
                continue
            _, file_ext = os.path.splitext(os.path.split(file_path)[-1])
            if file_ext != '.py':
                continue
            detected_files.add(os.path.basename(file_path))
        assert detected_files == should_not_ignore_files
        assert detected_files & should_ignore_files == set()
