# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common utility for testing CLI in Kubeflow."""

import datetime
import random
import string
from typing import Any, List, Text

from tfx import components
from tfx.dsl.components.base.base_component import BaseComponent
from tfx.utils import io_utils


def create_e2e_components(csv_input_location: Text,) -> List[BaseComponent]:
  """Creates components for a simple Chicago Taxi TFX pipeline for testing.

     Because we don't need to run whole pipeline, we will make a very short
     toy pipeline.

  Args:
    csv_input_location: The location of the input data directory.

  Returns:
    A list of TFX components that constitutes an end-to-end test pipeline.
  """

  example_gen = components.CsvExampleGen(input_base=csv_input_location)
  statistics_gen = components.StatisticsGen(
      examples=example_gen.outputs['examples'])
  schema_gen = components.SchemaGen(
      statistics=statistics_gen.outputs['statistics'],
      infer_feature_shape=False)

  return [example_gen, statistics_gen, schema_gen]


def generate_random_id(seed: Any = None):
  """Generate a random id string which has a timestamp prefix."""
  if seed:
    random.seed(seed)
  return datetime.datetime.now().strftime('%s') + ''.join([
      random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
  ])


def copy_and_change_pipeline_name(orig_path: Text, new_path: Text,
                                  origin_pipeline_name: Text,
                                  new_pipeline_name: Text) -> None:
  """Copy pipeline file to new path with pipeline name changed."""
  contents = io_utils.read_string_file(orig_path)
  assert contents.count(
      origin_pipeline_name) == 1, 'DSL file can only contain one pipeline name'
  contents = contents.replace(origin_pipeline_name, new_pipeline_name)
  io_utils.write_string_file(new_path, contents)
