import csv
import os

MOVIES_FILE = "movies.csv"
BOOKINGS_FILE = "bookings.csv"
USERS_FILE = "users.csv"
SEATS_PER_ROW = 10
ROWS = 5
SEAT_LIMIT = SEATS_PER_ROW * ROWS


def load_csv(file):
    if not os.path.exists(file):
        return []
    with open(file, mode='r', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(file, data, fieldnames):
    with open(file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(file, row, fieldnames):
    file_exists = os.path.exists(file)
    with open(file, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def register_user():
    users = load_csv(USERS_FILE)
    username = input("Choose a username: ").strip()
    if any(u['username'] == username for u in users):
        print("Username already exists.")
        return None
    append_csv(USERS_FILE, {'username': username}, ['username'])
    print("User registered successfully.")
    return username

def login_user():
    users = load_csv(USERS_FILE)
    username = input("Enter username: ").strip()
    if any(u['username'] == username for u in users):
        return username
    print("User not found.")
    return None

def show_seat_map(booked_seats):
    print("\nSeat Map (X = Booked, O = Available):")
    for row in range(ROWS):
        for col in range(SEATS_PER_ROW):
            seat = chr(65 + row) + str(col + 1)
            print("X" if seat in booked_seats else "O", end=' ')
        print()

def generate_seat_list():
    return [chr(65 + row) + str(col + 1) for row in range(ROWS) for col in range(SEATS_PER_ROW)]

def list_movies():
    movies = load_csv(MOVIES_FILE)
    if not movies:
        print("No movies available.")
        return
    genres = set(m['genre'] for m in movies)
    for genre in genres:
        print(f"\n🎬 {genre} Movies:")
        for m in movies:
            if m['genre'] == genre:
                print(f"ID: {m['movie_id']}, Name: {m['movie_name']}, Screen: {m['screen']}, Showtimes: {m['showtimes']}, Price: ₹{m['price']}")

def select_movie():
    movies = load_csv(MOVIES_FILE)
    movie_id = input("Enter Movie ID: ").strip()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        print("Movie not found.")
        return None, None
    showtimes = [s.strip() for s in movie['showtimes'].split(",")]
    for i, s in enumerate(showtimes):
        print(f"{i+1}. {s}")
    choice = input("Choose showtime number: ").strip()
    if not choice.isdigit() or int(choice) not in range(1, len(showtimes)+1):
        print("Invalid showtime.")
        return None, None
    return movie, showtimes[int(choice)-1]

def get_booked_seats(movie_id, showtime):
    bookings = load_csv(BOOKINGS_FILE)
    booked = [seat for b in bookings if b['movie_id'] == movie_id and b['showtime'] == showtime for seat in b['seats'].split(';')]
    return booked

def book_seats(username):
    movie, showtime = select_movie()
    if not movie:
        return
    booked = get_booked_seats(movie['movie_id'], showtime)
    show_seat_map(booked)
    seat_list = generate_seat_list()
    available = [s for s in seat_list if s not in booked]
    try:
        seats = input("Enter seats to book (comma separated): ").strip().upper().split(',')
        seats = [s.strip() for s in seats if s.strip() in available]
        if not seats:
            print("Invalid or already booked seats.")
            return
    except:
        print("Invalid input.")
        return
    total = len(seats) * int(movie['price'])
    print(f"\nBooking Summary for {username}:")
    print(f"Movie: {movie['movie_name']}, Showtime: {showtime}, Seats: {', '.join(seats)}, Total: ₹{total}")
    confirm = input("Confirm booking? (y/n): ").strip().lower()
    if confirm == 'y':
        append_csv(BOOKINGS_FILE, {
            'username': username,
            'movie_id': movie['movie_id'],
            'movie_name': movie['movie_name'],
            'showtime': showtime,
            'seats': ';'.join(seats),
            'total': str(total)
        }, ['username', 'movie_id', 'movie_name', 'showtime', 'seats', 'total'])
        print(" Booking confirmed!")
    else:
        print(" Booking cancelled.")

def view_user_bookings(username):
    bookings = load_csv(BOOKINGS_FILE)
    user_bookings = [b for b in bookings if b['username'] == username]
    if not user_bookings:
        print("No bookings found.")
        return
    for i, b in enumerate(user_bookings, start=1):
        print(f"{i}. {b['movie_name']} | {b['showtime']} | Seats: {b['seats']} | ₹{b['total']}")

def main():
    print("Welcome to the Movie Booking System")
    user = None
    while not user:
        print("\n1. Login\n2. Register")
        choice = input("Choose option: ").strip()
        if choice == '1':
            user = login_user()
        elif choice == '2':
            user = register_user()
        else:
            print("Invalid choice.")

    while True:
        print("\n Menu")
        print("1. List Movies")
        print("2. Book Tickets")
        print("3. View My Bookings")
        print("4. Exit")
        opt = input("Choose option: ").strip()
        if opt == '1':
            list_movies()
        elif opt == '2':
            book_seats(user)
        elif opt == '3':
            view_user_bookings(user)
        elif opt == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
