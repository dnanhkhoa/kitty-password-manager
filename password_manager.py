import re
from termios import ECHO, ICANON, ISIG, tcgetattr

from kittens.tui.handler import result_handler


def main():
    pass


@result_handler(no_ui=True)
def handle_result(_, __, window_id, boss):
    window = boss.window_id_map.get(window_id)

    if window:
        c_lflag = tcgetattr(window.child.child_fd)[3]

        if c_lflag & (ECHO | ICANON | ISIG) == (ICANON | ISIG) or re.search(
            r"\bPass(phrase|word)\b.*?:",
            window.as_text().strip().split("\n")[-1].strip(),
            flags=re.IGNORECASE,
        ):
            boss.call_remote_control(
                window,
                (
                    "launch",
                    "--title=KITTY PASSWORD MANAGER",
                    "--type=overlay",
                    "--env",
                    f"KITTY_PASSWORD_MANAGER={window_id}",
                    "--allow-remote-control",
                ),
            )
