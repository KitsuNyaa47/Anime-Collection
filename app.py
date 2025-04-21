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
                 "tech.jpg": ["cyberpunk", "cyberpunk edgerunners"],
                 "belmont.jpg": "castlevania",
                 "betrayal.jpg": "tower of god",
                 "brothers.jpg": "fullmetal alchemist",
                 "cannibals.jpg": "tokyo ghoul",
                 "criminals.jpg": "akudama drive",
                 "elf.jpg": "frieren",
                 "horror.jpg": ["higurashi", "higurashi when they cry"],
                 "kings.jpg": "k project",
                 "kintama.jpg": "dandadan",
                 "poison.jpg": "apothecary diaries",
                 "reapers.jpg": "bleach",
                 "ridiculous.jpg": "high school dxd"}

anime_hints = {  "yellow.jpg": "The main character's goal is to become the Hokage.",
                 "dog_and_chain.jpg": "The first word is something you use to cut down trees.",
                 "silver.jpg": "This is a comedy anime, the name translates to Silver Soul.",
                 "crushed_dreams.jpg": "The adventures of Gon and his three friends.",
                 "gamble.jpg": "The main theme is gambling.",
                 "cosplay.jpg": "A girl who likes to cosplay and her friend who makes her costumes.",
                 "not_a_fox.jpg": "A merchant befriends the wolf goddess.",
                 "flowers.jpg": "Criminals are sent to an island to find the elixir of life.",
                 "giants.jpg": "Eldians on an island live in fear of giants.",
                 "orange.jpg": "The main character's name is Goku.",
                 "sorcerers.jpg": "Itadori and his comrades fight against curses.",
                 "tech.jpg": "A world where technology is very advanced.",
                 "belmont.jpg": "A belmont, a vampire and a sorcerer fight against Dracula's forces.",
                 "betrayal.jpg": "A boy chases after his friend who wants to see the stars.",
                 "brothers.jpg": "Two brothers use techniques to try recover what they lost.",
                 "cannibals.jpg": "The main character is fooled by a pretty lady and nearly dies.",
                 "criminals.jpg": "A bunch of criminals are given a mission.",
                 "elf.jpg": "Two mages and a warrior start a journey to heaven.",
                 "horror.jpg": "Cute school girls are not what they seem.",
                 "kings.jpg": "The seven clans of color rule over Japan.",
                 "kintama.jpg": "A boy loses his precious family jewels.",
                 "poison.jpg": "A poison tester solves mysteries in the palace.",
                 "reapers.jpg": "A teenager gains soul reaper powers to protect humans from evil.",
                 "ridiculous.jpg": "A boy is surrounded by girls and uses strange powers"}

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
                     "spice.jpg": "holo",
                     "apothecary.jpg": "maomao",
                     "axe.jpg": "stark",
                     "nothisrealname.jpg": "okarun",
                     "purple_cannibal.png": "rize",
                     "ToGYellow.jpg": "rachel"}

character_hints = {  "aot.jpg": "The girl who loves potatoes.",
                     "assassin.jpg": "He's from an esteemed assassin family.",
                     "cosplay.jpg": "A girl who likes to cosplay.",
                     "csm.png": "The woman that Denji is obsessed with.",
                     "cyberpunk.jpg": "In cyberpunk, David joins her in stealing from Arasaka.",
                     "gintama.jpg": "The girl who is always with Gintoki and Shinpachi.",
                     "juju.jpg": "He lives within the body of Itadori Yuuji.",
                     "oniisan.jpg": "The older brother of Sasuke.",
                     "rascal.jpg": "The bunny in Rascal Does Not Dream of Bunny Girl Senpai.",
                     "sao.jpg": "The strong female character in Sword Art Online.",
                     "sh.jpg": "Racoon girl in Shield Hero.",
                     "spice.jpg": "Wolf Goddess.",
                     "apothecary.jpg": "A poison tester who solves mysteries in the palace.",
                     "axe.jpg": "The warrior that accompanies Frieren.",
                     "nothisrealname.jpg": "He was given this name by Momo.",
                     "purple_cannibal.png": "A ghoul that manages to deceive the main character.",
                     "ToGYellow.jpg": "The girl who found Bam."}

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
    if "anime_hint" not in session:
        session["anime_hint"] = False

    message = ""
    current_index = session["anime_index"]
    current_image = anime_image_list[current_index]
    correct_answer = anime_answers[current_image]
    anime_hint = anime_hints[current_image]

    if isinstance(correct_answer, str):
        correct_answer = [correct_answer.lower()]
    else:
        correct_answer = [ans.lower() for ans in correct_answer]

    if request.method == "POST":
        if "next" in request.form:
            session["anime_index"] = (current_index + 1) % len(anime_image_list)
            session["anime_reveal"] = False
            session["anime_hint"] = False
            return redirect(url_for("anime"))

        elif "previous" in request.form:
            session["anime_index"] = (current_index - 1) % len(anime_image_list)
            session["anime_reveal"] = False
            session["anime_hint"] = False
            return redirect(url_for("anime"))

        elif "anime_reveal" in request.form:
            session["anime_reveal"] = True
            session["anime_hint"] = False
            return redirect(url_for("anime"))

        elif "anime_hint" in request.form:
            session["anime_hint"] = True
            session["anime_reveal"] = False
            return redirect(url_for("anime"))

        elif "guess" in request.form:
            guess = request.form["guess"].strip().lower()
            if guess in correct_answer:
                message = f"✔️ Correct! It's {correct_answer[0].title()}"
            else:
                message = "❌ Incorrect! Try again."

    image_path = f"anime_pics/{current_image}"
    revealed_hint = anime_hint if session.get("anime_hint") else None
    revealed_answer = correct_answer[0].title() if session.get("anime_reveal") else None
    return render_template("anime.html", image=image_path, message=message, answer=revealed_answer, hint=revealed_hint)

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
    character_hint = character_hints[current_image]

    if isinstance(correct_answer, str):
        correct_answer = [correct_answer.lower()]
    else:
        correct_answer = [ans.lower() for ans in correct_answer]

    if request.method == "POST":
        if "next" in request.form:
            session["character_index"] = (current_index + 1) % len(character_image_list)
            session["character_reveal"] = False
            session["character_hint"] = False
            return redirect(url_for("characters"))

        elif "previous" in request.form:
            session["character_index"] = (current_index - 1) % len(character_image_list)
            session["character_reveal"] = False
            session ["character_hint"] = False
            return redirect(url_for("characters"))

        elif "character_hint" in request.form:
            session["character_reveal"] = False
            session["character_hint"] = True
            return  redirect(url_for("characters"))

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
    revealed_hint = character_hint if session.get("character_hint") else None
    revealed_answer = correct_answer[0].title() if session.get("character_reveal") else None

    return render_template("character.html", image=image_path, message=message, answer=revealed_answer, hint=revealed_hint)

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




