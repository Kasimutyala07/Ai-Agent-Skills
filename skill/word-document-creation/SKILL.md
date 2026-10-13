---
description: Create professional Microsoft Word documents (.docx) from
  user instructions, notes, or project content. Use when the user asks
  to create, format, or organize a report, letter, resume, meeting
  minutes, or other Word document.
name: word-document-creation
---

# Word Document Creation Skill

## Purpose

Help an AI agent create clear, well-structured, professional Word
documents from the user's request and supplied content.

This skill provides the workflow and quality checks. It does not create
files by itself; the agent must use an available document-generation
tool, script, or library such as `python-docx`.

## When to use this skill

Use this skill when the user asks to:

-   Create a Word document or `.docx` file.
-   Turn notes into a formal report, letter, proposal, or meeting
    minutes.
-   Format existing content with headings, lists, tables, headers, or
    page numbers.
-   Improve the structure and readability of a document.

Do not use this skill when the user explicitly requests only plain text,
Markdown, PDF, or another output format.

## Required workflow

1.  **Understand the request**
    -   Identify the document type, topic, audience, purpose, and
        requested length.
    -   Identify any supplied text, files, template, formatting rules,
        or required sections.
    -   Ask a concise clarification only if a missing detail prevents
        useful progress. Otherwise, use sensible defaults.
2.  **Plan the document**
    -   Create a logical outline before generating the file.
    -   Use sections appropriate to the document type.
    -   Do not invent personal details, research findings, references,
        or project results.
    -   Mark information that the user must supply rather than
        fabricating it.
3.  **Prepare the content**
    -   Correct obvious grammar and improve clarity without changing the
        intended meaning.
    -   Use concise paragraphs, meaningful headings, and lists where
        they improve readability.
    -   For technical reports, use sections such as Abstract,
        Introduction, Objectives, Methodology, Results, Conclusion, and
        References only when relevant.
    -   Include a table of contents only for longer documents or when
        requested.
4.  **Generate the `.docx`**
    -   Use an available file-generation tool or a library such as
        `python-docx`.
    -   Apply consistent page margins, font choices, heading styles,
        spacing, and page breaks.
    -   Use real Word heading styles rather than merely making heading
        text bold.
    -   Format tables so that they are readable and fit within the page.
    -   Add headers, footers, page numbers, a cover page, or a table of
        contents when requested or useful.
    -   Save the file to a known output path and report that exact path.
5.  **Validate the output**
    -   Confirm that the file was created successfully.
    -   Check that the document is not empty and contains the expected
        sections.
    -   Check for missing content, broken tables, inconsistent headings,
        or accidental placeholder text.
    -   If possible, reopen or render the file to verify its layout.
    -   Never claim that a file was created or checked unless the tool
        confirms it.
6.  **Deliver the result**
    -   Provide the generated file or a valid link to it.
    -   Briefly describe what it contains.
    -   Mention any assumptions or information that still needs the
        user's input.

## Default formatting

Unless the user specifies otherwise:

-   Use a clean, professional layout.
-   Use a readable body font at approximately 11 pt.
-   Use clear heading levels and consistent spacing.
-   Use standard page margins.
-   Use simple tables and restrained styling.
-   Keep the language appropriate for the intended audience.
-   Do not add decorative elements that make the document harder to
    read.

## Tool-use guidance

-   A skill is a set of reusable instructions; it is not the same as a
    tool.
-   Use only tools and libraries that are actually available in the
    current environment.
-   If using Python, `python-docx` is a common choice for creating
    `.docx` files.
-   If a required library is unavailable, explain the limitation and use
    an available alternative when possible.
-   Ask before taking external actions such as emailing or publishing
    the completed document.
-   Respect the user's privacy and do not include unrelated personal or
    confidential information.

## Example

**User request:**\
"Create a Word report for my AI project, Fake News Detection in Online
Media Using Deep Learning."

**Agent should:**

1.  Identify this as a technical project report.
2.  Draft a suitable outline, such as Introduction, Problem Statement,
    Objectives, Proposed Methodology, System Architecture, Evaluation
    Plan, Conclusion, and References.
3.  Use only facts and results supplied by the user; do not invent
    accuracy scores or experimental findings.
4.  Generate a `.docx` file using an available document-generation tool.
5.  Validate the file and provide it to the user.

## Completion checklist

Before returning the document, confirm:

-   [ ] The requested file exists.
-   [ ] The content matches the user's request.
-   [ ] Headings and formatting are consistent.
-   [ ] No unsupported facts or fabricated results were added.
-   [ ] The file was validated to the extent the environment allows.
-   [ ] The user receives the correct file link or location.
