# Credits to Cry4pt (On Discord)
# Open Sourced Malware
# Hitman 1/2/3 Profile Editor - (Peacock Needed)
# Credits To astra1dev (On Github) For Pull Request

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from shutil import get_terminal_size
import json
import os
import time
import ctypes
from pathlib import Path

# Set the TERM environment variable if not already set
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm-256color'

console = Console()

try:
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW("Created By Cry4pt")
except Exception:
    pass


def find_profile_directory():
    """
    Automatically searches for the directory 'Peacock\\userdata\\users'
    across common locations like all drives, Desktop, and Downloads.

    Returns:
        str: The path to the found directory or None if not found.
    """
    # Common base directories to search
    search_locations = [
        Path.home() / "Desktop",
        Path.home() / "Downloads",
        Path("C:\\"),
        Path("D:\\"),
        Path("E:\\"),
        Path("F:\\")
    ]

    # Target directory name
    target_path = os.path.join("Peacock", "userdata", "users")

    for base_path in search_locations:
        # Recursively search for the directory
        for root, dirs, files in os.walk(base_path):
            if target_path in root:
                return root

    return None


def format_json_file(file_path):
    """
    Formats a JSON file to have a consistent indentation.

    Args:
        file_path (str): The path to the JSON file to format.

    Returns:
        bool: True if the file was formatted successfully, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_data = file.read()
            if raw_data.startswith('\ufeff'):
                raw_data = raw_data[1:]
            data = json.loads(raw_data)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        console.print("[green]JSON file formatted successfully![/green]")
        return True
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return False


def calculate_hitman_xp(target_level):
    """
    Calculates the total XP required to reach a given level in Hitman.

    Args:
        target_level (int): The target level to calculate XP for.

    Returns:
        int: The total XP required to reach the target level.
    """
    REFERENCE_LEVEL = 16
    REFERENCE_XP = 95302
    xp_per_level = REFERENCE_XP / REFERENCE_LEVEL
    total_xp = xp_per_level * target_level
    return int(total_xp)


def find_and_replace_in_json(obj, new_level=None, new_xp=None, my_money=None, prestige_rank=None):
    """
    Recursively finds and replaces values in a JSON object.

    Args:
        obj (dict or list): The JSON object to modify.
        new_level (int, optional): The new level to set.
        new_xp (int, optional): The new XP to set.
        my_money (int, optional): The new money amount to set.
        prestige_rank (int, optional): The new prestige rank to set.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "ProfileLevel" and isinstance(value, (int, float)) and new_level is not None:
                obj[key] = new_level
            elif key == "PlayerProfileXP" and isinstance(value, dict) and new_xp is not None:
                if "Total" in value:
                    value["Total"] = new_xp
                if "ProfileLevel" in value and new_level is not None:
                    value["ProfileLevel"] = new_level
            elif key == "MyMoney" and my_money is not None:
                obj[key] = my_money
            elif key == "PrestigeRank" and prestige_rank is not None:
                obj[key] = prestige_rank
            elif isinstance(value, (dict, list)):
                find_and_replace_in_json(value, new_level, new_xp, my_money, prestige_rank)
    elif isinstance(obj, list):
        for item in obj:
            find_and_replace_in_json(item, new_level, new_xp, my_money, prestige_rank)


def get_current_values(file_path):
    """
    Retrieves the current values of level, money, and prestige rank from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        tuple: A tuple containing the current level, money, and prestige rank.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_data = file.read()
            if raw_data.startswith('\ufeff'):
                raw_data = raw_data[1:]
            data = json.loads(raw_data)

        def find_values(obj):
            level, money, prestige_rank = None, None, None
            if isinstance(obj, dict):
                if "ProfileLevel" in obj:
                    level = obj["ProfileLevel"]
                if "MyMoney" in obj:
                    money = obj["MyMoney"]
                if "PrestigeRank" in obj:
                    prestige_rank = obj["PrestigeRank"]
                for value in obj.values():
                    if isinstance(value, (dict, list)):
                        sub_level, sub_money, sub_rank = find_values(value)
                        level = level or sub_level
                        money = money or sub_money
                        prestige_rank = prestige_rank or sub_rank
            elif isinstance(obj, list):
                for item in obj:
                    sub_level, sub_money, sub_rank = find_values(item)
                    level = level or sub_level
                    money = money or sub_money
                    prestige_rank = prestige_rank or sub_rank
            return level, money, prestige_rank

        level, money, prestige_rank = find_values(data)
        return (
            f"{level:,}" if isinstance(level, (int, float)) else "N/A",
            f"{money:,}" if isinstance(money, (int, float)) else "N/A",
            f"{prestige_rank:,}" if isinstance(prestige_rank, (int, float)) else "N/A",
        )
    except Exception as e:
        console.print(f"[red]Error reading current values: {str(e)}[/red]")
        return None, None, None


def update_profile(file_path, new_level=None, my_money=None, prestige_rank=None):
    """
    Updates the profile JSON file with new values for level, money, and prestige rank.

    Args:
        file_path (str): The path to the JSON file.
        new_level (int, optional): The new level to set.
        my_money (int, optional): The new money amount to set.
        prestige_rank (int, optional): The new prestige rank to set.

    Returns:
        tuple: A tuple containing a boolean indicating success and a message.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_data = file.read()
            if raw_data.startswith('\ufeff'):
                raw_data = raw_data[1:]
            data = json.loads(raw_data)

        new_xp = calculate_hitman_xp(new_level) if new_level is not None else None
        backup_path = file_path + '.backup'
        os.replace(file_path, backup_path)

        find_and_replace_in_json(data, new_level, new_xp, my_money, prestige_rank)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        os.system('cls' if os.name == 'nt' else 'clear')  # Added compatibility for non-Windows systems

        header = Panel(
            "[bold cyan]Hitman Profile Editor[/bold cyan]",
            expand=False,
            border_style="bold green"
        )
        console.print(header, justify="center")

        # Create table for updated values
        table = Table(title="[bold yellow]Updated Values[/bold yellow]", show_header=True, header_style="bold magenta")
        table.add_column("Attribute", style="cyan", justify="center")
        table.add_column("Value", style="yellow", justify="center")

        # Add rows for each updated value
        if new_level is not None:
            table.add_row("Level", f"{new_level:,}")
            table.add_row("XP", f"{new_xp:,}")
        if my_money is not None:
            table.add_row("Merces", f"{my_money:,}")
        if prestige_rank is not None:
            table.add_row("Prestige Rank", f"{prestige_rank:,}")

        console.print(table, justify="center")
        console.print("")  # Add spacing

        # Center the "Press Enter" prompt
        prompt_message = "[bold cyan]                       Press Enter To Go Back [/bold cyan]"
        try:
            console_width = os.get_terminal_size().columns
        except OSError:
            console_width = 80
        prompt_length = len(prompt_message)
        padding = (console_width - prompt_length) // 2

        console.print(" " * padding + prompt_message, end="")
        console.input()

        return True, ""
    except Exception as e:
        return False, f"[red]Error: {str(e)}[/red]"


def display_input_prompt(title, prompt_text, file_path, value_type):
    """
    Displays an input prompt for the user to enter a new value.

    Args:
        title (str): The title of the prompt.
        prompt_text (str): The text to display in the prompt.
        file_path (str): The path to the JSON file.
        value_type (str): The type of value being prompted for (level, money, prestige).

    Returns:
        str: The user input.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    # Get current values
    current_level, current_money, current_prestige = get_current_values(file_path)

    # Determine which current value to show based on value_type
    current_value = ""
    if value_type == "level":
        current_value = current_level
    elif value_type == "money":
        current_value = current_money
    elif value_type == "prestige":
        current_value = current_prestige

    header = Panel(
        "[bold cyan]Hitman Profile Editor[/bold cyan]",
        expand=False,
        border_style="bold green"
    )
    console.print(header, justify="center")

    # Create input table
    table = Table(title=f"[bold yellow]{title}[/bold yellow]", show_header=True, header_style="bold magenta")
    table.add_column("Input Required", style="cyan", justify="center")
    table.add_column("Current Value", style="yellow", justify="center")
    table.add_row(prompt_text, str(current_value))
    console.print(table, justify="center")

    # Add spacing
    console.print("\n", end="")

    # Center the input prompt
    prompt_message = "[bold cyan]                 Enter Value[/bold cyan]"
    try:
        console_width = os.get_terminal_size().columns
    except OSError:
        console_width = 80
    prompt_length = len(prompt_message)
    padding = (console_width - prompt_length) // 2

    console.print(" " * padding + prompt_message, end="")
    return Prompt.ask("", default="0")


def display_multi_input_prompt(file_path, completed_inputs=None):
    """
    Displays a multi-input prompt for the user to enter multiple values.

    Args:
        file_path (str): The path to the JSON file.
        completed_inputs (dict, optional): A dictionary of already completed inputs.

    Returns:
        str: The user input or None if all inputs are completed.
    """
    if completed_inputs is None:
        completed_inputs = {}

    os.system('cls' if os.name == 'nt' else 'clear')

    # Get current values
    current_level, current_money, current_prestige = get_current_values(file_path)

    header = Panel(
        "[bold cyan]Hitman Profile Editor[/bold cyan]",
        expand=False,
        border_style="bold green"
    )
    console.print(header, justify="center")

    # Create table showing all current and input values
    table = Table(title="[bold yellow]Current Values[/bold yellow]", show_header=True, header_style="bold magenta")
    table.add_column("Attribute", style="cyan", justify="center")
    table.add_column("Current Value", style="yellow", justify="center")
    table.add_column("New Value", style="green", justify="center")

    # Add rows for all values
    table.add_row(
        "Level",
        str(current_level),
        str(completed_inputs.get('level', ''))
    )
    table.add_row(
        "Money",
        str(current_money),
        str(completed_inputs.get('money', ''))
    )
    table.add_row(
        "Prestige Rank",
        str(current_prestige),
        str(completed_inputs.get('prestige', ''))
    )

    console.print(table, justify="center")
    console.print("\n", end="")

    # Determine which input to show
    if 'level' not in completed_inputs:
        prompt_text = "[bold cyan]              Enter New Level[/bold cyan]"
    elif 'money' not in completed_inputs:
        prompt_text = "[bold cyan]                Enter New Money Amount[/bold cyan]"
    elif 'prestige' not in completed_inputs:
        prompt_text = "[bold cyan]                Enter New Prestige Rank[/bold cyan]"
    else:
        # If all inputs are completed, show the values for a moment before proceeding
        time.sleep(2)
        return None

    # Center the input prompt
    try:
        console_width = os.get_terminal_size().columns
    except OSError:
        console_width = 80
    prompt_length = len(prompt_text)
    padding = (console_width - prompt_length) // 2

    console.print(" " * padding + prompt_text, end="")
    return Prompt.ask("", default="0")


def main():
    file_path = None
    directory = find_profile_directory()

    if directory:
        console.print(f"[green]Found directory: {directory}[/green]")
        # Look for JSON files in the found directory
        for filename in os.listdir(directory):
            if filename.endswith(".json") and filename != "lop.json":
                file_path = os.path.join(directory, filename)
                break
    else:
        console.print(
            "[red]Unable to find the directory 'Peacock\\userdata\\users'. Please specify the file path manually.[/red]")
        file_path = Prompt.ask(
            "[bold cyan]Enter the path to your profile JSON file:[/bold cyan]",
            default="userdata.json"
        )

    if file_path and os.path.exists(file_path):
        console.print(f"[green]Using profile file: {file_path}[/green]")
    else:
        console.print("[red]Invalid file path provided or no JSON file found.[/red]")
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.clear()

        # Render a centered header using Rich
        header = Panel(
            "[bold cyan]Hitman Profile Editor[/bold cyan]",
            expand=False,
            border_style="bold green"
        )
        console.print(header, justify="center")

        # Create and display the menu table
        table = Table(title="[bold yellow]Options[/bold yellow]", show_header=True, header_style="bold magenta")
        table.add_column("Choice", style="cyan", justify="center")
        table.add_column("Action", style="yellow")

        table.add_row("1", "Edit Level")
        table.add_row("2", "Edit Money")
        table.add_row("3", "Edit Prestige Rank")
        table.add_row("4", "Edit Level, Money, Prestige Rank")
        table.add_row("5", "Display Current Values")
        table.add_row("6", "Format JSON File")
        table.add_row("7", "Exit")

        console.print(table, justify="center")

        # Add an empty line above the prompt
        console.print("\n", end="")

        # Calculate the padding to center the input prompt
        prompt_message = "[bold cyan]Enter your choice[/bold cyan]"
        try:
            console_width = os.get_terminal_size().columns
        except OSError:
            console_width = 80
        prompt_length = len(prompt_message)
        padding = (console_width - prompt_length) // 2

        # Print the prompt with calculated padding, and the input field right after it
        console.print(" " * padding + prompt_message, end="")

        # Prompt for user choice with no extra space between prompt and input
        choice = Prompt.ask("", choices=["1", "2", "3", "4", "5", "6", "7"], default="")

        if choice == "7":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        elif choice == "1":
            new_level_input = display_input_prompt("Level Editor", "Enter New Level", file_path, "level")
            try:
                new_level = int(new_level_input)
                if new_level > 0:
                    success, message = update_profile(file_path, new_level=new_level)
                    if not success:
                        console.print(message)
                else:
                    console.print("[bold red]Please enter a valid level greater than 0.[/bold red]")
            except ValueError:
                console.print("[bold red]Invalid input for level. Please enter a number.[/bold red]")

        elif choice == "2":
            my_money_input = display_input_prompt("Money Editor", "Enter Money Amount", file_path, "money")
            try:
                my_money = int(my_money_input)
                success, message = update_profile(file_path, my_money=my_money)
                if not success:
                    console.print(message)
            except ValueError:
                console.print("[bold red]Invalid input for money amount. Please enter a valid number.[/bold red]")

        elif choice == "3":
            prestige_rank_input = display_input_prompt("Prestige Rank Editor", "Enter Prestige Rank", file_path,
                                                       "prestige")
            try:
                prestige_rank = int(prestige_rank_input)
                success, message = update_profile(file_path, prestige_rank=prestige_rank)
                if not success:
                    console.print(message)
            except ValueError:
                console.print("[bold red]Invalid input for prestige rank. Please enter a valid number.[/bold red]")

        elif choice == "4":
            completed_inputs = {}

            # Get level input
            while True:
                new_level_input = display_multi_input_prompt(file_path, completed_inputs)
                if new_level_input is None:
                    break
                try:
                    new_level = int(new_level_input)
                    if new_level <= 0:
                        console.print("[bold red]Please enter a valid level greater than 0.[/bold red]")
                        continue
                    completed_inputs['level'] = f"{new_level:,}"
                    break
                except ValueError:
                    console.print("[bold red]Invalid input for level. Please enter a number.[/bold red]")
                    continue

            # Get money input
            while True and new_level_input is not None:
                my_money_input = display_multi_input_prompt(file_path, completed_inputs)
                if my_money_input is None:
                    break
                try:
                    my_money = int(my_money_input)
                    completed_inputs['money'] = f"{my_money:,}"
                    break
                except ValueError:
                    console.print("[bold red]Invalid input for money amount. Please enter a valid number.[/bold red]")
                    continue

            # Get prestige rank input
            while True and my_money_input is not None:
                prestige_rank_input = display_multi_input_prompt(file_path, completed_inputs)
                if prestige_rank_input is None:
                    break
                try:
                    prestige_rank = int(prestige_rank_input)
                    completed_inputs['prestige'] = f"{prestige_rank:,}"
                    # Display the final state with all inputs
                    display_multi_input_prompt(file_path, completed_inputs)
                    break
                except ValueError:
                    console.print("[bold red]Invalid input for prestige rank. Please enter a valid number.[/bold red]")
                    continue

            if all(key in completed_inputs for key in ['level', 'money', 'prestige']):
                success, message = update_profile(
                    file_path,
                    new_level=int(new_level_input),
                    my_money=int(my_money_input),
                    prestige_rank=int(prestige_rank_input)
                )
                if not success:
                    console.print(message)

        elif choice == "6":
            os.system('cls' if os.name == 'nt' else 'clear')
            format_json_file(file_path)

        elif choice == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            level, money, prestige_rank = get_current_values(file_path)
            if level is not None:
                header = Panel(
                    "[bold cyan]Hitman Profile Editor[/bold cyan]",
                    expand=False,
                    border_style="bold green"
                )
                console.print(header, justify="center")
                table = Table(title="[bold yellow]Current Values[/bold yellow]", show_header=True,
                              header_style="bold magenta")
                table.add_column("Attribute", style="cyan", justify="center")
                table.add_column("Value", style="yellow", justify="center")
                table.add_row("Level", str(level))
                table.add_row("Money", str(money))
                table.add_row("Prestige Rank", str(prestige_rank))
                console.print(table, justify="center")
            else:
                console.print("[bold red]Failed to retrieve values.[/bold red]")

            # Add an empty line above the prompt
            console.print("\n", end="")

            # Calculate the padding to center the input prompt
            prompt_message = "[bold cyan]                       Press Enter To Go Back [/bold cyan]"
            try:
                console_width = os.get_terminal_size().columns
            except OSError:
                console_width = 80
            prompt_length = len(prompt_message)
            padding = (console_width - prompt_length) // 2

            # Print the prompt with calculated padding, and the input field right after it
            console.print(" " * padding + prompt_message, end="")
            console.input()


if __name__ == "__main__":
    main()
