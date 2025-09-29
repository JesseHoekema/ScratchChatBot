import scratchattach as sa
import google.generativeai as genai
import warnings
from dotenv import load_dotenv
import os

load_dotenv()

warnings.filterwarnings(
    "ignore",
    category=sa.LoginDataWarning
)
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

session = sa.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
cloud = session.connect_tw_cloud(os.getenv("PROJECT_ID"))
events = cloud.events()
encode_map = {
    "a": "001", "b": "002", "c": "003", "d": "004", "e": "005",
    "f": "006", "g": "007", "h": "008", "i": "009", "j": "010",
    "k": "011", "l": "012", "m": "013", "n": "014", "o": "015",
    "p": "016", "q": "017", "r": "018", "s": "019", "t": "020",
    "u": "021", "v": "022", "w": "023", "x": "024", "y": "025",
    "z": "026", "1": "027", "2": "028", "3": "029", "4": "030",
    "5": "031", "6": "032", "7": "033", "8": "034", "9": "035",
    " ": "036", ".": "037", ",": "038", "?": "039", "<": "040",
    ">": "041", "(": "042", ")": "043", "[": "044", "]": "045",
    "{": "046", "}": "047", ":": "048", ";": "049", "'": "050",
    '"': "051", "\\": "052", "/": "053", "|": "054", "!": "055",
    "@": "056", "#": "057", "$": "058", "%": "059", "^": "060",
    "&": "061", "*": "062", "0": "063", "-": "064", "_": "065"
}
decode_map = {v: k for k, v in encode_map.items()}


def encode(text: str) -> str:
    encoded = ""
    for char in text:
        if char in encode_map:
            encoded += encode_map[char]
        else:
            raise ValueError(f"TurboWrap => Character '{char}' not in encoding map.")
    return encoded



def decode(triplets: str) -> str:
    if len(triplets) % 3 != 0:
        raise ValueError("TurboWrap => Triplets string length must be a multiple of 3.")

    decoded = ""
    for i in range(0, len(triplets), 3):
        triplet = triplets[i:i+3]
        if triplet in decode_map:
            decoded += decode_map[triplet]
        else:
            continue
    return decoded


def ask_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(
            f"{prompt}\n\nAlways reply briefly in under 200 characters."
        )
        text = response.text.strip()
        return text[:200]  
    except Exception as e:
        return f"TurboWrap => An error occurred: {e}"


@events.event
def on_set(activity):
    if activity.var == "prompt":
        print("TurboWrap => New prompt received.")
        prompt = decode(activity.value)
        response = ask_gemini(prompt)
        cleaned_response = response.lower()
        encoded_response = encode(''.join(c for c in cleaned_response if c in encode_map))
        cloud.set_var("response", encoded_response)
        cloud.set_var("response_first", 1)


@events.event
def on_ready():
    print("TurboWrap => Event listener ready!")


def ping():
    return "pong"

events.start()
