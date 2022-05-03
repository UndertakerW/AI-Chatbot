import time


def get_user_choice(text):
    print('---------------------')
    print('Please make a choice:')
    print('1. Check my affair list')
    print('2. Add an affair')
    print('3. Modify an affair')
    print('4. Delete an affair')
    print('5. Exit')
    user_input = int(text)
    print('---------------------')
    return user_input


def warning_message():
    print('WARNING: exiting the program will clear all your data!')
    print('Continue? yes/no')
    if input() == 'yes':
        return True
    return False


def handle_user_request(choice, checklist, datelist):
    if choice == 1:
        if len(checklist) == 0:
            print('Your list is empty!')
        range_user_lists(checklist, datelist)
        for i in range(0, len(checklist)):
            print(i + 1, checklist[i], datelist[i], "is the ddl")
        return checklist, datelist
    if choice == 2:
        entry_time = input('Type the ddl time here: ')
        datelist.append(entry_time)
        new_entry = input('Type you new to-do here: ')
        checklist.append(new_entry)
        print('Your affair has been added successfully!')
        return checklist, datelist
    if choice == 3:
        if len(checklist) == 0:
            print("Your list is empty! Nothing can be modified.")
            return checklist, datelist
        print('Which do you want to modify? Please enter its index.')
        for i in range(0, len(checklist)):
            print(i + 1, checklist[i], datelist[i])
        index = int(input()) - 1
        datelist[index] = input('Type your new time here: ')
        checklist[index] = input('Type your new to-do here: ')
        print('Your affair has been modified successfully!')
        return checklist, datelist
    if choice == 4:
        if len(checklist) == 0:
            print("Your list is empty! Nothing can be deleted.")
            return checklist
        print('Which do you want to delete? Please enter its index.')
        for i in range(0, len(checklist)):
            print(i + 1, checklist[i], datelist[i])
        index = int(input()) - 1
        del datelist[index]
        del checklist[index]
        print('Your affair has been deleted successfully!')
        return checklist, datelist


def range_user_lists(checklist, datelist):
    localtime = time.localtime(time.time())
    month = localtime[1]
    day = localtime[2]
    for i in range(0, len(datelist)):
        ddl = datelist[i].split('.')
        ddl_month = int(ddl[0])
        ddl_day = int(ddl[1])
        if month - ddl_month < 0:
            checklist[i] = checklist[i] + " has Expired"
        elif month - ddl_month == 0 and day - ddl_day > 0:
            checklist[i] = checklist[i] + " has Expired"
        elif month - ddl_month == 0 and day - ddl_day == 0:
            checklist[i] = checklist[i] + " ★★★"
            checklist[0], checklist[i] = checklist[i], checklist[0]
            datelist[i] = 'Today'
        elif month - ddl_month == 0 and day - ddl_day < 0:
            checklist[i] = checklist[i] + " ★"
        else:
            pass


def schedule(ui, text):
    checklist = []
    datelist = []
    while True:
        choice = get_user_choice(text)
        if choice < 1 or choice > 5:
            print('Invalid input!')
            continue
        if choice == 5:
            if warning_message():
                print('Goodbye!')
                break
        else:
            handle_user_request(choice, checklist, datelist)


# Main function
if __name__ == '__main__':
    pass
