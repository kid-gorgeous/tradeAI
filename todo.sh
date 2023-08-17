#!/bin/bash

# Define the file to store the todo list
TODO_FILE="$HOME/todo.txt"

# Check if the todo file exists, and create it if it doesn't
if [ ! -e "$TODO_FILE" ]; then
    touch "$TODO_FILE"
fi

# Function to add a task to the todo list
add_task() {
    read -p "Enter task: " task
    read -p "Enter due date (YYYY-MM-DD): " due_date
    read -p "Enter priority level (High/Medium/Low): " priority
    echo "$due_date | $priority | $task" >> "$TODO_FILE"
    echo "Task added: $task"
}

# Function to list all tasks in the todo list
list_tasks() {
    if [ -s "$TODO_FILE" ]; then
        echo "Todo List:"
        cat -n "$TODO_FILE"
    else
        echo "Todo list is empty."
    fi
}

# Function to remove a task from the todo list
remove_task() {
    if [ -s "$TODO_FILE" ]; then
        list_tasks
        read -p "Enter the task number to remove: " task_number
        sed -i "${task_number}d" "$TODO_FILE"
        echo "Task removed."
    else
        echo "Todo list is empty."
    fi
}

# Function to schedule a sound notification
schedule_notification() {
    local notification_time="$1"
    local notification_message="$2"
    echo "$notification_message" | at "$notification_time"
}

# Main loop
while true; do
    clear
    echo "Bash Todo App"
    echo "1. Add Task"
    echo "2. List Tasks"
    echo "3. Remove Task"
    echo "4. Exit"
    read -p "Select an option: " choice

    case $choice in
        1)
            add_task
            ;;
        2)
            list_tasks
            ;;
        3)
            remove_task
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please select a valid option."
            ;;
    esac

    read -p "Press Enter to continue..."
done


# Save this script to a file named todo.sh, then make it executable using the command chmod +x todo.sh. You can run the app by executing ./todo.sh in your terminal.

