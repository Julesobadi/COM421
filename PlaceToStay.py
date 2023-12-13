
import json


class PlaceToStay:
    cities = {}

    def __init__(self, city, location_type, name):
        self.city = city
        self.location_type = location_type
        self.name = name
        self.availability = 10
        self.enquiries = []

    def show_menu_after_login(self):
        print("Choose an option: ")

        options = {
            1: "Add Location",
            2: "Search Location",
            3: "Display All Places",
            4: "Search Type of Location (Apartment, Hotel)",
            5: "Book Location",
            6: "Save/Load Locations",
            7: "FAQ",
            8: "Find Route",
            9: "Logout",
        }

        while True:
            for key, value in options.items():
                print(f"[{key}] {value}")

            user = int(input("Enter your choice: "))

            if user in options:
                return user
            else:
                print("Enter the correct option: ")

    def add_new_location(self):
        print("\nAdding a new location:")
        city = input("Enter the name of the City: ")
        location_type = input("Is it a Hotel or Apartment: ")
        name = input("Enter the name of the location:  ")
        availability = 10

        PlaceToStay.cities[city] = {
            'city': city,
            'location_type': location_type,
            'name': name,
            'availability': availability
        }

        print(f"Location '{name}' in '{city}' has been added successfully.")

    def search_locations(self):
        city_choice = input("Enter the name of the city to search for locations: ")

        matching_locations = []
        for place_city, place in PlaceToStay.cities.items():
            if city_choice.capitalize() in place_city.capitalize():
                matching_locations.append(place_city)

        if matching_locations:
            print(f"{city_choice} found ")
            for place_city in matching_locations:
                place = PlaceToStay.cities[place_city]
                print(f"City: {place['city']}")
                print(f"Type: {place['location_type']}")
                print(f"Name: {place['name']}")
                print(f"Availability: {place['availability']}")
        else:
            print(f"{city_choice} not found")

    def display_all_places(self):
        print("All Locations:")
        places_list = list(PlaceToStay.cities.values())
        self.quicksort(places_list, 0, len(places_list) - 1)

        for place in places_list:
            print(f"City: {place['city']}")
            print(f"Name: {place['name']}")
            print(f"Type: {place['location_type']}")
            print(f"Availability: {place['availability']}")
        print()

    def quicksort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quicksort(arr, low, pi - 1)
            self.quicksort(arr, pi + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]['name']
        i = low - 1

        for j in range(low, high):
            if arr[j]['name'] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def search_location_type(self):
        location_type = input("Enter the type of location to search (Apartment/Hotel): ").capitalize()

        matching_locations = []
        for place_city, place in PlaceToStay.cities.items():
            if location_type.capitalize() in place['location_type'].capitalize():
                matching_locations.append(place_city)

        if matching_locations:
            print(f"{location_type} found ")
            for place_city in matching_locations:
                place = PlaceToStay.cities[place_city]
                print(f"City: {place['city']}")
                print(f"Name: {place['name']}")
                print(f"Type: {place['location_type']}")
                print(f"Availability: {place['availability']}")
        else:
            print(f"{location_type} not found")

    def book_now(self):
        # Display all locations before booking
        self.display_all_places()

        hotel_apartments = input("Which place would you like to book: ")
        matching_locations = []
        for place_name, place in PlaceToStay.cities.items():
            if hotel_apartments.capitalize() in place['name'].capitalize():
                matching_locations.append(place_name)

        if matching_locations:
            place_name = matching_locations[0]
            booking_place = int(input("How many rooms would you like to book: "))
            if booking_place > 0:
                if booking_place <= PlaceToStay.cities[place_name].get('availability', 0):
                    PlaceToStay.cities[place_name]['availability'] -= booking_place
                    print(f"Booking successful! {booking_place} room(s) booked at {hotel_apartments}")
                else:
                    print("No rooms available")
        else:
            print(f"{hotel_apartments} not found")

    def manage_locations(self):
        print("\n1. Save All Locations")
        print("2. Save Specific Locations")
        print("3. Load Locations")
        choice = int(input("Enter your choice (1/2/3): "))

        if choice == 1:
            with open("place.json", "w") as file:
                json.dump(PlaceToStay.cities, file)
            print("All locations saved.")
        elif choice == 2:
            # Display all locations before choosing which ones to save
            self.display_all_places()

            # Get the sorted list of places
            sorted_places = list(PlaceToStay.cities.values())
            self.quicksort(sorted_places, 0, len(sorted_places) - 1)

            # Prompt the user to enter the names of places to save
            places_to_save_input = input("Enter the name of place to save: ")
            places_to_save_names = [place.strip().capitalize() for place in places_to_save_input]

            # Check if entered names are valid
            if all(place in [p['name'].capitalize() for p in sorted_places] for place in places_to_save_names):
                selected_places = {
                    place['name']: place for place in sorted_places if
                    place['name'].capitalize() in places_to_save_names
                }

                with open("place.json", "w") as file:
                    json.dump(selected_places, file)
                print("Selected locations saved.")
            else:
                print("No valid places selected.")
        elif choice == 3:
            with open("place.json") as file:
                PlaceToStay.cities = json.load(file)
                print("Locations loaded.\n")
                print(f"{PlaceToStay.cities.keys()}\n")
                print(f"{PlaceToStay.cities.values()}")
        else:
            print("Invalid choice.")

    def show_faq(self):
        choices = int(input("1. Write your enquiry\n2. Load inquiry (for staff only): "))

        if choices == 1:
            print("Choose an option:")
            place_type = input("Which place would you like to make the enquiry for: ")
            enquiry = input("Write your enquiry: ")
            enquiry_store = {'place_type': place_type, 'enquiry': enquiry}
            self.enquiries.append(enquiry_store)
            print("Thank you for your enquiry.")
        elif choices == 2:
            enquiry_store = self.enquiries
            if enquiry_store:
                print("Enquiries:")
                while enquiry_store:
                    last_enquiry = enquiry_store.pop()  # Remove and get the last added enquiry
                    print(f"Place: {last_enquiry['place_type']}")
                    print(f"Enquiry: {last_enquiry['enquiry']}")
                    print("---")
                print("Enquiries answered.")
            else:
                print("No enquiries to answer.")
        else:
            return self.show_menu_after_login()


if __name__ == "__main__":
    city = PlaceToStay("", "", "")

    while True:
        selected_choice = city.show_menu_after_login()

        if selected_choice == 1:
            city.add_new_location()
        elif selected_choice == 2:
            city.search_locations()
        elif selected_choice == 3:
            city.display_all_places()
        elif selected_choice == 4:
            city.search_location_type()
        elif selected_choice == 5:
            city.book_now()
        elif selected_choice == 6:
            city.manage_locations()
        elif selected_choice == 7:
            city.show_faq()
        elif selected_choice == 8:
            city.find_route()  # I noticed this method is not defined in your provided code
        elif selected_choice == 9:
            print("Logout successful. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
