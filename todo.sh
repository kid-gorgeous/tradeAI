#!/bin/bash

# Define the file to store the todo list
TODO_FILE="$HOME/.todo"

# Check if the todo file exists, and create it if it doesnt
if [ ! -f $TODO_FILE ]; then
    touch $TODO_FILE
fi

# Function to add a task to the todo list
add_task() {
    echo "$1" >> "$TODO_FILE"
    echo "Task added: $1"
}

# Function to list all tasks in the todo list
list_tasks() {
    if [ -s "$TODO_FILE" ]; then
        echo "Todo List:"
        cat -n "$TODO_FILE"
    else
        echo "No tasks in list"
    fi
}

# Function to remove a task from the todo list
remove_task() {
    if [ -s "$TODO_FILE" ]; then
        line_number=$1
        sed -i "${line_number}d" "$TODO_FILE"
        echo "Task removed: $line_number"
    else
        echo "No tasks in list"
    fi
}

# Main loop
while true; do
    clear
    echo "Bash Todo App"
    echo "1. Add Task"
    echo "2. List Tasks"
    echo "3. Remove Task"
    echo "4. Exit"
    read -p "Enter your choice: " choice

    case $choice in
        1)
            read -p "Enter task name: " task
            add_task "$task"
            read -p "Press enter to continue"
            ;;
        2)
            list_tasks
            read -p "Press enter to continue"
            ;;
        3)
            list_tasks
            read -p "Enter task number to remove: " task_number
            remove_task "$task_number"
            read -p "Press enter to continue"
            ;;

        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice"
            read -p "Press enter to continue"
            ;;
    esac

    read -p "Press enter to continue..."
done

# Save this script to a file named `todo.sh`, then make it
#  executable with `chmod +x todo.sh`. Run it with `./todo.sh`.