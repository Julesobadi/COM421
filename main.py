import json
from collections import deque

users = [{'username': 'Jules', 'password': 'Jawahir', 'favorites': [], 'role': 'staff'}]  # Default admin/staff member
faq_list = deque([
    "Can I cancel my booking?",
    "Can you resend my confirmation email?"
])

locations_list = []  # Add a list to store location details

all_locations = []

user_locations = []

location_counter = 1


class City:
    def __init__(self, name, hotels, apartments):
        self.name = name
        self.hotels = [{"Place": hotel, "Availability": 5} for hotel in hotels]
        self.apartments = [{"Place": apartment, "Availability": 5} for apartment in apartments]
        self.cities = {
            "Jeddah": {
                "hotels": ["Jeddah Hilton", "Andalus Habitat Hotel", "Mövenpick Hotel City Star Jeddah", "The 40th Pearl Hotel Suites", "Blue Diamond Hotel"],
                "apartments": ["Taj Jeddah Hotel Apartment", "White Pearl Al Basatin", "Khozama AlNahda", "Red Sea Studio PArtial Sea View", "Sky Private Studio"]
            },
            "Riyadh": {
                "hotels": ["Grand Plaza Hotel", "Centro Olaya", "Dahab Hotel", "Hilton Riyadh Hotel", "Aswar Hotel Suites Riyadh"],
                "apartments": ["Paradise of North Riyadh", "Rahaf Smart Residence", "Hitin Studio", "Walaa Homes-Luxury", "Diva Chalet"]
            },
            "Dammam": {
                "hotels": ["Residence Inn Marriott Dammam", "Swiss Al Hamra Hotel", "Tripper Inn Hotel", "Braira Al Dammam", "Radisson Hotel Dammam"],
                "apartments": ["TIME Dammam Residence", "Aros Al Faisaliah Units", "Lamssat El Saada", "Natwan Units", "Durra Taraf Residental"]
            },
            "Abha": {
                "hotels": ["Blue Inn Boutique", "Abha Palace Hotel", "Qimam Park Hotel", "Golden Andalus Hotel", "Pearly Hotel"],
                "apartments": ["Qasr Aldabab Housing Units", "Layali Rahaf Chalets", "Msakn Aldar Abha", "Sunrise Furnished Apartmet", "Masharef Abha Suites"]
            },
            "Makkah": {
                "hotels": ["Montana Al Azizia Hotel", "Hotel Inn Makkah", "Hibatullah Hotel Makkah", "Hilton Makkah Hotel", "Jumeirah Makkah"],
                "apartments": ["Holiday Apartment", "Rekaz Aparthotel", "Jabal Omar Hyatt Residental", "Makkah Towers", "Novotel Makkah"]
            }
        }



def show_menu_after_login(username, is_staff=False):
    while True:
        print("\n1. Add Location")
        print("2. Search Location")
        print("3. Display All Places")
        print("4. Search Type of Location (Apartment, Hotel)")
        print("5. Book Location")
        print("6. Save/Load Locations")
        print("7. FAQ")
        print("8. Find Route")
        print("9. Logout")

        choice = input(f"Hello, {username}! What would you like to do? (1-9): ")

        if choice == '1':
            add_location()
        elif choice == '2':
            search_locations()
        elif choice == '3':
            display_all_places(cities, user_locations, all_locations)
        elif choice == '4':
            search_location_type()
        elif choice == '5':
            book_now(cities, user_locations)
        elif choice == '6':
            manage_locations(user_locations, all_locations)
        elif choice == '7':
            show_faq(is_staff=is_staff)
        elif choice == '8':
            find_route()
        elif choice == '9':
            print(f"Logging out user '{username}'. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def add_location():
    print("\nAdding a new location:")
    name = input("Enter the name of the location: ")
    type_location = input("Enter the type of the location (e.g., Hotel, Airbnb, Hostel): ")
    address = input("Enter the address of the location: ")
    other_info = input("Enter any other information about the location (e.g., rating, phone number): ")

    user_location = {
        'Place': name,
        'type': type_location,
        'address': address,
        'other_info': other_info,
        'Availability': 5
    }

    user_locations.append(user_location)

    print(f"Location '{name}' has been added successfully.")


def search_locations():
    print("\nAvailable Cities:")
    for i, city in enumerate(cities, start=1):
        print(f"{i}. {city.name}")

    print(f"{len(cities) + 1}. User-Added Locations")

    city_choice = input("Enter the number of the city to search for locations (or 0 to go back): ")

    try:
        city_index = int(city_choice)
        if 1 <= city_index <= len(cities):
            selected_city = cities[city_index - 1]
            print(f"\nCity: {selected_city.name}")
            print("\n---Hotels---")
            for i, hotel in enumerate(selected_city.hotels, start=1):
                print(f"{i}. {hotel['Place']} - Availability: {hotel.get('Availability', 5)} rooms")

            print("\n---Apartments---")
            for i, apartment in enumerate(selected_city.apartments, start=1):
                print(f"{i}. {apartment['Place']} - Availability: {apartment.get('Availability', 5)} rooms")

            # Display user-added locations
            print("\n---User-Added Locations---")
            for i, location in enumerate(user_locations, start=1):
                print(f"{i}. {location['Place']} ({location['type']}) - Availability: {location.get('Availability', 5)} rooms")

            # Ask the user what they want to do after displaying locations
            user_choice = input(
                "\nWhat would you like to do?\n"
                "1. Book a room\n"
                "2. Go back to the main menu\n"
                "Enter your choice (1/2): "
            )
            if user_choice == '1':
                book_now(cities, user_locations)
            elif user_choice == '2':
                return
            else:
                print("Invalid choice. Returning to the main menu.")
        elif city_index == len(cities) + 1:
            # Display user-added locations only
            print("\n---User-Added Locations---")
            for i, location in enumerate(user_locations, start=1):
                print(f"{i}. {location['Place']} ({location['type']}) - Availability: {location.get('Availability', 5)} rooms")

            # Ask the user what they want to do after displaying locations
            user_choice = input(
                "\nWhat would you like to do?\n"
                "1. Book a room\n"
                "2. Go back to the main menu\n"
                "Enter your choice (1/2): "
            )
            if user_choice == '1':
                book_now(cities, user_locations)
            elif user_choice == '2':
                return
            else:
                print("Invalid choice. Returning to the main menu.")
        elif city_index == 0:
            return  # Go back to the main menu
        else:
            print("Invalid city choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def display_all_places(cities, user_locations, all_locations):
    global location_counter  # Use the global counter

    print("\nAll Places:")

    for city in cities:
        # Print the city name
        print(f"\nCity: {city.name}")

        # Add hotels and apartments to the list of locations
        all_locations_city = city.hotels + city.apartments

        # Include user-added locations for this city
        user_city_locations = [loc for loc in user_locations if loc['Place'] == city.name]
        all_locations_city.extend(user_city_locations)

        # Bubble sort by name
        n = len(all_locations_city)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if all_locations_city[j]['Place'] > all_locations_city[j + 1]['Place']:
                    all_locations_city[j], all_locations_city[j + 1] = all_locations_city[j + 1], all_locations_city[j]

        # Print sorted locations under the city
        for location in all_locations_city:
            if 'type' in location:
                # User-added location or city
                print(f"{location_counter}. {location['type']}: {location['Place']} - "
                      f"Availability: {location.get('Availability', 5)} rooms")
            else:
                # City
                print(f"{location_counter}. Location: {location['Place']}")

            location_counter += 1  # Increment the counter

    location_choice = input("Enter number of location you wish to save or 0 to go back: ")
    return location_choice


def manage_locations(cities, user_locations, all_locations):
    global location_counter  # Use the global counter

    print("\n1. Save Locations")
    print("2. Load Locations")
    print("X. Go back ")

    sub_choice = input("Enter your choice (1/2/X): ").upper()

    if sub_choice == '1':
        location_choice = display_all_places(cities, user_locations, [])

        if location_choice == '0':
            return  # Go back to the main menu

        try:
            location_index = int(location_choice) - 1

            if 0 <= location_index < len(all_locations):
                selected_location = all_locations[location_index]
                save_location_to_file(selected_location)
                print(f"Location '{selected_location['Place']}' saved to test.json.")
            else:
                print(f"Invalid location choice. Please enter a number between 1 and {location_counter - 1}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    elif sub_choice == 'X':
        return  # Go back to the main menu
    else:
        print("Invalid choice. Please enter '1', '2', or 'X.")


def save_location_to_file(self, filename="test.json"):
    with open(filename, "w") as file:
        json.dump(self.cities, file)


def print_sorted_locations(all_locations):
    # Bubble sort by 'Place' attribute
    n = len(all_locations)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if all_locations[j].get('Place', '') > all_locations[j + 1].get('Place', ''):
                all_locations[j], all_locations[j + 1] = all_locations[j + 1], all_locations[j]

    sorted_locations = []
    print("\nAll Locations (Sorted by Name):")

    for i, location in enumerate(all_locations, start=1):
        place_name = location.get('Place', 'Unknown Place')
        location_type = location.get('type', 'Unknown Type')
        availability = location.get('Availability', 5)

        print(f"{i}. {place_name} ({location_type}) - Availability: {availability} rooms")
        sorted_locations.append(location)

    return sorted_locations  # Return the sorted list


def load_from_file(filename="test.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


# In the manage_locations function:
# Reset the global counter before each use
location_counter = 1


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
            print(f"{i}. {location['Place']} - Availability: {location.get('Availability', 5)} rooms")
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
            try:
                question_index = int(input("Enter the number of the question to answer: "))
                if 1 <= question_index <= len(faq_list):
                    print(f"Answer to Question {question_index}: ...")  # Add corresponding answer
                else:
                    print("Invalid question number. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif not is_staff and choice.upper() == 'A':
            new_question = input("Enter your new question: ")
            faq_list.appendleft(new_question)  # Push new question to the left
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


def book_now(cities, user_locations):
    if not cities:
        print("Error: No cities available. Please add cities first.")
        return

    print("\nBooking a room:")

    # Prompt user to choose a city
    print("\nAvailable Cities:")
    for i, city in enumerate(cities, start=1):
        print(f"{i}. {city.name}")

    try:
        city_choice = int(input("Enter the number of the city you want to book in: "))
        selected_city = cities[city_choice - 1]

        # Ensure selected_city is a City object
        if not isinstance(selected_city, City):
            print("Error: Invalid city selection.")
            return

        # Display locations in the selected city
        print("\nLocations in the selected city:")
        all_locations = selected_city.hotels + selected_city.apartments + user_locations
        for i, location in enumerate(all_locations, start=1):
            location_type = location.get('type', "Unknown Type")
            print(f"{i}. {location['Place']} ({location_type}) - "
                  f"Availability: {location.get('Availability', 5)} rooms")

        location_choice = int(input("Enter the number of the location you want to book: "))

        if 1 <= location_choice <= len(all_locations):
            selected_location = all_locations[location_choice - 1]

            location_type = "Hotel" if selected_location in selected_city.hotels else "Apartment"
            if selected_location in user_locations:
                location_type = selected_location.get('type', "Unknown Type")

            print(f"\nYou've selected {location_type}: '{selected_location['Place']}' for booking.")

            if selected_location.get('Availability', 5) > 0:
                selected_location['Availability'] = selected_location.get('Availability', 5) - 1
                print("Booking successful! Thank you.")
            else:
                print("Sorry, no available rooms for booking.")
        else:
            print("Invalid choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def find_route():
    # Implement find_route functionality if needed
    pass


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


if __name__ == "__main__":
    main()
