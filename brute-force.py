import itertools
import hashlib
import string
import time

# Function to hash the guessed password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# The stored password hash (this is the password you're trying to crack)
stored_password_hash = hash_password("cat")  # Use the password you're testing

# Brute-force attack function with report generation
def brute_force_attack(charset, max_length, rate_limit=0.1):
    total_guesses = sum(len(charset) ** i for i in range(1, max_length + 1))  # Total number of guesses
    current_guess = 0  # Track the current guess number
    start_time = time.time()  # Start the timer
    
    # Generate password combinations up to the max length
    for password_length in range(1, max_length + 1):
        for guess in itertools.product(charset, repeat=password_length):
            guess = ''.join(guess)  # Combine the tuple of characters into a string
            current_guess += 1
            print(f"Trying password: {guess} ({current_guess}/{total_guesses})")  # Show progress
            
            # Hash the guess and compare it to the stored hash
            if hash_password(guess) == stored_password_hash:
                elapsed_time = time.time() - start_time  # Calculate time taken
                return {
                    "password_found": guess,
                    "guesses_made": current_guess,
                    "time_taken": elapsed_time
                }
            
            # Simulate real-world... rate limiting by adding a delay. without rate-limiting, can guess millions per second depending on hardware
            time.sleep(rate_limit)  # Rate limiting (e.g., 0.1 second between guesses)
    
    return {
        "password_found": None,
        "guesses_made": current_guess,
        "time_taken": time.time() - start_time
    }

# Function to generate the report based on attack results
def generate_report(result):
    report = f"""
    Brute Force Attack Report
    -------------------------
    Password Found: {result['password_found'] if result['password_found'] else 'Not found'}
    Number of Guesses: {result['guesses_made']}
    Time Taken: {result['time_taken']:.2f} seconds
    Recommendations:
    - Use stronger passwords with a mix of uppercase, lowercase, digits, and symbols.
    - Enforce minimum password length (at least 8 characters).
    - Implement rate-limiting or account lockouts after several failed attempts.
    """
    print(report)

# Defining the character set (lowercase letters, digits)
charset = string.ascii_lowercase + string.digits
max_password_length = 3  # Keep this short for testing

# Run brute force attack
result = brute_force_attack(charset, max_password_length)

# Generate the report
generate_report(result)
