# Credits to Cry4pt (On Discord)
# Open Sourced Malware
# Hitman 1/2/3 Profile Editor - (Peacock Needed)

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import json
import os
import time
import ctypes
from pathlib import Path

XP_PER_LEVEL = 6000  # Define the XP required for each level

# Set the TERM environment variable if not already set
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm-256color'

console = Console()

try:
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW("Created By Cry4pt")
except Exception:
    pass


def find_profile_directory() -> str or None:
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


def read_json_file(file_path) -> dict or None:
    """
    Reads a JSON file and returns its content as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_data = file.read()
            if raw_data.startswith('\ufeff'):
                raw_data = raw_data[1:]
            return json.loads(raw_data)
    except Exception as e:
        console.print(f"[red]Error reading JSON file: {str(e)}[/red]")
        return None


def write_json_file(file_path: str, data: dict) -> None:
    """
    Writes a dictionary to a JSON file with formatted indentation.

    Args:
        file_path (str): The path to the JSON file to format.
        data (dict): The JSON data to write to the file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        console.print("[green]JSON file formatted successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error writing JSON file: {str(e)}[/red]")


def calculate_level(xp: int) -> int:
    """
    Calculates the level for the given XP based on XP_PER_LEVEL.
    Minimum level returned is 1.
    """
    return max(1, (xp // XP_PER_LEVEL) + 1)

def calculate_xp(target_level: int) -> int:
    """
    Calculates the required XP for the given level based on XP_PER_LEVEL.
    Minimum XP returned is 0.
    """
    return max(0, (target_level - 1) * XP_PER_LEVEL)

def find_and_replace_in_json(obj: dict, new_level: int = None, new_xp: int = None, my_money: int = None, prestige_rank: int = None) -> None:
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


def get_current_values(file_path: str) -> tuple:
    """
    Retrieves the current values from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        tuple: A tuple containing the current level, xp, money, and prestige rank.
    """
    try:
        data = read_json_file(file_path)

        def find_values(obj):
            level, xp, money, prestige_rank = None, None, None, None
            if isinstance(obj, dict):
                if "ProfileLevel" in obj:
                    level = obj["ProfileLevel"]
                if "PlayerProfileXP" in obj:
                    if "Total" in obj["PlayerProfileXP"]:
                        xp = obj["PlayerProfileXP"]["Total"]
                if "MyMoney" in obj:
                    money = obj["MyMoney"]
                if "PrestigeRank" in obj:
                    prestige_rank = obj["PrestigeRank"]
                for value in obj.values():
                    if isinstance(value, (dict, list)):
                        sub_level, sub_xp, sub_money, sub_rank = find_values(value)
                        level = level or sub_level
                        xp = xp or sub_xp
                        money = money or sub_money
                        prestige_rank = prestige_rank or sub_rank
            elif isinstance(obj, list):
                for item in obj:
                    sub_level, sub_xp, sub_money, sub_rank = find_values(item)
                    level = level or sub_level
                    xp = xp or sub_xp
                    money = money or sub_money
                    prestige_rank = prestige_rank or sub_rank
            return level, xp, money, prestige_rank

        level, xp, money, prestige_rank = find_values(data)
        return (
            f"{level:,}" if isinstance(level, (int, float)) else "N/A",
            f"{xp:,}" if isinstance(xp, (int, float)) else "N/A",
            f"{money:,}" if isinstance(money, (int, float)) else "N/A",
            f"{prestige_rank:,}" if isinstance(prestige_rank, (int, float)) else "N/A",
        )
    except Exception as e:
        console.print(f"[red]Error reading current values: {str(e)}[/red]")
        return None, None, None, None


def create_header_panel() -> Panel:
    return Panel(
        "[bold cyan]Hitman Profile Editor[/bold cyan]",
        expand=False,
        border_style="bold green"
    )


def update_profile(file_path: str, new_level: int = None, new_xp:int = None, my_money: int = None, prestige_rank:int = None) -> tuple:
    """
    Updates the profile JSON file with new values for level, xp, money, and prestige rank.

    Args:
        file_path (str): The path to the JSON file.
        new_level (int, optional): The new level to set.
        new_xp (int, optional): The new xp to set.
        my_money (int, optional): The new money amount to set.
        prestige_rank (int, optional): The new prestige rank to set.

    Returns:
        tuple: A tuple containing a boolean indicating success and a message.
    """
    try:
        data = read_json_file(file_path)

        # Calculate new_level and new_xp if either is provided
        if new_xp is not None:
            new_level = calculate_level(new_xp)
        elif new_level is not None:
            new_xp = calculate_xp(new_level)

        # Backup the original file
        backup_path = file_path + '.bak'
        os.replace(file_path, backup_path)

        # Update the data with new values
        find_and_replace_in_json(data, new_level, new_xp, my_money, prestige_rank)

        # Write the updated data back to the file
        write_json_file(file_path, data)

        # Clear the console for a clean display
        console.clear()

        # Display the updated values
        header = create_header_panel()
        console.print(header, justify="center")

        table = Table(title="[bold yellow]Updated Values[/bold yellow]", show_header=True, header_style="bold magenta")
        table.add_column("Attribute", style="cyan", justify="center")
        table.add_column("Value", style="yellow", justify="center")

        # Add rows for each updated value
        if new_level is not None:
            table.add_row("Level", f"{new_level:,}")
            table.add_row("XP", f"{new_xp:,}")
        if my_money is not None:
            table.add_row("Money", f"{my_money:,}")
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
    """
    console.clear()

    # Get current values (now properly unpacking 4 values)
    current_level, current_xp, current_money, current_prestige = get_current_values(file_path)

    # Determine which current value to show based on value_type
    current_value = ""
    if value_type == "level":
        current_value = current_level
    elif value_type == "xp":
        current_value = current_xp
    elif value_type == "money":
        current_value = current_money
    elif value_type == "prestige":
        current_value = current_prestige

    header = create_header_panel()
    console.print(header, justify="center")

    # Create input table
    table = Table(title=f"[bold yellow]{title}[/bold yellow]", show_header=True, header_style="bold magenta")
    table.add_column("Input Required", style="cyan", justify="center")
    table.add_column("Current Value", style="yellow", justify="center")
    table.add_row(prompt_text, str(current_value))
    console.print(table, justify="center")

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
    """
    if completed_inputs is None:
        completed_inputs = {}

    console.clear()

    # Get current values (now properly unpacking 4 values)
    current_level, current_xp, current_money, current_prestige = get_current_values(file_path)

    header = create_header_panel()
    console.print(header, justify="center")

    # Create table showing all current and input values
    table = Table(title="[bold yellow]Current Values[/bold yellow]", show_header=True, header_style="bold magenta")
    table.add_column("Attribute", style="cyan", justify="center")
    table.add_column("Current Value", style="yellow", justify="center")
    table.add_column("New Value", style="green", justify="center")

    # Calculate XP if level is provided
    if 'level' in completed_inputs:
        level = int(completed_inputs['level'].replace(',', ''))
        xp = calculate_xp(level)
        completed_inputs['xp'] = f"{xp:,}"
    
    # Add rows for all values
    table.add_row(
        "Level",
        str(current_level),
        str(completed_inputs.get('level', ''))
    )
    table.add_row(
        "XP",
        str(current_xp),
        str(completed_inputs.get('xp', ''))
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

    # Rest of the prompts
    if 'level' not in completed_inputs:
        prompt_text = "[bold cyan]              Enter New Level[/bold cyan]"
    elif 'money' not in completed_inputs:
        prompt_text = "[bold cyan]                Enter New Money Amount[/bold cyan]"
    elif 'prestige' not in completed_inputs:
        prompt_text = "[bold cyan]                Enter New Prestige Rank[/bold cyan]"
    else:
        time.sleep(2)
        return None

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
        console.clear()

        header = create_header_panel()
        console.print(header, justify="center")

        table = Table(title="[bold yellow]Options[/bold yellow]", show_header=True, header_style="bold magenta")
        table.add_column("Choice", style="cyan", justify="center")
        table.add_column("Action", style="yellow")

        table.add_row("1", "Edit Level")
        table.add_row("2", "Edit XP")
        table.add_row("3", "Edit Money")
        table.add_row("4", "Edit Prestige Rank")
        table.add_row("5", "Edit Level, Money, Prestige Rank")
        table.add_row("6", "Display Current Values")
        table.add_row("7", "Format JSON File")
        table.add_row("8", "Exit")

        console.print(table, justify="center")
        console.print("\n", end="")

        try:
            console_width = os.get_terminal_size().columns
        except OSError:
            console_width = 80
        prompt_message = "[bold cyan]                                        Enter Your Choice[/bold cyan] [bold magenta][1/2/3/4/5/6/7/8][/bold magenta] [bold cyan]()[/bold cyan]: "
        prompt_length = len(prompt_message)
        padding = (console_width - prompt_length) // 2

        console.print(" " * padding + prompt_message, end="")
        
        # Modified input handling
        choice = console.input()
        
        # Check if input is valid
        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            continue  # Skip back to start of loop if invalid input
            
        if choice == "8":
            console.clear()
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
            new_xp_input = display_input_prompt("XP Editor", "Enter New XP", file_path, "xp")
            try:
                new_xp = int(new_xp_input)
                if new_xp > 0:
                    success, message = update_profile(file_path, new_xp=new_xp)
                    if not success:
                        console.print(message)
                else:
                    console.print("[bold red]Please enter a valid xp greater than 0.[/bold red]")
            except ValueError:
                console.print("[bold red]Invalid input for xp. Please enter a number.[/bold red]")

        elif choice == "3":
            my_money_input = display_input_prompt("Money Editor", "Enter Money Amount", file_path, "money")
            try:
                my_money = int(my_money_input)
                success, message = update_profile(file_path, my_money=my_money)
                if not success:
                    console.print(message)
            except ValueError:
                console.print("[bold red]Invalid input for money amount. Please enter a valid number.[/bold red]")

        elif choice == "4":
            prestige_rank_input = display_input_prompt("Prestige Rank Editor", "Enter Prestige Rank", file_path,
                                                       "prestige")
            try:
                prestige_rank = int(prestige_rank_input)
                success, message = update_profile(file_path, prestige_rank=prestige_rank)
                if not success:
                    console.print(message)
            except ValueError:
                console.print("[bold red]Invalid input for prestige rank. Please enter a valid number.[/bold red]")

        elif choice == "5":
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

        elif choice == "7":
            console.clear()
            data = read_json_file(file_path)
            write_json_file(file_path, data)

        elif choice == "6":
            console.clear()
            level, xp, money, prestige_rank = get_current_values(file_path)
            if level is not None:
                header = create_header_panel()
                console.print(header, justify="center")
                table = Table(title="[bold yellow]Current Values[/bold yellow]", show_header=True,
                              header_style="bold magenta")
                table.add_column("Attribute", style="cyan", justify="center")
                table.add_column("Value", style="yellow", justify="center")
                table.add_row("Level", str(level))
                table.add_row("XP", str(xp))
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
