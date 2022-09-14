import pyperclip
import curses
from curses import wrapper

items = pyperclip.paste().strip().splitlines()
items = [item.strip() for item in items]


lines = len(items)
lineNoWidth = len(str(lines))
padding = lineNoWidth + 2

down = {456, 258, 106} # VSCode down arrow, down arrow, J
up =  {450, 259, 107} # VSCode up arrow, up arrow, K
read =  {452, 260, 100, 104} # VSCode left arrow, left arrow, D, H
move = {454, 261, 102, 108} # VSCode right arrow, right arrow, F, L
quit = {27, 113} # Escape, Q

def main(stdscr):
    if lines + 2 > curses.LINES:
        raise(ValueError(f"Window must be at least {lines + 2} lines tall"))
 
    curses.curs_set(0) # Hide cursor

    # Print top line
    stdscr.addstr(0, 0, "MODE:            MOVE (F/L)")
    stdscr.addstr(0, 6, "READ (D/H)", curses.A_STANDOUT)
    mode = "read"

    # Print bottom line
    stdscr.addstr(lines + 1, 0, "Q TO QUIT")

    maxAllowedLen = curses.COLS - padding
    # Print items
    # Print first item
    stdscr.addstr(1, 0, f"{1:>{lineNoWidth}d}.")
    stdscr.addstr(1, padding, items[0][:maxAllowedLen], curses.A_STANDOUT)

    # Print remaining items
    for item, lineNo in zip(items, range(2, lines+1)):
                stdscr.addstr(lineNo, 0, f"{lineNo:>{lineNoWidth}d}. {item[:maxAllowedLen]}")

    clearLine = " " * maxAllowedLen # This will be used later to clear items

    selectedLine = 1
    key = 0

    while key not in quit:
        stdscr.refresh()
        key = stdscr.getch()

        prevSelectedLine = selectedLine # Technically not true if the input changes the mode but if that is the case then prevSelectedLine isn't used anyway

        if key in down:
            selectedLine += 1
            if selectedLine > lines: selectedLine = lines

        elif key in up:
            selectedLine -= 1
            if selectedLine < 1: selectedLine = 1

        elif key in read:
            stdscr.addstr(0, 6, "READ (D/H)", curses.A_STANDOUT)
            stdscr.addstr(0, 17, "MOVE (F/L)")
            mode = "read"
            continue

        elif key in move:
            stdscr.addstr(0, 6, "READ (D/H)")
            stdscr.addstr(0, 17, "MOVE (F/L)", curses.A_STANDOUT)
            mode = "move"
            continue

        if mode == "move":
            items.insert(selectedLine - 1, items.pop(prevSelectedLine - 1)) # This moves the item from index prevSelectedLine - 1 to index selectedLine - 1
            pyperclip.copy("\n".join(items)) # Add new order to clipboard 

        # Update and unhighlight the previous line
        stdscr.addstr(prevSelectedLine, padding, clearLine)
        stdscr.addstr(prevSelectedLine, padding, items[prevSelectedLine - 1][:maxAllowedLen])

        # Update and highlight new line
        stdscr.addstr(selectedLine, padding, clearLine)
        stdscr.addstr(selectedLine, padding, items[selectedLine - 1][:maxAllowedLen], curses.A_STANDOUT)
  
wrapper(main)

