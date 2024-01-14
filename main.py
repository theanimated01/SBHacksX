import os
import sys
import time
import subprocess
import torch
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
from cat import CatWindow
from custom import CustomizationWindow, get_user_pref, get_quit_status
from urllib.parse import urlparse, parse_qs
from sentence_transformers import SentenceTransformer
from google.cloud import language_v1


study_list = ["New Tab", "chegg", "quora", "stackoverflow", "khanacademy", "coursera", "quizlet", "Wikipedia", "openai"]

class MainFunctionalityStarter(QObject):
    start_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.start_signal.connect(self.start_main_functionality)

    def start_main_functionality(self):
        threading.Thread(target=main_func).start()

def close_tab():
    try:
        cat_window.enable_chase = True
        close_tab_script = """
        tell application "Google Chrome"
            close active tab of first window
        end tell
        """
        subprocess.run(["osascript", "-e", close_tab_script])
    except Exception as e:
        print(f"Failed to close tab: {e}")


def analyze_text(content):
    try:
        client = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_entities(document=document)
        return response.entities
    except Exception as e:
        print(f"Error during Google NLP API call: {e}")
        return []


def encode_text(text):
    # Use the model to encode the text and convert to tensor
    encoded_text = model.encode(text, convert_to_tensor=True)
    # Convert to 1D tensor if not already
    return encoded_text if len(encoded_text.shape) == 1 else encoded_text.squeeze()


def cosine_similarity(vec1, vec2):
    # Reshape the vectors to 2D tensors if they are 1D
    if len(vec1.shape) == 1:
        vec1 = vec1.view(1, -1)
    if len(vec2.shape) == 1:
        vec2 = vec2.view(1, -1)
    
    return torch.nn.functional.cosine_similarity(vec1, vec2, dim=1).item()



def get_chrome_info():
    apple_script = """
        tell application "Google Chrome"
            set activeTab to active tab of first window
            set tabTitle to title of activeTab
            set tabUrl to URL of activeTab
            return {tabTitle, tabUrl}
        end tell
    """

    osa_command = f"osascript -e '{apple_script}'"
    output = subprocess.check_output(osa_command, shell=True).decode('utf-8').strip()
    tab_title, tab_url = output.split(', ', 1)
    parsed_url = urlparse(tab_url)
    domain = parsed_url.netloc
    path = parsed_url.path
    query_string = parsed_url.query
    parsed_query = parse_qs(query_string)
    search_query = None
    if "google" in domain or "google" in path:
        # The search query parameter in Google Search URL is 'q'
        search_query = parsed_query.get('q')
    elif "youtube" in domain or "youtube" in path:
        # The search query parameter in YouTube URL is 'search_query'
        if (user_pref["YouTube"]):
            search_query = "override"
        else:
            search_query = parsed_query.get('search_query')
    elif any(i in domain for i in study_list):
        search_query = "override"
    elif "netflix" in domain or "netflix" in path:
        if (user_pref["Netflix"]):
            search_query = "override"
        else:
            search_query = "restricted"
    elif "instagram" in domain or "instagram" in path or "twitter" in domain or "twitter" in path or "facebook" in domain or "facebook" in path or "tiktok" in domain or "tiktok" in path or "pinterest" in domain or "pinterest" in path:
        if (user_pref["Social Media"]):
            search_query = "override"
        else:
            search_query = "restricted"
    elif "amazon" in domain or "amazon" in path or "shein" in domain or "shein" in path or "target" in domain or "target" in path or "etsy" in domain or "etsy" in path or "ebay" in domain or "ebay" in path:
        if (user_pref["Shopping"]):
            search_query = "override"
        else:
            search_query = "restricted"
    if search_query != None:
        if search_query == "restricted":
            return search_query
        elif search_query == "override":
            return search_query
        else:
            return ' '.join(search_query)
    else:
        return tab_title

def main_func():
    global user_pref
    global quit_app
    quit_app = get_quit_status()


    while not quit_app:
        user_pref = get_user_pref()
        search = ""
        focus_topic = user_pref["Topic"]
        url_content = get_chrome_info()
        if url_content in study_list:
            url_content = "override"
        if url_content:
            if (url_content == "restricted"):
                close_tab()
            elif (url_content != "override"):
                keywords = analyze_text(url_content)
                for keyword in keywords:
                    if (keyword.salience > 0.6):
                        search +=  keyword.name
                focus_topic_vec = encode_text(focus_topic)
                search_vec = encode_text(url_content)

                similarity_score = cosine_similarity(focus_topic_vec, search_vec)
                if (similarity_score < 0.4):
                    close_tab()

        else:
            print("No active Chrome tab found.")

        time.sleep(3)
        quit_app = get_quit_status()


if __name__ == "__main__":

    model = SentenceTransformer('all-MiniLM-L6-v2')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sbhacks10-2bfb17f06a90.json')
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    app = QApplication(sys.argv)
    customization_window = CustomizationWindow()
    cat_window = CatWindow()
    starter = MainFunctionalityStarter()

    # Connect the signal from CustomizationWindow to the slot in MainFunctionalityStarter
    customization_window.topicEntered.connect(starter.start_signal.emit)

    customization_window.show()
    cat_window.show()
    sys.exit(app.exec_())
