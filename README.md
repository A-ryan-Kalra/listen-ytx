<div align='center'>
  
# listen-ytx 🗣️📝

#### Listen is a sleek, command-line-fist to-do list📝 manager built for powerful users. It lets you manage you daily task directly from the CLI with intutive commands that feels like natural language.

<video src="https://github.com/user-attachments/assets/77903333-37d9-4f88-9d99-385dbee61288" autoplay muted loop />


</div>

<br/>

# Contents

- [💎 Features](#-features)
  - [ 🚀 Key Functionalities](#-add-remove-and-mark-tasks-as-done)
- [👨‍💻 Commands](#-commands)
- [🚀 Installation](#-installation)
- [🚮 Uninstalling](#-uninstalling)

<br/>

## 💎 Features

- ##### 📌 Add, remove, and mark tasks as done.
- ##### 🧾 Clean, readable output.
- ##### 📂 Persist tasks between sessions, leveraging streams; storing data into json file in the root directory.

<br/>


##### Just "tell" it what to do:

> [!TIP]
> listen add "Go for shopping"  
> `add task to the list`
>
> listen show  
> `show all the tasks`
>
> listen done 2  
> `mark 2nd task as done`
>
> listen remove 1  
> `remove 2nd task from the lists`

🧠 No clutter. No distractions. Just type and track.

<br/>

## 👨‍💻 Commands

```bash
listen
# Greets user with name and time,showing all the current task to do.

listen add "Task Name"
# Add a task.

listen remove <Task-Number>
# Remove a task from the lists.

listen do <Task-Number>
# Mark task as done.

listen undo <Task-Number>
# Mark task as undone.

listen edit <Task-Number> "Edit-Task"
# Edit a task.

listen lists
# List all tasks.

listen swap <Old-Number> <New-Number>
# Swap the position of the old task with the new one.

listen move <Old-Number> <New-Number>
# Move a task to a specific position in the lists.

listen callme "New Name"
# Change your name.

listen changetimeformat
# Change time format.

listen clearall
# Clear all the tasks.
```

<br/>

## 🚀 Installation

Make sure you have Python 3.7+ installed.

```bash
pip install listen-ytx
# If you see an error saying 'pip not found', just replace 'pip' with 'pip3'.

listen
# run this command to begin the game.
```

<br/>

## 🚮 Uninstalling

Open your terminal and type:

```bash
pip uninstall arcade-ytx
```

`(Optional)`
and also remove the listen-ytx directory located in the .config directory in the root folder.

<br/>

<details>
  <summary>You know what's absolutely free?</summary>

- Leaving a ⭐ star
- 🍴Forking the repository
- No hidden fees, no subscriptions — just pure open-source love🥰!

</details>

<br/>

<div align="center">
Pleasure contributing 🕶️ <br>
Aryan Kalra

</div>
