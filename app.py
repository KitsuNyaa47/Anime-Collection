from flask import Flask, request, render_template, url_for, session
import  os
from dotenv import load_dotenv
from werkzeug.utils import redirect
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

anime_answers = {"yellow.jpg": "naruto",
                 "dog_and_chain.jpg": "chainsaw man",
                 "silver.jpg": "gintama",
                 "crushed_dreams.jpg": "hunter x hunter",
                 "gamble.jpg": "kakegurui",
                 "cosplay.jpg": "my dress up darling",
                 "not_a_fox.jpg": "spice and wolf",
                 "flowers.jpg": ["hell's paradise", "hells paradise"],
                 "giants.jpg": "attack on titan",
                 "orange.jpg": ["dragon ball", "dragon ball z"],
                 "sorcerers.jpg": "jujutsu kaisen",
                 "tech.jpg": ["cyberpunk", "cyberpunk edgerunners"]}

character_answers = {"aot.jpg": "sasha",
                 "assassin.jpg": "killua",
                 "cosplay.jpg": "marin",
                 "csm.png": "makima",
                 "cyberpunk.jpg": "lucy",
                 "gintama.jpg": "kagura",
                 "juju.jpg": "sukuna",
                 "oniisan.jpg": "itachi",
                 "rascal.jpg": "mai",
                 "sao.jpg": "asuna",
                 "sh.jpg": "raphtalia",
                 "spice.jpg": "holo"}

trivia_answers = {"What is the name of the demon fox trapped in Naruto?": "kurama",
                  "What is Hisoka's primary weapon?": ["card", "cards"],
                  "What is the name of the island where Eren Jaeger grew up?": "paradis",
                  "What is the name of Chainsaw-Man's pet devil?": "pochita",
                  "Who is the Asaemon assigned to Gabimaru in Hell's Paradise?": "sagiri",
                  "What is the name of the tech tower in Cyberpunk?": "arasaka"}

anime_image_list = list(anime_answers.keys())
character_image_list = list(character_answers.keys())

@app.route("/")

def home():
    return render_template("home.html")

@app.route("/anime", methods=["GET", "POST"])

def anime():
    if "anime_index" not in session:
        session["anime_index"] = 0
    if "anime_reveal" not in session:
        session["anime_reveal"] = False

    message = ""
    current_index = session["anime_index"]
    current_image = anime_image_list[current_index]
    correct_answer = anime_answers[current_image]

    if isinstance(correct_answer, str):
        correct_answer = [correct_answer.lower()]
    else:
        correct_answer = [ans.lower() for ans in correct_answer]

    if request.method == "POST":
        if "next" in request.form:
            session["anime_index"] = (current_index + 1) % len(anime_image_list)
            session["anime_reveal"] = False
            return redirect(url_for("anime"))

        elif "previous" in request.form:
            session["anime_index"] = (current_index - 1) % len(anime_image_list)
            session["anime_reveal"] = False
            return redirect(url_for("anime"))

        elif "anime_reveal" in request.form:
            session["anime_reveal"] = True
            return redirect(url_for("anime"))

        elif "guess" in request.form:
            guess = request.form["guess"].strip().lower()
            if guess in correct_answer:
                message = f"✔️ Correct! It's {correct_answer[0].title()}"
            else:
                message = "❌ Incorrect! Try again."

    image_path = f"anime_pics/{current_image}"
    revealed_answer = correct_answer[0].title() if session.get("anime_reveal") else None
    return render_template("anime.html", image=image_path, message=message, answer=revealed_answer)

@app.route("/character", methods=["GET", "POST"])

def characters():
    if "character_index" not in session:
        session["character_index"] = 0
    if "character_reveal" not in session:
        session["character_reveal"] = False

    message = ""
    current_index = session["character_index"]
    current_image = character_image_list[current_index]
    correct_answer = character_answers[current_image]

    if isinstance(correct_answer, str):
        correct_answer = [correct_answer.lower()]
    else:
        correct_answer = [ans.lower() for ans in correct_answer]

    if request.method == "POST":
        if "next" in request.form:
            session["character_index"] = (current_index + 1) % len(character_image_list)
            session["character_reveal"] = False
            return redirect(url_for("characters"))

        elif "previous" in request.form:
            session["character_index"] = (current_index - 1) % len(character_image_list)
            session["character_reveal"] = False
            return redirect(url_for("characters"))

        elif "character_reveal" in request.form:
            session["character_reveal"] = True
            return redirect(url_for("characters"))

        elif "guess" in request.form:
            guess = request.form["guess"].strip().lower()
            if guess in correct_answer:
                message = f"✔️ Correct! It's {correct_answer[0].title()}"
            else:
                message = "❌ Incorrect! Try again."

    image_path = f"character_pics/{current_image}"
    revealed_answer = correct_answer[0].title() if session.get("character_reveal") else None

    return render_template("character.html", image=image_path, message=message, answer=revealed_answer)

@app.route("/trivia", methods=["GET", "POST"])

def trivia():
    if "index" not in session:
        session["index"] = 0
    if "reveal" not in session:
        session["reveal"] = False

    message = ""
    current_index = session["index"]
    trivia_keys = list(trivia_answers.keys())
    current_question = trivia_keys[current_index]
    correct_answer = trivia_answers[current_question]

    if isinstance(correct_answer, str):
        correct_answer = [correct_answer.lower()]
    else:
        correct_answer = [ans.lower() for ans in correct_answer]

    if request.method == "POST":
        if "next" in request.form:
            session["index"] = (current_index + 1) % len(trivia_answers)
            session["reveal"] = False
            return redirect(url_for("trivia"))

        elif "previous" in request.form:
            session["index"] = (current_index - 1) % len(trivia_answers)
            session["reveal"] = False
            return  redirect(url_for("trivia"))

        elif "reveal" in request.form:
            session["reveal"] = True
            return  redirect(url_for("trivia"))

        elif "guess" in request.form:
            guess = request.form["guess"].strip().lower()
            if guess in correct_answer:
                message = f"✔️ Correct! It's {correct_answer[0].title()}"
            else:
                message = "❌ Incorrect! Try again."

    question_path = f"{current_question}"
    revealed_answer = correct_answer[0].title() if session.get("reveal") else None

    return render_template("trivia.html", question=question_path, message=message, answer=revealed_answer)

if __name__ == "__main__":
    app.run(debug=True)




