

def main():
    while True:
        print("\n1. New User")
        print("2. Login User")
        print("3. Login Staff")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            username = input("Create username: ")
            password = input("Create password: ")
            register(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login(username, password):
                print(f"User '{username}' logged in.")
                show_menu_after_login(username)
        elif choice == '3':
            staff_username = input("Enter staff username: ")
            staff_password = input("Enter staff password: ")
            if login_staff(staff_username, staff_password):
                print(f"Staff '{staff_username}' logged in.")
                show_menu_after_login(staff_username, is_staff=True)
            else:
                print("Sorry, this is not a staff member.")
        elif choice == '4':
            print("Program closed. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


def login(username, password):
    user = next((user for user in users if
                 user['username'] == username and user['password'] == password and user['role'] == 'user'), None)
    return user is not None


def login_staff(username, password):
    staff = next((user for user in users if
                  user['username'] == username and user['password'] == password and user['role'] == 'staff'), None)
    return staff is not None


def register(username, password):
    if any(user['username'] == username for user in users):
        print(f"Username '{username}' is already taken. Please choose a different username.")
    else:
        users.append({'username': username, 'password': password, 'favorites': [], 'role': 'user'})
        print(f"User '{username}' has been registered successfully. Please login!")


def login_after_register(username, password):
    print(f"\nLogging in user '{username}' after registration.")
    login(username, password)


def display_all_places(all_cities, user_locations):
    print("\nAll Places:")

    all_locations = []

    for city in all_cities:
        all_locations.extend(city.hotels)
        all_locations.extend(city.apartments)

    # Include user-added locations
    all_locations.extend(user_locations)

    # Bubble sort by name
    n = len(all_locations)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if all_locations[j]['Place'] > all_locations[j + 1]['Place']:
                all_locations[j], all_locations[j + 1] = all_locations[j + 1], all_locations[j]

    for location in all_locations:
        if 'type' in location:
            # User-added location
            print(f"\nUser-Added Location: {location['Place']} ({location['type']}) - "
                  f"Availability: {location.get('availability', 5)} rooms")
        else:
            # City
            print(f"\nCity: {location['Place']}")

            # Check if the location is a hotel or an apartment
            if 'type' in location:
                print(f"{location['type']}: {location['name']}")
            else:
                print(location['Place'])

    # Include user-added locations
    print("\nUser-Added Locations:")
    # Bubble sort user-added locations by name
    n_user_locations = len(user_locations)
    for i in range(n_user_locations - 1):
        for j in range(0, n_user_locations - i - 1):
            if user_locations[j]['Place'] > user_locations[j + 1]['Place']:
                user_locations[j], user_locations[j + 1] = user_locations[j + 1], user_locations[j]

    print("\n".join([
        f"{i}. {location['Place']} ({location['type']}) - "
        f"Availability: {location.get('availability', 5)} rooms"
        for i, location in enumerate(user_locations, start=len(all_locations) + 1)
    ]))


def search_location_type():
    location_type = input("Enter the type of location to search (Apartment/Hotel): ").capitalize()
    matching_locations = []

    for city in cities:
        if location_type == 'Apartment':
            matching_locations.extend(city.apartments)
        elif location_type == 'Hotel':
            matching_locations.extend(city.hotels)

    if matching_locations:
        print(f"\nMatching {location_type}s: ")
        for i, location in enumerate(matching_locations, start=1):
            print(f"{i}. {location['Place']} - Availability: {location.get('availability', 5)} rooms")
    else:
        print(f"\nNo {location_type}s found.")


def show_faq(is_staff=False):
    while True:
        print("\nFrequently Asked Questions:")
        for i, question in enumerate(faq_list, start=1):
            print(f"{i}. {question}")

        if is_staff:
            print("\nOptions:")
            print("0. Go back to the main menu")
            print("A. Answer a question")
        else:
            print("\nOptions:")
            print("0. Go back to the main menu")
            print("A. Ask a question")

        choice = input("Enter your choice (0/A): ")

        if choice == '0':
            return
        elif is_staff and choice.upper() == 'A':
            # Staff member answering a question
            try:
                question_index = int(input("Enter the number of the question to answer: "))
                if 1 <= question_index <= len(faq_list):
                    print(f"Answer to Question {question_index}: ...")  # Add corresponding answer
                else:
                    print("Invalid question number. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif not is_staff and choice.upper() == 'A':
            # User asking a new question
            new_question = input("Enter your new question: ")
            faq_list.append(new_question)
            print("Question added successfully!")
        else:
            try:
                choice_index = int(choice)
                if 0 < choice_index <= len(faq_list):
                    print(f"Answer to Question {choice_index}: ...")  # Add corresponding answer
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid choice. Please enter 0, A, or a valid number.")


def book_now(selected_city, all_cities, user_locations):
    print("\nBooking a room:")
    # Display available locations for booking
    display_all_places(all_cities, user_locations)
    try:
        choice = int(input("Enter the number of the location you want to book: "))

        if 1 <= choice <= len(selected_city.hotels):
            selected_location = selected_city.hotels[choice - 1]
        elif 1 <= choice <= len(selected_city.apartments):
            selected_location = selected_city.apartments[choice - len(selected_city.hotels) - 1]
        elif len(selected_city.hotels) + 1 <= choice <= len(selected_city.hotels) + len(user_locations):
            selected_location = user_locations[choice - len(selected_city.hotels) - 1]
        else:
            print("Invalid choice. Please enter a valid number.")
            return

        print(f"\nYou've selected '{selected_location['Place']}' for booking.")

        # Check room availability
        if selected_location.get('Availability', 5) > 0:
            # Update availability and book the room
            selected_location['Availability'] = selected_location.get('Availability', 5) - 1
            print("Booking successful! Thank you.")
        else:
            print("Sorry, no available rooms for booking.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def add_location():
    print("\nAdding a new location:")
    name = input("Enter the name of the location: ")
    type_location = input("Enter the type of the location (e.g., Hotel, Airbnb, Hostel): ")
    address = input("Enter the address of the location: ")
    other_info = input("Enter any other information about the location (e.g., rating, phone number): ")

    # Create a new dictionary to store the location details
    user_location = {
        'name': name,
        'type': type_location,
        'address': address,
        'other_info': other_info,
        'Availability': 5  # Set initial room availability to 5
    }

    # Append the new location to the list of locations
    locations_list.append(user_location)

    print(f"Location '{name}' has been added successfully.")


def search_locations():
    print("\nAvailable Cities:")
    for i, city in enumerate(cities, start=1):
        print(f"{i}. {city.name}")

    city_choice = input("Enter the number of the city to search for locations: ")

    try:
        city_index = int(city_choice)
        if 1 <= city_index <= len(cities):
            selected_city = cities[city_index - 1]
            print(f"\nCity: {selected_city.name}")
            print("\n---Hotels---")
            for i, hotel in enumerate(selected_city.hotels, start=1):
                print(f"{i}- {hotel} - Availability: {hotel.get('availability', 5)} rooms")

            print("\n---Apartments---")
            for i, apartment in enumerate(selected_city.apartments, start=1):
                print(f"{i}- {apartment} - Availability: {apartment.get('availability', 5)} rooms")

            # Ask the user what they want to do after displaying locations
            user_choice = input(
                "\nWhat would you like to do?\n"
                "1. Book a room\n"
                "2. Go back to the main menu\n"
                "Enter your choice (1/2): "
            )
            if user_choice == '1':
                book_now(selected_city, cities, locations_list)
            elif user_choice == '2':
                return
            else:
                print("Invalid choice. Returning to the main menu.")
        else:
            print("Invalid city choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def save_location_to_file(location, filename="user_locations.json"):
    try:
        with open(filename, 'r') as file:
            user_saved_locations = json.load(file)
    except FileNotFoundError:
        user_saved_locations = []

    user_saved_locations.append(location)

    with open(filename, 'w') as file:
        json.dump(user_saved_locations, file, indent=2)

    print(f"Location '{location['Place']}' saved to {filename}.")


def print_sorted_locations():
    all_locations = cities + locations_list
    all_locations.sort(key=lambda x: x.name)  # Use x.name instead of x['name']
    print("\nAll Locations (Sorted by Name):")
    for i, location in enumerate(all_locations, start=1):
        print(f"{i}. {location.name} ({location.type})")  # Use location.name and location.type

# Inside your 'show_menu_after_login' function, update the '6' case like this:

elif choice == '6':
    sub_choice = input("Save or load locations? (S/L): ").upper()
    if sub_choice == 'S':
        print_sorted_locations()
        location_choice = input("Enter the number of the location to save (or 0 to go back): ")
        if location_choice == '0':
            continue  # Go back to the main menu
        save_location_to_file(all_locations[int(location_choice) - 1])
    elif sub_choice == 'L':
        user_locations = load_locations_from_file()
        if user_locations:
            print_sorted_locations()
            location_choice = input("Enter the number of the location to load (or 0 to go back): ")
            if location_choice == '0':
                continue  # Go back to the main menu
            selected_location = user_locations[int(location_choice) - 1]
            print(f"Loaded location: {selected_location}")
            # Do something with the loaded location
        else:
            print("No locations to load.")
    else:
        print("Invalid choice. Please enter 'S' or 'L'.")

def find_route():
    # Implement the find_route functionality
    pass


def load_locations_from_file(filename="user_locations.json"):
    try:
        with open(filename, 'r') as file:
            user_locations = json.load(file)
        print(f"Locations loaded from {filename}.")
        return user_locations
    except FileNotFoundError:
        print(f"File {filename} not found. Returning an empty list.")
        return []


if __name__ == "__main__":
    main()


def load_locations_from_file(filename="user_locations.json"):
    try:
        with open(filename, 'r') as file:
            user_locations = json.load(file)
        print(f"Locations loaded from {filename}.")
        return user_locations
    except FileNotFoundError:
        print(f"File {filename} not found. Returning an empty list.")
        return []


def save_location_to_file(location, filename="user_locations.json"):
    try:
        with open(filename, 'r') as file:
            user_saved_locations = json.load(file)
    except FileNotFoundError:
        user_saved_locations = []

    user_saved_locations.append(location)

    with open(filename, 'w') as file:
        json.dump(user_saved_locations, file, indent=2)

    print(f"Location '{location['Place']}' saved to {filename}.")




def print_sorted_locations(all_cities, user_locations):
    all_locations = all_cities + user_locations
    all_locations.sort(key=lambda x: x['Place'])
    print("\nAll Locations (Sorted by Name):")
    for i, location in enumerate(all_locations, start=1):
        print(
            f"{i}. {location['Place']} ({location['type']}) - "
            f"Availability: {location.get('Availability', 5)} rooms"
        )




def display_all_places(cities, user_locations):
    print("\nAll Places:")

    for city in cities:
        # Print the city name
        print(f"\nCity: {city.name}")

        # Add hotels and apartments to the list of locations
        all_locations = city.hotels + city.apartments

        # Include user-added locations for this city
        user_city_locations = [loc for loc in user_locations if loc['Place'] == city.name]
        all_locations.extend(user_city_locations)

        # Bubble sort by name
        n = len(all_locations)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if all_locations[j]['Place'] > all_locations[j + 1]['Place']:
                    all_locations[j], all_locations[j + 1] = all_locations[j + 1], all_locations[j]

        # Print sorted locations under the city
        for location in all_locations:
            if 'type' in location:
                # User-added location or city
                print(f"   {location['type']}: {location['Place']} - "
                      f"Availability: {location.get('Availability', 5)} rooms")
            else:
                # City
                print(f"   Location: {location['Place']}")
