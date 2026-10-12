from rich.console  import Console
from rich.markdown import Markdown
from openai        import OpenAI

console = Console(highlight = False)
client = OpenAI()

def main():
    console.print("Patois client 2a", style = "reverse gold1")
    print("Copyright (C) 1999 G.C. Looa")
    print("Enter \"/exit\" to quit.")

    thinking_animation = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    frame = 0

    response_prev = None
    PROGRAM_RUNNING = True
    
    while PROGRAM_RUNNING:
        userinput = input("████ ")

        if userinput == "/exit":
            PROGRAM_RUNNING = False
            break

        if response_prev == None:
            response = client.responses.create(
                model                = "gpt-5.4-mini",
                input                = userinput,
                background           = True
            )
        else:
            response = client.responses.create(
                model                = "gpt-5.4-mini",
                previous_response_id = response_prev.id,
                input                = userinput,
                background           = True
            )

        while response.status in {"queued", "in_progress"}:
            console.print(
                "[reverse gold1] •-•[/] " + thinking_animation[frame] + " ",
                end = "\r",
                style = "gold1"
            )
            frame = (frame + 1) % len(thinking_animation)
            response = client.responses.retrieve(response.id)
        response_prev = response

        # console.log(response.output_text)
        response_md = Markdown(response.output_text)
        console.print("[reverse gold1] •-•[/] ", style = "gold1", end = "")
        console.print(response_md, style = "gold1", soft_wrap = True)

if __name__ == "__main__":
    main()
