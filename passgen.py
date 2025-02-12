from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Function to check if a password is strong if not , provide what is necessary 
def is_strong_password(password):
    """Check if the password is strong."""
    reasons = []
    if len(password) < 8:
        reasons.append("Password must be at least 8 characters long.")
    if not any(c.isdigit() for c in password):
        reasons.append("Password must contain at least one digit.")
    if not any(c.isupper() for c in password):
        reasons.append("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        reasons.append("Password must contain at least one lowercase letter.")
    if not any(c in "!@#$%^&*()-_+=<>?{}[]|\\/~`" for c in password):
        reasons.append("Password must contain at least one special character.")
    
    return reasons  # Return reasons if password is not strong

# PassCheck route
@app.route('/')
def index():
    """Render the Password Checker page."""
    return render_template_string(''' 
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Checker</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #4b6cb7, #182848);
            background-size: 400% 400%;
            animation: gradientAnimation 20s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            color: #ffffff;
            overflow: hidden;
            transition: background 2s ease;
            perspective: 1000px;
        }

        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .container {
            background: rgba(0, 0, 0, 0.7);
            padding: 40px 50px;
            border-radius: 20px;
            width: 100%;
            max-width: 450px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.7s ease-in-out;
            transform-style: preserve-3d;
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        h1 {
            font-size: 36px;
            color: #fff;
            margin-bottom: 30px;
            font-weight: 700;
        }

        label {
            font-size: 18px;
            margin-bottom: 15px;
            display: block;
            font-weight: 600;
            color: #fff;
        }

        #passwordInput {
            padding: 12px;
            font-size: 16px;
            width: 100%;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 2px solid #ccc;
            outline: none;
            background-color: #1a1a1a;
            color: #fff;
            transition: all 0.3s ease;
        }

        #passwordInput:focus {
            border-color: #4CAF50;
            background-color: #333;
        }

        #visibilityToggle {
            cursor: pointer;
            font-size: 20px;
            margin-left: 10px;
            color: #ccc;
        }

        #visibilityToggle:hover {
            transform: scale(1.1);
        }

        button {
            padding: 15px;
            background-color: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            margin-top: 15px;
            transition: all 0.3s ease-in-out;
        }

        button:hover {
            background-color: #45a049;
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        #result {
            font-size: 20px;
            font-weight: 600;
            margin-top: 20px;
            opacity: 0;
            animation: fadeInResult 0.7s forwards;
        }

        @keyframes fadeInResult {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        .error {
            color: #e74c3c;
        }

        .success {
            color: #2ecc71;
        }

        p a {
            color: #4CAF50;
            text-decoration: none;
            font-weight: bold;
        }

        /* Particle animation */
        .particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .particle {
            position: absolute;
            border-radius: 50%;
            background-color: #0f0;
            opacity: 0.7;
            animation: particleMovement 5s linear infinite;
        }

        @keyframes particleMovement {
            0% { transform: translate(0, 0); }
            100% { transform: translate(100vw, 100vh); }
        }

        .digital-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: -1;
            animation: digitalEffect 3s linear infinite;
        }

        @keyframes digitalEffect {
            0% {
                background: rgba(0, 0, 0, 0.5);
                background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/e0/Matrix-digital-rain.svg');
                background-size: cover;
                background-position: center;
            }
            50% {
                background: rgba(0, 0, 0, 0.7);
                background-image: none;
            }
            100% {
                background: rgba(0, 0, 0, 0.5);
                background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/e0/Matrix-digital-rain.svg');
                background-size: cover;
                background-position: center;
            }
        }

    </style>
</head>
<body>
    <div class="digital-background"></div>

    <div class="particles">
        <div class="particle" style="width: 5px; height: 5px; animation-duration: 5s; animation-delay: 0s;"></div>
        <div class="particle" style="width: 6px; height: 6px; animation-duration: 6s; animation-delay: 2s;"></div>
        <div class="particle" style="width: 7px; height: 7px; animation-duration: 7s; animation-delay: 3s;"></div>
        <div class="particle" style="width: 4px; height: 4px; animation-duration: 4s; animation-delay: 1s;"></div>
        <div class="particle" style="width: 8px; height: 8px; animation-duration: 8s; animation-delay: 0.5s;"></div>
    </div>

    <div class="container">
        <h1>Password Strength Checker</h1>
        <label for="passwordInput">Enter Password:</label>
        <div style="position: relative;">
            <input type="password" id="passwordInput" placeholder="Type your password">
            <span id="visibilityToggle" onclick="toggleVisibility()">👁️</span>
        </div>
        <button id="checkButton" onclick="checkPassword()">Check Password</button>
        <p id="result"></p>
        <p><a href="/generator" style="color: #4CAF50; text-decoration: none; font-weight: bold;">Go to Password Generator</a></p>
    </div>
    
    <script>
        function checkPassword() {
            const passwordInput = document.getElementById('passwordInput');
            const password = passwordInput.value;

            fetch('/check-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password }),
            })
            .then(response => response.json())
            .then(data => {
                const resultElement = document.getElementById('result');
                resultElement.style.opacity = 1;  // Fade in result
                if (data.is_strong) {
                    resultElement.innerHTML = '<span class="success">Password is strong!</span>';
                } else {
                    let reasons = '<ul>';
                    data.reasons.forEach(function(reason) {
                        reasons += `<li class="error">${reason}</li>`;
                    });
                    reasons += '</ul>';
                    resultElement.innerHTML = `<span class="error">Password is not strong:</span>${reasons}`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        function toggleVisibility() {
            const passwordInput = document.getElementById('passwordInput');
            passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
            document.getElementById('visibilityToggle').style.transform = passwordInput.type === 'password' ? 'scale(1)' : 'scale(1.1)';
        }
    </script>
</body>
</html>
''')

#pass_gen route
@app.route('/generator')
def password_generator():
    """Render the Password Generator page."""
    return render_template_string('''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #4b6cb7, #182848);
            background-size: 400% 400%;
            animation: gradientAnimation 20s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            color: #ffffff;
            overflow: hidden;
            transition: background 2s ease;
            perspective: 1000px;
        }

        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .container {
            background: rgba(0, 0, 0, 0.7);
            padding: 40px 50px;
            border-radius: 20px;
            width: 100%;
            max-width: 450px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.7s ease-in-out;
            transform-style: preserve-3d;
        }

        h1 {
            font-size: 36px;
            text-align: center;
            margin-bottom: 30px;
        }

        #generatedPassword {
            font-size: 18px;
            margin: 20px 0;
            padding: 12px;
            background: #1a1a1a;
            color: #fff;
            border-radius: 8px;
            border: 2px solid #ccc;
            word-break: break-word;
            animation: slideIn 0.5s ease-in-out;
        }

        @keyframes slideIn {
            0% { opacity: 0; transform: translateX(-30px); }
            100% { opacity: 1; transform: translateX(0); }
        }

        button {
            padding: 15px;
            background-color: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            margin-top: 15px;
            transition: all 0.3s ease-in-out;
        }

        button:hover {
            background-color: #45a049;
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        p a {
            color: #4CAF50;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Password Generator</h1>
        <button onclick="generatePassword()">Generate Password</button>
        <p id="generatedPassword">Click the button to generate a password</p>
        <button class="copy-button" onclick="copyPassword()">Copy Password</button>
        <p><a href="/" style="color: #4CAF50; text-decoration: none; font-weight: bold;">Go to Password Strength Checker</a></p>
    </div>
    <script>
        function generatePassword() {
            const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+[]{}|;:,.<>?";
            const length = 16;
            let password = "";
            for (let i = 0; i < length; i++) {
                password += charset.charAt(Math.floor(Math.random() * charset.length));
            }
            document.getElementById("generatedPassword").innerText = password;
        }

        function copyPassword() {
            const passwordText = document.getElementById("generatedPassword").innerText;
            navigator.clipboard.writeText(passwordText)
                .then(() => {
                    alert("Password copied to clipboard!");
                })
                .catch(err => {
                    console.error("Error copying password: ", err);
                });
        }
    </script>
</body>
</html>
''')

# Password Strength Check route
@app.route('/check-password', methods=['POST'])
def check_password():
    """API route to check password strength."""
    data = request.get_json()
    password = data.get('password')
    reasons = is_strong_password(password)
    is_strong = len(reasons) == 0
    return jsonify({
        'is_strong': is_strong,
        'reasons': reasons
    })

if __name__ == '__main__':
    app.run(debug=True)
