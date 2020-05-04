"""
===================================================
:mod:`excel` -- Extractors for Excel data extracting.
===================================================
"""
from typing import List

from openpyxl.worksheet.worksheet import Worksheet

from .abc import AbstractSimpleExtractor
from .exceptions import ExprError


class ExcelExtractor(AbstractSimpleExtractor):
    """
    Use Openpyxl for excel extracting.

    Before extracting, should load the Excel file with Openpyxl
    and retrieve the sheet with interested data as
    :class:`openpyxl.worksheet.worksheet.Worksheet` object.

    :param expr: Cell coordinate.
    :type expr: str
    """

    def extract(self, element: Worksheet) -> List[str]:
        """
        Extract data from Excel.

        :param element: Worksheet with all interested data.
        :type element: Worksheet

        :returns: Data.
        :rtype: Any
        """
        try:
            cell = element[self.expr]
        except ValueError as exc:
            raise ExprError(extractor=self, exc=exc) from exc
        else:
            if isinstance(cell, tuple):  # Cell range
                return [
                    c.value for row in cell for c in row
                    if c.value is not None  # Escape empty cells
                ]

            value = cell.value

            if not value:
                return []

            return [value]


__all__ = ("ExcelExtractor",)
