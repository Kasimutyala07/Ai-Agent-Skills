
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from skill_loader import load_skills
from document_tool import create_word_document
from presentation_tool import create_presentation
from excel_tool import create_excel
from pdf_tool import create_pdf


# -------------------------------
# 1. Setup
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-120b"

# Conversation memory for the current session
conversation_history = []


# -------------------------------
# 2. LLM helper
# -------------------------------

def ask_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content


# -------------------------------
# 3. JSON parser
# -------------------------------

def parse_json(content):
    if not isinstance(content, str) or not content.strip():
        raise ValueError("The AI returned an empty response.")

    content = content.strip()

    if content.startswith("```"):
        lines = content.splitlines()
        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end > start:
        return json.loads(content[start:end + 1])

    raise ValueError("The AI response does not contain valid JSON.")


# -------------------------------
# 4. Intent detection
# -------------------------------

def detect_intent(user_request):
    response = ask_llm([
        {
            "role": "system",
            "content": (
                "Classify the user's request. Return JSON only: "
                '{"intent":"file"} or {"intent":"question"}. '
                "Use file if the user explicitly asks to create a "
                "Word document, PowerPoint, Excel workbook, or PDF. "
                "Otherwise use question."
            ),
        },
        {"role": "user", "content": user_request},
    ])

    result = parse_json(response)
    intent = result.get("intent")

    if intent not in {"file", "question"}:
        raise ValueError("Invalid intent returned by AI.")

    return intent


# -------------------------------
# 5. Select a skill
# -------------------------------

def select_skill(user_request, skills):
    catalog = [
        {
            "name": skill["name"],
            "description": skill["description"],
        }
        for skill in skills
    ]

    result = ask_llm([
        {
            "role": "system",
            "content": (
                "Choose the best skill for the user's request "
                "from this catalog:\n"
                + json.dumps(catalog)
                + '\nReturn JSON only: {"skill_name":"exact skill name"}. '
                'If no skill fits, return {"skill_name":"none"}.'
            ),
        },
        {"role": "user", "content": user_request},
    ])

    choice = parse_json(result)
    selected_name = choice.get("skill_name")

    for skill in skills:
        if skill["name"] == selected_name:
            return skill

    return None


# -------------------------------
# 6. Generate file content
# -------------------------------

def generate_content(user_request, skill):
    name = skill["name"]

    if name == "word-document-creation":
        format_instructions = """
Return JSON with this structure:
{
    "title": "Document title",
    "sections": {
        "Introduction": "Paragraph content",
        "Conclusion": "Paragraph content"
    }
}
Include the sections requested by the user.
"""

    elif name == "powerpoint-creation":
        format_instructions = """
Return JSON with this structure:
{
    "title": "Presentation title",
    "slides": [
        {
            "title": "Slide title",
            "points": ["Point one", "Point two"]
        }
    ]
}
Create concise, useful slides.
The tool creates a title slide automatically.
If the user specifies a total slide count, include
one fewer content slides because of the title slide.
"""

    elif name == "excel-creation":
        format_instructions = """
Return JSON with this structure:
{
    "title": "Workbook title",
    "sheets": [
        {
            "name": "Sheet1",
            "headers": ["Name", "Marks"],
            "rows": [["Ravi", 85], ["Sita", 90]]
        }
    ]
}
Use sample data when the user requests sample data.
Do not invent actual user records or claim sample data is real.
"""

    elif name == "pdf-creation":
        format_instructions = """
Return JSON with this structure:
{
    "title": "PDF title",
    "sections": {
        "Introduction": "Paragraph content",
        "Conclusion": "Paragraph content"
    }
}
Include the sections requested by the user.
"""

    else:
        raise ValueError(
            f"No generation workflow configured for skill: {name}"
        )

    # Give the model skill instructions and recent conversation history.
    messages = [
        {
            "role": "system",
            "content": (
                "Follow these skill instructions:\n\n"
                + skill["instructions"]
                + "\n\n"
                + format_instructions
                + "\nUse recent conversation history to understand "
                "references such as 'the same topic' or 'that example'. "
                "Return valid JSON only. Do not use Markdown fences."
            ),
        }
    ]

    messages.extend(conversation_history[-10:])

    messages.append({
        "role": "user",
        "content": user_request,
    })

    # Retry once if the response is not valid JSON.
    for attempt in range(2):
        result = ask_llm(messages)

        try:
            return parse_json(result)

        except (json.JSONDecodeError, ValueError) as error:
            if attempt == 1:
                raise

            print("Invalid JSON received. Asking the AI to correct it...")

            messages.append({
                "role": "assistant",
                "content": result or "",
            })

            messages.append({
                "role": "user",
                "content": (
                    "Your previous response was not valid JSON. "
                    "Correct the error and return only valid JSON "
                    "matching the required structure. "
                    f"Parsing error: {error}"
                ),
            })


# -------------------------------
# 7. Answer general questions
# -------------------------------

def answer_general_question(user_request):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "Use recent conversation history to understand "
                "follow-up questions such as 'the same topic' "
                "or 'that example'. Answer clearly and accurately. "
                "Do not create files unless explicitly requested."
            ),
        }
    ]

    messages.extend(conversation_history[-10:])

    messages.append({
        "role": "user",
        "content": user_request,
    })

    response = ask_llm(messages)

    conversation_history.extend([
        {"role": "user", "content": user_request},
        {"role": "assistant", "content": response},
    ])

    del conversation_history[:-10]

    return response


# -------------------------------
# 8. Execute the selected tool
# -------------------------------

def execute_skill(skill_name, data):
    title = data["title"]

    if skill_name == "word-document-creation":
        sections = data["sections"]

        if not isinstance(sections, dict) or not sections:
            raise ValueError("Document sections are missing.")

        return create_word_document(title, sections)

    elif skill_name == "powerpoint-creation":
        slides = data["slides"]

        if not isinstance(slides, list) or not slides:
            raise ValueError("Presentation slides are missing.")

        for slide in slides:
            if (
                not isinstance(slide, dict)
                or not isinstance(slide.get("title"), str)
                or not isinstance(slide.get("points"), list)
            ):
                raise ValueError("Invalid slide structure.")

        return create_presentation(title, slides)

    elif skill_name == "excel-creation":
        sheets = data["sheets"]

        if not isinstance(sheets, list) or not sheets:
            raise ValueError("Excel worksheets are missing.")

        for sheet in sheets:
            if (
                not isinstance(sheet, dict)
                or not isinstance(sheet.get("headers"), list)
                or not sheet["headers"]
                or not isinstance(sheet.get("rows", []), list)
            ):
                raise ValueError("Invalid Excel worksheet structure.")

        return create_excel(title, sheets)

    elif skill_name == "pdf-creation":
        sections = data["sections"]

        if not isinstance(sections, dict) or not sections:
            raise ValueError("PDF sections are missing.")

        return create_pdf(title, sections)

    raise ValueError(f"No tool registered for {skill_name}")


# -------------------------------
# 9. Main agent loop
# -------------------------------

def main():
    skills = load_skills()

    if not skills:
        raise RuntimeError(
            "No skills found. Check your skills folder and SKILL.md files."
        )

    print("\nAgent Skills loaded:")

    for skill in skills:
        print(f"- {skill['name']}")

    print("\nAsk me to create a Word, PowerPoint, Excel, or PDF file.")
    print("Type 'exit' to stop.\n")

    while True:
        user_request = input("You: ").strip()

        if user_request.lower() == "exit":
            break

        if not user_request:
            continue

        try:
            intent = detect_intent(user_request)

            if intent == "question":
                answer = answer_general_question(user_request)
                print(f"\nAgent: {answer}\n")
                continue

            skill = select_skill(user_request, skills)

            if skill is None:
                print(
                    "Agent: I couldn't identify a suitable "
                    "file-creation skill.\n"
                )
                continue

            print(f"\nSelected skill: {skill['name']}")

            data = generate_content(user_request, skill)

            file_path = None

            # Retry file creation once for operating-system errors.
            for attempt in range(2):
                try:
                    file_path = execute_skill(skill["name"], data)
                    break

                except (PermissionError, OSError) as error:
                    if attempt == 1:
                        raise

                    print(
                        "File creation failed. Retrying once... "
                        f"Error: {error}"
                    )

            if file_path is None:
                raise RuntimeError("File creation failed.")

            if not Path(file_path).is_file():
                raise RuntimeError(
                    "The tool returned a path, but the file does not exist."
                )

            print("\nTask completed successfully!")
            print(f"Skill used: {skill['name']}")
            print(f"File created: {file_path}\n")

            # Remember the request and generated file summary.
            conversation_history.extend([
                {
                    "role": "user",
                    "content": user_request,
                },
                {
                    "role": "assistant",
                    "content": (
                        f"Created a {skill['name']} file titled "
                        f"'{data['title']}'. "
                        f"Saved at: {file_path}"
                    ),
                },
            ])

            del conversation_history[:-10]

        except (json.JSONDecodeError, KeyError, ValueError) as error:
            print(f"Content or JSON error: {error}\n")

        except Exception as error:
            print(f"Execution error: {error}\n")


if __name__ == "__main__":
    main()
