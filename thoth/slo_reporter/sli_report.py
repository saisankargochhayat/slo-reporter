#!/usr/bin/env python3
# slo-reporter
# Copyright(C) 2020 Francesco Murdaca
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This file contains all sli metrics that should be included in the report."""

import os
import datetime
import logging

from .configuration import Configuration

from .sli_references import _add_dashbords
from .sli_pypi_knowledge_graph import SLIPyPIKnowledgeGraph
from .sli_knowledge_graph import SLIKnowledgeGraph
from .sli_learning import SLILearning
from .sli_user_api import SLIUserAPI
from .sli_workflow_quality import SLIWorkflowQuality
from .sli_template import HTMLTemplates


_END_TIME = datetime.datetime.utcnow()
_START_TIME = _END_TIME - datetime.timedelta(days=7)
_START_TIME_EPOCH = int(_START_TIME.timestamp() * 1000)
_END_TIME_EPOCH = int(_END_TIME.timestamp() * 1000)

_LOGGER = logging.getLogger(__name__)


class SLIReport:
    """This class contains all sections included in a report."""

    REPORT_SUBJECT = (
        f"Thoth Service Level Indicators Update Week"
        + f" ({_START_TIME.strftime('%Y-%m-%d')} - {_END_TIME.strftime('%Y-%m-%d')})"
    )

    REPORT_START = HTMLTemplates.thoth_report_start_template()

    REPORT_INTRO = HTMLTemplates.thoth_report_intro_template(
        html_inputs={
            "environment": Configuration._ENVIRONMENT,
            "start_time": str(_START_TIME.strftime("%Y-%m-%d")),
            "end_time": str(_END_TIME.strftime("%Y-%m-%d")),
        }
    )

    REPORT_STYLE = HTMLTemplates.thoth_report_style_template()

    REPORT_SLI_CONTEXT = {
        SLIPyPIKnowledgeGraph._SLI_NAME: SLIPyPIKnowledgeGraph()._aggregate_info(),
        SLIKnowledgeGraph._SLI_NAME: SLIKnowledgeGraph()._aggregate_info(),
        SLILearning._SLI_NAME: SLILearning()._aggregate_info(),
        SLIUserAPI._SLI_NAME: SLIUserAPI()._aggregate_info(),
        SLIWorkflowQuality._SLI_NAME: SLIWorkflowQuality()._aggregate_info(),
    }

    REPORT_REFERENCES = _add_dashbords(_START_TIME_EPOCH, _END_TIME_EPOCH)

    REPORT_END = HTMLTemplates.thoth_report_end_template()
