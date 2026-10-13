
---
name: excel-creation
description: Create Excel workbooks with structured data, headers, formatting, and multiple worksheets. Use when the user requests an Excel spreadsheet, workbook, table, or data report.
---

# Excel Creation Skill

## Purpose
Create useful, organized Excel workbooks from user requests.

## Workflow
1. Understand the requested workbook and its purpose.
2. Identify the required columns, worksheets, and data.
3. Organize information into rows and columns.
4. Use clear worksheet names and column headers.
5. Apply appropriate formatting, widths, and number formats.
6. Include formulas only when appropriate and supported.
7. Use the available Excel-generation tool to create an .xlsx file.
8. Verify that the workbook exists and contains the expected worksheets.

## Rules
- Never invent real-world data or claim that sample data is factual.
- Label illustrative data as sample data.
- Keep the workbook readable and consistently formatted.
- Return the generated file location.

## Tool Requirements
These instructions do not create files by themselves.
Use an available tool or library such as openpyxl.
