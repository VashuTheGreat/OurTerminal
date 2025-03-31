import subprocess
import pickle
import numpy as np

# Load trained model and encoders
with open('customTerminal2.pkl', 'rb') as file:
    custom_terminal, le_x, le_y = pickle.load(file)  # Load all components

def answer(command):
    """Encodes the command, predicts, and decodes the result."""
    encoded_cmd = le_x.transform([command])  # Encode input
    prediction = custom_terminal.predict(np.array(encoded_cmd).reshape(-1, 1))  # Predict
    return le_y.inverse_transform(prediction)[0]  # Decode output

# Create a single persistent terminal session
shell_process = subprocess.Popen("cmd.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

def run_command(command):
    """Runs a system command in the same terminal session."""
    words = command.split(' ', 1)
    first, second = words[0], words[1] if len(words) > 1 else ''

    firstc = answer(first)  # Convert first word
    final_command = firstc + ' ' + second  # Construct final command

    print(f"Executing: {final_command}")

    # Send command to the running shell
    shell_process.stdin.write(final_command + "\n")
    shell_process.stdin.flush()

    # Read output (optional)
    output = shell_process.stdout.readline()
    if output:
        print(output.strip())

print("🔥 Vashu Terminal Started! Type 'exit' to quit. 🔥\n")

while True:
    user_input = input("Vashu's Terminal-> ")

    if user_input.lower() == "exit":
        print("Exiting Vashu Terminal...")
        shell_process.stdin.write("exit\n")
        shell_process.stdin.flush()
        shell_process.terminate()
        break  

    try:
        run_command(user_input)
    except Exception as e:
        print("⚠️ Error:", e)
